import numbers
import random
import os
import PIL
import queue as Queue
import threading
from typing import Iterable

import mxnet as mx
import numpy as np
import torch
from functools import partial
from torch import distributed
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
from utils.utils_distributed_sampler import DistributedSampler
from utils.utils_distributed_sampler import get_dist_info, worker_init_fn


def get_dataloader(
    root_dir,
    local_rank,
    batch_size,
    dali = False,
    seed = 2048,
    num_workers = 2,
    sampler=None
    ) -> Iterable:

    rec = os.path.join(root_dir, 'train.rec')
    idx = os.path.join(root_dir, 'train.idx')
    train_set = None
    # Synthetic
    if root_dir == "synthetic":
        train_set = SyntheticDataset()

    # Mxnet RecordIO
    elif os.path.exists(rec) and os.path.exists(idx):
        train_set = MXFaceDataset(root_dir=root_dir, local_rank=local_rank)

    # Image Folder
    else:
        transform = transforms.Compose([
             transforms.RandomHorizontalFlip(),
             transforms.CenterCrop(size=(112, 112)), # According to paper?
             transforms.ToTensor(),
             transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
             ])
        train_set = ImageFolder(root_dir, transform)
        print(len(train_set))
    # DALI
    if dali:
        return dali_data_iter(
            batch_size=batch_size, rec_file=rec, idx_file=idx,
            num_threads=2, local_rank=local_rank)

    rank, world_size = get_dist_info()
    #train_sampler = DistributedSampler(
    #    train_set, num_replicas=world_size, rank=rank, shuffle=True, seed=seed)

    if seed is None:
        init_fn = None
    else:
        init_fn = partial(worker_init_fn, num_workers=num_workers, rank=rank, seed=seed)

    train_loader = DataLoaderX(
        local_rank=local_rank,
        dataset=train_set,
        batch_size=batch_size,
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True,
        worker_init_fn=init_fn,
    )

    return train_loader

class BackgroundGenerator(threading.Thread):
    def __init__(self, generator, local_rank, max_prefetch=6):
        super(BackgroundGenerator, self).__init__()
        self.queue = Queue.Queue(max_prefetch)
        self.generator = generator
        self.local_rank = local_rank
        self.daemon = True
        self.start()

    def run(self):
        torch.cuda.set_device(self.local_rank)
        for item in self.generator:
            self.queue.put(item)
        self.queue.put(None)

    def next(self):
        next_item = self.queue.get()
        if next_item is None:
            raise StopIteration
        return next_item

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self


class DataLoaderX(DataLoader):

    def __init__(self, local_rank, **kwargs):
        super(DataLoaderX, self).__init__(**kwargs)
        self.stream = torch.cuda.Stream(local_rank)
        self.local_rank = local_rank

    def __iter__(self):
        self.iter = super(DataLoaderX, self).__iter__()
        self.iter = BackgroundGenerator(self.iter, self.local_rank)
        self.preload()
        return self

    def preload(self):
        self.batch = next(self.iter, None)
        if self.batch is None:
            return None
        with torch.cuda.stream(self.stream):
            for k in range(len(self.batch)):
                self.batch[k] = self.batch[k].to(device=self.local_rank, non_blocking=True)

    def __next__(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        batch = self.batch
        if batch is None:
            raise StopIteration
        self.preload()
        return batch


class MXFaceDataset(Dataset):
    def __init__(self, root_dir, local_rank):
        super(MXFaceDataset, self).__init__()
        self.transform = transforms.Compose(
            [transforms.ToPILImage(),
             transforms.RandomHorizontalFlip(),
             transforms.ToTensor(),
             transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
             ])
        self.root_dir = root_dir
        self.local_rank = local_rank
        path_imgrec = os.path.join(root_dir, 'train.rec')
        path_imgidx = os.path.join(root_dir, 'train.idx')
        self.imgrec = mx.recordio.MXIndexedRecordIO(path_imgidx, path_imgrec, 'r')
        s = self.imgrec.read_idx(0)
        header, _ = mx.recordio.unpack(s)
        if header.flag > 0:
            self.header0 = (int(header.label[0]), int(header.label[1]))
            self.imgidx = np.array(range(1, int(header.label[0])))
        else:
            self.imgidx = np.array(list(self.imgrec.keys))

    def __getitem__(self, index):
        idx = self.imgidx[index]
        s = self.imgrec.read_idx(idx)
        header, img = mx.recordio.unpack(s)
        label = header.label
        if not isinstance(label, numbers.Number):
            label = label[0]
        label = torch.tensor(label, dtype=torch.long)
        sample = mx.image.imdecode(img).asnumpy()
        if self.transform is not None:
            sample = self.transform(sample)
        return sample, label

    def __len__(self):
        return len(self.imgidx)


class SyntheticDataset(Dataset):
    def __init__(self):
        super(SyntheticDataset, self).__init__()
        img = np.random.randint(0, 255, size=(112, 112, 3), dtype=np.int32)
        img = np.transpose(img, (2, 0, 1))
        img = torch.from_numpy(img).squeeze(0).float()
        img = ((img / 255) - 0.5) / 0.5
        self.img = img
        self.label = 1

    def __getitem__(self, index):
        return self.img, self.label

    def __len__(self):
        return 1000000


def dali_data_iter(
    batch_size: int, rec_file: str, idx_file: str, num_threads: int,
    initial_fill=32768, random_shuffle=True,
    prefetch_queue_depth=1, local_rank=0, name="reader",
    mean=(127.5, 127.5, 127.5), 
    std=(127.5, 127.5, 127.5)):
    """
    Parameters:
    ----------
    initial_fill: int
        Size of the buffer that is used for shuffling. If random_shuffle is False, this parameter is ignored.

    """
    rank: int = distributed.get_rank()
    world_size: int = distributed.get_world_size()
    import nvidia.dali.fn as fn
    import nvidia.dali.types as types
    from nvidia.dali.pipeline import Pipeline
    from nvidia.dali.plugin.pytorch import DALIClassificationIterator

    pipe = Pipeline(
        batch_size=batch_size, num_threads=num_threads,
        device_id=local_rank, prefetch_queue_depth=prefetch_queue_depth, )
    condition_flip = fn.random.coin_flip(probability=0.5)
    with pipe:
        jpegs, labels = fn.readers.mxnet(
            path=rec_file, index_path=idx_file, initial_fill=initial_fill, 
            num_shards=world_size, shard_id=rank,
            random_shuffle=random_shuffle, pad_last_batch=False, name=name)
        images = fn.decoders.image(jpegs, device="mixed", output_type=types.RGB)
        images = fn.crop_mirror_normalize(
            images, dtype=types.FLOAT, mean=mean, std=std, mirror=condition_flip)
        pipe.set_outputs(images, labels)
    pipe.build()
    return DALIWarper(DALIClassificationIterator(pipelines=[pipe], reader_name=name, ))

# TODO: Training the test on casia and then testing on LFW yields low accuracy
# See if we can fine-tune, or just directly train on LFW.
# If the latter, change the below dataloader
class LFWTrainDataset(Dataset):
    def __init__(self, info_file, img_dir='../../lfw',input_shape=(112, 112)):
        # Maybe change input size if necessary
        self.file = info_file
        self.img_dir = img_dir
        self.input_shape = input_shape
        with open(os.path.join(self.file), 'r') as fd:
            # Skip line with single number
            fd.readline()
            imgs = fd.readlines()
        self.imgs = [line.strip().split('\t') for line in imgs]
        #random.shuffle(self.imgs)
        self.transforms = transforms.Compose([
            transforms.RandomCrop(self.input_shape),
            transforms.ToTensor(),
             transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])],
            )
        self.labels = self.gen_labels()
    def gen_labels(self):
        labels = {}
        for i, dirname in enumerate(os.listdir(self.img_dir)):
            labels[dirname] = i
        return labels
            
        
    def __getitem__(self, idx):
        sample = self.imgs[idx]
        im1_pth = os.path.join(self.img_dir, 
                            f"{sample[0]}/{sample[0]}_{sample[1].rjust(4,'0')}.jpg")
        #print(im1_pth)

        ## Images of different people
        #if len(sample) == 4:
        #    matching = 0
        #    im2_pth = os.path.join(self.img_dir, 
        #        f"{sample[2]}/{sample[2]}_{sample[3].rjust(4,'0')}.jpg")
        ## Same person
        #elif len(sample) == 3:
        #    matching = 1
        #    im2_pth = os.path.join(self.img_dir, 
        #                 f"{sample[0]}/{sample[0]}_{sample[2].rjust(4,'0')}.jpg")

        im1 = PIL.Image.open(im1_pth)
        #im2 = PIL.Image.open(im2_pth)

        im1 = self.transforms(im1)
        #im2 = self.transforms(im2)

        return im1, im2, matching

    def __len__(self):
        return len(self.imgs)

# My dataloader for LFW pairs
class LFWEvalDataset(Dataset):
    def __init__(self, info_file, img_dir='../../lfw',input_shape=(112, 112)):
        # Maybe change input size if necessary
        self.file = info_file
        self.img_dir = img_dir
        self.input_shape = input_shape
        with open(os.path.join(self.file), 'r') as fd:
            # Skip line with single number
            fd.readline()
            imgs = fd.readlines()
        self.imgs = [line.strip().split('\t') for line in imgs]
        random.shuffle(self.imgs)
        self.transforms = transforms.Compose([
            transforms.RandomCrop(self.input_shape),
            transforms.ToTensor(),
             transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])],
            )

    def __getitem__(self, idx):
        sample = self.imgs[idx]
        #print(sample)
        #print(f"{sample[0]}_{sample[2].rjust(4, '0')}.jpg")
        im1_pth = os.path.join(self.img_dir, 
                            f"{sample[0]}/{sample[0]}_{sample[1].rjust(4,'0')}.jpg")
        #print(im1_pth)

        # Images of different people
        if len(sample) == 4:
            matching = 0
            im2_pth = os.path.join(self.img_dir, 
                f"{sample[2]}/{sample[2]}_{sample[3].rjust(4,'0')}.jpg")
        # Same person
        elif len(sample) == 3:
            matching = 1
            im2_pth = os.path.join(self.img_dir, 
                         f"{sample[0]}/{sample[0]}_{sample[2].rjust(4,'0')}.jpg")

        im1 = PIL.Image.open(im1_pth)
        im2 = PIL.Image.open(im2_pth)

        im1 = self.transforms(im1)
        im2 = self.transforms(im2)

        return (torch.sqrt(im1).type(torch.uint8)*2), (torch.sqrt(im2, ).type(torch.uint8)*2), matching

    def __len__(self):
        return len(self.imgs)

@torch.no_grad()
class DALIWarper(object):
    def __init__(self, dali_iter):
        self.iter = dali_iter

    def __next__(self):
        data_dict = self.iter.__next__()[0]
        tensor_data = data_dict['data'].cuda()
        tensor_label: torch.Tensor = data_dict['label'].cuda().long()
        tensor_label.squeeze_()
        return tensor_data, tensor_label

    def __iter__(self):
        return self

    def reset(self):
        self.iter.reset()

