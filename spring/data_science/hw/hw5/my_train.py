import argparse
import logging
import os
import torch
import random

import numpy as np
from torch.utils.data import DataLoader, SubsetRandomSampler
from torch import distributed
from torch.utils.tensorboard import SummaryWriter

from backbones import get_model
from dataset import get_dataloader
from losses import CombinedMarginLoss
from lr_scheduler import PolyScheduler
from partial_fc import PartialFC, PartialFCAdamW
from utils.utils_callbacks import CallBackLogging, CallBackVerification
from utils.utils_config import get_config
from utils.utils_logging import AverageMeter, init_logging

# Single machine single GPU
world_size = 1
rank = 0
distributed.init_process_group(
    backend="nccl",
    init_method="tcp://127.0.0.1:12584",
    rank=rank,
    world_size=world_size,
)
def get_sample_indices(ratio=0.25, img_dir='../../CASIA-WebFace'):
    offset = 0
    samples = []
    for dirname in os.listdir(img_dir):
        file_count = 0
        # Get file number in directory
        for file in os.listdir(f'{img_dir}/{dirname}'):
            file_count += 1
        
        chosen_num = int(file_count * ratio)
        chosen_indices = random.sample(range(0, file_count), chosen_num)
        print(f'{img_dir}/{dirname}: {chosen_indices}')
        
        # Add offset for dataloader
        for index in chosen_indices:
            samples.append(offset + index)
        
        offset += file_count
       
            
    return samples
def main(args):
   

    # Not using distributed learning
   
    cfg = get_config(args.config)
    samples = get_sample_indices(args.ratio)
    sampler = SubsetRandomSampler(samples)
    #setup_seed(seed=cfg.seed,cuda_deterministic=False)

    torch.cuda.set_device(args.local_rank)
    os.makedirs(cfg.output, exist_ok=True)
    init_logging(0, cfg.output)

    summary_writer = (
                    SummaryWriter(log_dir=os.path.join(cfg.output, "tensorboard"))
                    if rank == 0
                    else None
                )
    train_loader = get_dataloader(
                    cfg.rec,
                    args.local_rank,
                    cfg.batch_size,
                    cfg.dali,
                    cfg.seed,
                    cfg.num_workers,
                    sampler=sampler
                )
    backbone = get_model(
            cfg.network, dropout=0.0, fp16=cfg.fp16, num_features=cfg.embedding_size
            ).cuda()
    backbone.train()
    print(f'Training on {len(sampler)} images, ratio {args.ratio}')
    # Fix this in case
    #backbone._set_static_graph()
    
    margin_loss = CombinedMarginLoss(
                    64,
                    cfg.margin_list[0],
                    cfg.margin_list[1],
                    cfg.margin_list[2],
                    #cfg.interclass_filtering_method
                )
    if cfg.optimizer == "sgd":
        module_partial_fc = PartialFC(
                                margin_loss,
                                cfg.embedding_size,
                                cfg.num_classes,
                                cfg.sample_rate,
                                cfg.fp16
                            )
        module_partial_fc.train().cuda()
        opt = torch.optim.SGD(
                params=[{"params": backbone.parameters()}, {"params":module_partial_fc.parameters()}],
                lr=cfg.lr, weight_decay=cfg.weight_decay)
    
    cfg.total_batch_size = cfg.batch_size * world_size
    cfg.warmup_step = cfg.num_image // cfg.total_batch_size * cfg.warmup_epoch
    cfg.total_step = cfg.num_image // cfg.total_batch_size * cfg.num_epoch
    lr_scheduler = PolyScheduler(
        optimizer=opt,
        base_lr=cfg.lr,
        max_steps=cfg.total_step,
        warmup_steps=cfg.warmup_step
    )

    for key, value in cfg.items():
        num_space = 25 - len(key)
        logging.info(": " + key + " " * num_space + str(value))

    callback_verification = CallBackVerification(
        val_targets=cfg.val_targets, rec_prefix=cfg.rec, summary_writer=summary_writer
    )
    callback_logging = CallBackLogging(
        frequent=cfg.frequent,
        total_step=cfg.total_step,
        batch_size=cfg.batch_size,
        writer=summary_writer
    )

    loss_am = AverageMeter()
    start_epoch = 0
    global_step = 0
    amp = torch.cuda.amp.grad_scaler.GradScaler(growth_interval=100)
    
    for epoch in range(start_epoch, cfg.num_epoch):
        #if isinstance(train_loader, DataLoader):
        #    train_loader.sampler.set_epoch(epoch)
        for _, (img, local_labels) in enumerate(train_loader):
            global_step += 1
            local_embeddings = backbone(img)
            
            loss: torch.Tensor = module_partial_fc(local_embeddings, local_labels, opt)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm(backbone.parameters(), 5)
            opt.step()
            opt.zero_grad()
            lr_scheduler.step()

            with torch.no_grad():
                loss_am.update(loss.item(), 1)
                callback_logging(global_step, loss_am, 
                                 epoch, cfg.fp16, 
                                 lr_scheduler.get_last_lr()[0], amp)
                if global_step % cfg.verbose == 0 and global_step > 200:
                    callback_verification(global_step, backbone)
        path_pfc = os.path.join(cfg.output, "softmax_fc_gpu_{}.pt".format(rank))
        torch.save(module_partial_fc.state_dict(), path_pfc)

        if rank == 0:
            path_module = os.path.join(cfg.output, "model.pt")
            torch.save(backbone.state_dict(), path_module)
    if rank == 0:
        path_module = os.path.join(cfg.output, "model.pt")
        torch.save(backbone.state_dict(), path_module)    
   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Distributed Arcface Training in Pytorch")
    parser.add_argument("config", type=str, help="py config file")
    parser.add_argument("--ratio", type=float, help='Ratio of training images to use')
    parser.add_argument("--local_rank", type=int, default=0, help="local_rank")
    main(parser.parse_args())
