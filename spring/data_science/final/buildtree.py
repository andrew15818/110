#!/usr/bin/env python
# coding: utf-8

# ## Build semantic tree
# We need to build a semantic hash of the different leaf categories so that when we get the embedding from the network, we can quickly determine which to which class our picture belongs.
# After we determine the leaf class, we need to check with all the items in that set.

# In[1]:


import os
import PIL
import torch
import loader
import pickle

from tqdm import tqdm
from lshash.lshash import LSHash
from torch.utils.data import DataLoader
from model.resnet50 import ResNet50

IMG_DIR = '../images'
TRAIN_IMG = 'train'
INDEX_IMG = 'eval/index'


# ## Get index image embeddings
# If we loop through all the training images and get their model embeddings, we could make a kind of prototype for each class.
# The `index` contains our 1.1m images we have to search through. What I'm thinking:
# - Run each of the images through our model to get its embeddings.
# - Save it as a dictionary {uuid: embedding(or hash)}
# - For each query image, run it through LSH and use that to get its approx knn

# ### Load model

# In[2]:

device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu')
model = ResNet50()
checkpoint = torch.load('./.checkpoints/model.pt')
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

embDataset = loader.eProductTestDataset('../images/meta', 'index.csv')
embLoader = DataLoader(embDataset, batch_size=8)


# ### Loop through each index image and get its embedding
# This will allow us to create the dictionary of image embeddings and uuids for similarity comparison later on.

# In[ ]:


embs = {}
hashtable = LSHash(hash_size=50, 
                   input_dim=1002)
with torch.no_grad():
        for i, (uuids, imgs) in tqdm(enumerate(embLoader)):
            imgs = imgs.to(device)
            preds = model(imgs)
           

            #print(preds[][0].sum())
            # Concat level
            preds_concat = torch.concat([torch.argmax(preds[0], dim=1).reshape((8,1)),
                                        torch.argmax(preds[1], dim=1).reshape((8,1)),
                                        #torch.argmax(preds[2], dim=1).reshape(8, 1)], dim=1)
                                         preds[2]], dim=1)
            preds_concat = preds_concat.cpu()
            #if not hashtable:
            #     hashtable = lshashing.LSHRandom(preds_concat[0], hash_len=500)
            
            for uuid in range(len(uuids)):
                hashtable.index(preds_concat[uuid].numpy(), extra_data=uuids[uuid])
            
            if (i+1) % 1000 == 0:
                fname = f'.lshnp/lsh_{i+1}.p'
                with open(fname, 'wb')  as f:
                    pickle.dump(hashtable, f)
                    print(f'Saved {fname}')
                del hashtable
                hashtable = LSHash(20, 1002)
            
            


# ## Pickle Hashtable and save it

# In[ ]:




