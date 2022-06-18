#!/usr/bin/env python
# coding: utf-8

# # eBay Dataset Train Model

# In[1]:


import os
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter
from hierarchical import HierarchicalNetworkLoss
from tqdm import tqdm
from torch.optim import Adam
from torch.utils.data import DataLoader
from model.resnet50 import ResNet50
from loader import eProductTrainDataset

IMG_DIR = '../images/'
CSV_PATH = '../images/meta'
CHECKPOINT_PATH = './.checkpoints/model.pth'
epochs = 12
lr = 0.0002
batch_size = 8
device = torch.device("cuda:0" if torch.cuda.is_available()  else 'cpu')

model = ResNet50(num_classes=[16, 77, 1000])
optimizer = Adam(model.parameters(), lr=lr)


# ## DataLoaders

# In[2]:


trainDataset = eProductTrainDataset(
    os.path.join(CSV_PATH, 'train.csv'),
    IMG_DIR
    )
testDataset = eProductTrainDataset(
    os.path.join(CSV_PATH, 'query_part1.csv'),
    IMG_DIR
)
trainDataLoader = DataLoader(trainDataset, batch_size=batch_size)
HEL = HierarchicalNetworkLoss(device=device)
writer = SummaryWriter()


# In[3]:


def accuracy(predictions, labels):
    size = labels.size()[0]
    preds = torch.argmax(predictions, dim=1)
    
    correct = torch.sum(preds == labels)
    accuracy = correct * (100 / size)
    return accuracy.detach().cpu().item()

def plot_losses(losses, meta_accs, lvl2_accs, leaf_accs):
    print(losses[0].device)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot(range(len(losses)), losses)
    ax1.set_title('Loss value each epoch')
    
    ax2.plot(range(len(meta_accs)), meta_accs)
    ax2.set_title('Meta category accuracies')
    
    ax3.plot(range(len(lvl2_accs)), lvl2_accs)
    ax3.set_title('Level 2 Accuracies')
    
    ax4.plot(range(len(leaf_accs)), leaf_accs)
    ax4.set_title('Leaf category accuracies per epoch')


# In[4]:


try:
    checkpoint = torch.load(CHECKPOINT_PATH)
    if checkpoint:
        last_epoch = checkpoint['epoch']
        loss = model['loss']
        model.load_state_dict(checkpoint['model'])
        optimizer.load_state
    else:
        last_epoch = 0
        loss = 0
except FileNotFoundError:
    last_epoch = 0
    loss = 0


# 
# ## Train Loop

# In[ ]:


train_epoch_losses = []
train_epoch_accuracies = []
train_epoch_meta_accuracies = []
train_epoch_level2_accuracies = []
train_epoch_leaf_accuracies = []

model = model.to(device)
for epoch in range(last_epoch, epochs):
    epoch_loss = []
    epoch_meta_accuracy = []
    epoch_level2_accuracy = []
    epoch_leaf_accuracy = []
    
    meta_acc, lvl2_acc, leaf_acc = 0, 0, 0
    for i, batch in tqdm(enumerate(trainDataLoader)):
        meta_cats, l2_cats, leaf_cats, imgs = batch
        
        # Move data to GPU
        meta_cats = meta_cats.cuda()
        l2_cats = l2_cats.cuda()
        leaf_cats = leaf_cats.cuda()
        imgs = imgs.cuda()
        
        # Reset previous batch gradients
        optimizer.zero_grad()
        
        meta_preds, l2_preds, leaf_preds = model(imgs)
        
        # Layer Loss and Dependence loss
        predictions = [meta_preds, l2_preds, leaf_preds]
        labels = [meta_cats, l2_cats, leaf_cats]
        lloss = HEL.lloss(predictions, labels)
        dloss = HEL.dloss(predictions, labels)
        
        loss = dloss + lloss
        loss.backward()
        optimizer.step()
        
        # Plotting
        #print(f'Meta{accuracy(predictions[0], labels[0])}')
        #print(f'L2{accuracy(predictions[1], labels[1])}')
        #print(f'Leaf{accuracy(predictions[2], labels[2])}')

        meta_acc += accuracy(predictions[0], labels[0])
        lvl2_acc += accuracy(predictions[1], labels[1])
        leaf_acc += accuracy(predictions[2], labels[2])
        if i % 10000 == 0:
            print(f'[epoch {epoch}, batch {i}]: loss: {loss:.3f} meta: {(meta_acc / (i+1)):.3f} lvl2: {(lvl2_acc/ (i+1)):.3f} leaf: {(leaf_acc/ (i+1)):.3f}')
    
        writer.add_scalar('Accuracy/meta',meta_acc, epoch)
        writer.add_scalar('Accuracy/level2',lvl2_acc, epoch)
        writer.add_scalar('Accuracy/leaf', leaf_acc, epoch)
        writer.add_scalar('Loss/train', loss.item(), epoch)
        
    
    train_epoch_losses.append(loss.detach().cpu() ) # Only plotting the last loss value
    train_epoch_meta_accuracies.append(meta_acc / (i+1))
    train_epoch_level2_accuracies.append(lvl2_acc / (i+1))
    train_epoch_leaf_accuracies.append(leaf_acc / (i+1))
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss
    }, './.checkpoints/model.pt')
    
plot_losses(train_epoch_losses,
           train_epoch_meta_accuracies,
           train_epoch_level2_accuracies,
           train_epoch_leaf_accuracies
           )   


# 

# In[ ]:




