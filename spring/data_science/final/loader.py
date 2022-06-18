import os
import pandas as pd # Better way than dataframe?

from torchvision.io import read_image
from torch.utils.data import Dataset 

import torchvision.transforms as transforms

class eProductTrainDataset(Dataset):
    def __init__ (self, label_path, img_path):
        self.label_path = label_path
        self.img_path = img_path
        self.df = pd.read_csv(self.label_path)

        self.transforms = transforms.Compose([
                transforms.Resize((64, 64)),
                transforms.RandomRotation(0.2),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)) 
            ])


    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        item = self.df.iloc[idx, :]
        meta = item['META_CATEG_ID']
        l2 = item['CATEG_LVL2_ID']
        leaf = item['LEAF_CATEG_ID']
        image = read_image(os.path.join(self.img_path, item['IMAGE_PATH'])).float()
        return meta, l2, leaf, self.transforms(image)

class eProductTestDataset(Dataset):
    def __init__(self, label_path, csv_path):
        self.label_path = label_path
        self.csv_path = csv_path 
        self.df = pd.read_csv(os.path.join(self.label_path, self.csv_path))
        self.transforms = transforms.Compose([
                transforms.Resize((64, 64)),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
            ])

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        item = self.df.iloc[idx, :]
        uuid = item['UUID']
        path = item['IMAGE_PATH']
        image = read_image(os.path.join('../images/', path)).float()
        return uuid, self.transforms(image)

'''
if __name__ == '__main__':
    dl = eProductTrainDataset('../images/meta/train.csv', '../images/train/')
    meta, l2, leaf, im = dl.__getitem__(1)
    '''
