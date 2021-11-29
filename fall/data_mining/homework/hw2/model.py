import torch
import pandas as pd
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

from collections import OrderedDict
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Create a Dataset class so we can create our own DataLoader
class customDataset(Dataset):
    def __init__(self, data):
        tmp = data.values[:,:-1].astype(np.float32)
        scaler = StandardScaler()
        tmp = scaler.fit_transform(tmp)
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
        self.path = None
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
        x = F.softmax(self.linear3(x), dim=1)
        
        return x 
    def set_path(self, path):
        self.path = path
       

def train_model(data, dims:int, class_num:int, validation=None) -> NeuralClassifier:
    # Hyperparameters
    epochs = 100# or 40
    batch_size = 32# Smaller for smaller sets?
    learning_rate = 0.25# or .05
    
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
        batch_loss = 0
        for i, data in enumerate(dataloader, 0):
            x_train, y_train = data
            # Clear the gradient from previous run 
            optimizer.zero_grad()
            outputs = model(x_train)
            loss = criterion(outputs, y_train.long())
            loss.backward()
            optimizer.step()
            batch_loss += loss.item()

        losses.append(batch_loss / len(dataloader))
    print('Finished training')
    model.set_path('./checkpoints/model.pth')
    torch.save(model.state_dict(), model.path)
    plot_loss(losses)
    return model

def test_model(model:NeuralClassifier, testdata:pd.DataFrame):
    # Custom dataloader for our dataset
    dataset = customDataset(testdata)
    dataloader = DataLoader(dataset)
    
    total = 0
    correct = 0
    with torch.no_grad():
        for data in dataloader:
            # Inference
            attrs, ground_truth = data
            guess = model(attrs)
            _, predicted = torch.max(guess.data, 1)

            total += ground_truth.size(0)
            correct += (predicted == ground_truth).sum().item()
    print(f'Total Accuracy: {correct / total}')


# Plot the loss for each epoch
def plot_loss(losses):
    fig, ax = plt.subplots()
    ax.plot(range(len(losses)), losses)
    plt.show()
    pass
