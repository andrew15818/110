import os
import torch
import loader
import pickle
import PIL

import matplotlib.pyplot as plt
import torch.nn as nn
from lshash.lshash import LSHash
from torch.utils.data import DataLoader
from model.resnet50 import ResNet50
from tqdm import tqdm

IMG_DIR = '../images'
INDEX_IMG = 'eval/index'
CSV_DIR = '../images/meta'
LSH_PATH = './.lshnp'
CSV_PATH = 'query_part2.csv'
CHKPT = './.checkpoints/model.pt'

out_file = 'out.csv'
batch_size = 1
device = torch.device("cuda:0" if torch.cuda.is_available() else 'cpu')

dataset = loader.eProductTestDataset(
                '../images/meta', 'query_part2.csv'
            )
dataloader = DataLoader(dataset, batch_size=batch_size)

checkpoint = torch.load(CHKPT)
model = ResNet50(num_classes=[16, 77, 1000]).to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

def show_image(path):
    plt.imshow(PIL.Image.open(path))
    plt.show()

def write_to_file(img_uuid, sim_imgs, fp):
    fp.write(f"{img_uuid},{' '.join(sim_imgs)}\n")
    
    print(f'\t Wrote to file.')
# Scan through all pickled files?
def get_closest_images(emb, min_dist=0.1):
    sim_imgs = [] # UUID of similar images
    
    for file in os.listdir(LSH_PATH):
        f = open(os.path.join(LSH_PATH, file), 'rb')
        lsh = pickle.load(f)
        res =lsh.query(emb, num_results=1, distance_func='cosine')
        for item in res:
            if item[1] < min_dist:
                imgname = item[0][1]
                print(f'{imgname}: {item[1]}')
                sim_imgs.append((imgname, item[1]))
                #show_image(os.path.join(f'../images/eval/index/{imgname}.JPEG'))                
        #print('\n')
    return sim_imgs

# Get embeddings
with torch.no_grad():
    #with open(out_file, 'w') as f:
    for i, (uuid, img) in tqdm(enumerate(dataloader)):
        # Check specific embedding
        if not uuid[0] == 'HqHtsrdBnGZmRomu':
            continue
        print("Found HqHtsrdBnGZmRomu")
        img = img.to(device)
        preds = model(img)
        preds_concat = torch.concat([torch.argmax(preds[0], dim=1).reshape((1, 1)),
                                    torch.argmax(preds[1], dim=1).reshape((1,1)),
                                    preds[2]], dim=1)
        preds_concat = preds_concat.cpu()
        sims = get_closest_images(preds_concat.reshape(1002,))
        print(sims)
        print(sims.sort(key=lambda y: y[1]))
        #
            #write_to_file(uuid[0], sims, f)

            #break
