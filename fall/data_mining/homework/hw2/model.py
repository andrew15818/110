import torch
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from collections import OrderedDict
from torch.utils.data import Dataset, DataLoader

# Create a Dataset class so we can create our own DataLoader
class customDataset(Dataset):
    def __init__(self, data):
        tmp = data.values[:,:-1].astype(np.float32)
        self.data = torch.tensor(tmp)       
        self.labels = data.iloc[:,-1]
        self.label_dict = None
        self.len = len(tmp)

        if type(self.labels.iloc[0]) == str:
            self.label_dict = OrderedDict()
            self._int_class_names(self.labels.unique())

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        train = self.data[idx]
        label = self.labels.iloc[idx]
        if self.label_dict:
            label = self.label_dict[label]
        return train, label

    # Assign a numeric class ID to string classes
    def _int_class_names(self, labels):
        for i,label in enumerate(labels):
            self.label_dict[label] = i
        print(self.label_dict)


class NeuralClassifier(nn.Module):
    """ 
      dims: number of input features (no. columns in our data)
      class_num: Number of output classes
    """
    def __init__(self, dims:int, class_num:int):
        self.label_dict = OrderedDict()
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Running on {device}.')
        super(NeuralClassifier, self).__init__()

        self.linear1 = nn.Linear(dims, dims)
        self.linear2 = nn.Linear(dims, class_num)
        self.linear3 = nn.Linear(class_num, class_num)

    # forward feeds the data to the network
    def forward(self, data):
        x = self.linear1(data)        
        x = F.relu(x)
        x = F.relu(self.linear2(x))
        x = F.softmax(self.linear3(x))
        
        return x 

       
    # Preprocess the data and pass it through model
    def run(self, data):

        # Get all the rows, exclude the class label
        inputs = data.values[:,:-1].astype(np.float32)
        inputs = torch.tensor(inputs)

        # Start the feed-forward 

# TODO: How do we better adjust the hyperparams?
def train_model(data, dims:int, class_num:int) -> NeuralClassifier:
    # Hyperparameters
    epochs = 20
    batch_size = 16# Smaller for smaller sets?
    learning_rate = 0.01
    
    # Model and training data
    model = NeuralClassifier(dims, class_num)
    dataset = customDataset(data)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    criterion = nn.CrossEntropyLoss()
    labels = data.iloc[:,-1]
    optimizer = optim.SGD(model.parameters(),
                        lr=learning_rate)

    # Record the results for plotting 
    losses = []
    counter = []
    for epoch in range(epochs):
        for i, data in enumerate(dataloader, 0):
            x_train, y_train = data
            
            # Clear the gradient from previous run 
            optimizer.zero_grad()
            outputs = model(x_train)
            loss = criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
            print(loss.item())
    print('Finished training')
    PATH = './checkpoints/model.pth'
    torch.save(model.state_dict(), PATH)
    return model

#TODO: Test model
def test_model(model:NeuralClassifier):
    pass
