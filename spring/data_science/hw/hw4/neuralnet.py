import torch
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.utils.data import Dataset, DataLoader

# Convert the input to tensor
class tabularDataset(Dataset):
    # Input data should already be scaled
    def __init__(self,data:pd.DataFrame):
        self.data = data
        self.len = data.shape[0]

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        features = self.data.iloc[idx,:-1]
        label = self.data.iloc[idx, -1]
        
        return torch.tensor(features), torch.tensor(label)

class MLP(nn.Module):
    def __init__(self, input_dims:int, class_num:int):
        super(MLP, self).__init__()
        output_dims = input_dims # try with just constant

        self.drop = nn.Dropout(0.2)
        self.fc1 = nn.Linear(input_dims, output_dims)
        self.fc2 = nn.Linear(output_dims, output_dims)
        self.fc3 = nn.Linear(output_dims, class_num)

    def forward(self, data):
        x = F.relu(self.fc1(data))
        x = self.drop(x)

        x = F.relu(self.fc2(x))
        x = self.drop(x)

        x = self.fc3(x)
        return x
        


class tabularNet:
    def __init__(self):
        pass
    def fit(self, x:pd.DataFrame, y:pd.Series, n_labels=1, epochs=5, lr=0.001) -> float:
        dataset = tabularDataset(x)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

        dims = x.shape[1] - n_labels # Number of label columns in output 
        class_num = y.nunique()
        epochs = 10
        model = MLP(dims, class_num)
        for i in range(epochs):
            for feature, label in dataloader:
                # Inference
                feature = feature.float()
                label = label.float()
                print(label)
                out = model(feature)

                # Backprop

if __name__ == '__main__':
    df = pd.read_csv('./data/biodeg.csv')
    net = tabularNet()
    net.fit(df.iloc[:, :-1], df.iloc[:, -1])



