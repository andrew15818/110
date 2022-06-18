import torch
import torch.nn as nn
import torch.nn.functional as F

class HierarchicalNetworkLoss():
    def __init__(self, device='cpu', alpha=1, beta=0.8, ploss=3):
        self.device = device
        self.alpha = alpha
        self.beta = 0.8
        self.p_loss = 3
    
    def lloss(self, predictions:list, labels:list):  
        loss = 0
        if len(predictions) != len(labels):
            print("Length of predictions and labels lists should be the same!")
            
        for l in range(len(predictions)):
            loss += nn.CrossEntropyLoss()(predictions[l], labels[l])
            #print(loss)
        return self.alpha * loss
    
    def dependence(self, curr_level, prev_level, prev_level_labels):
        # Not sure if this is correct way of calculating D
        bools = []
        #print(prev_level_labels.shape())
        for b in range(curr_level.size()[0]):
            bool_arr = [1 if prev_level[b][i].item() == prev_level_labels[i] else 0 for i in range(curr_level.size()[0])]
            bools.append(bool_arr)
            
        return torch.FloatTensor(bools).to(self.device)
    def dloss(self, predictions:list, labels:list):
        dloss = 0
        for l in range(1, len(predictions)):
            curr_lvl_pred = torch.argmax(nn.Softmax(dim=1)(predictions[l]), dim=1)
            prev_lvl_pred = torch.argmax(nn.Softmax(dim=1)(predictions[l-1]), dim=1)
            
            # Need to check if currrent level prediction is child of prev level
            D = self.dependence(predictions[l], predictions[l-1], labels[l-1])
            
            # I think I already have these lines in D
            l_prev = torch.where(prev_lvl_pred == labels[l-1], torch.FloatTensor([0]).to(self.device), torch.FloatTensor([1]).to(self.device))
            l_curr = torch.where(curr_lvl_pred== labels[l], torch.FloatTensor([0]).to(self.device), torch.FloatTensor([1]).to(self.device))
            dloss += torch.sum(torch.pow(self.p_loss, D*l_prev)*torch.pow(self.p_loss, D*l_curr) -1)
                                         
        return self.beta * dloss
                                        