import torch
import torch.nn as nn

class NeuralClassifier(nn.Module):
    def __init__(self, dims:int, class_num:int):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Running on {device}.')
        super(NeuralClassifier, self).__init__()

        self.linear1 = nn.Linear(dims, dims)
        self.linear2 = nn.Linear(dims, class_num)
        self.linear3 = nn.Linear(class_num, class_num)

    # forward feeds the data to the network
    def forward(self, data):
        
        pass
