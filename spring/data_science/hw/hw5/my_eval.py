import argparse
import torch
import numpy as np
from torch.utils.data import DataLoader
from backbones import get_model 

from dataset import LFWEvalDataset
import matplotlib.pyplot as plt

# Overall process
# 1. Use dataloader
# 2. Use cosine similarity b/w embeddings as "matching"
# 3. Calculate metrics such as acc, recall, precision, etc...

def get_args():
    parser = argparse.ArgumentParser(description="Andres Ponce\'s LFW verification script.")
    parser.add_argument('--model-name', type=str, help="name of architecture to use.")
    parser.add_argument('--model-path', type=str, help="path to model (e.g. model.pt) ")
    parser.add_argument('--data-dir', type=str, help="path to lfw dataset.")
    parser.add_argument('--label-file', type=str, help='path to the img pairs.')
    return parser.parse_args()
    
# These should be vectors
def cosine_dist(emb1, emb2):
    return 1 - (np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))

def roc(items):
    num_threshs = 50 
    thresholds = np.linspace(0, 1.0, num_threshs, endpoint=False)
    fn = np.zeros(num_threshs)
    tp = np.zeros(num_threshs)
    fp = np.zeros(num_threshs)
    tn = np.zeros(num_threshs)
    acc = np.zeros(num_threshs)
    for item in items:
        dist = item[0]
        areSame = item[1]
        for i in range(num_threshs):
            if areSame:
                if dist < thresholds[i]:
                    tp[i] += 1
                    acc[i] += 1
                else:
                    fn[i] += 1
                 
            elif not areSame:
                if dist < thresholds[i]:
                    fp[i] += 1
                else:
                    acc[i] += 1
                    tn[i] += 1
        
    print(f'fn:{fn}, tp:{tp} tn:{tn} fp: {fp}')
    print(f'Accuracy distinguishing faces: {acc / len(items)}')
    recall = (tp / (tp + fn+.1))
    fpr = (fp / (tn + fp+.1))
    print(f'Recall: {recall}, fpr: {fpr}')
    return tp, tn, fp, fn

def print_preds(preds):          
    avg = 0
    pavg = 0
    pcount = 0
    count = 0
    for pred in preds:
        dist = pred[0]
        match = pred[1]
        if not match:
            count += 1
            avg += dist
        else:
            pavg += dist
            pcount += 1
            
    print(f'Negatives avg: {avg / count} positives avg: {pavg/pcount}')
def plot(tp, tn, fp, fn, model_name):
    # PR Curve
    plt.figure(1)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp +.001)
    plt.title(model_name)
    plt.xticks(np.arange(0, 1.1, .1))
    plt.yticks(np.arange(0, 1.1, .1))
    plt.plot(recall, precision)
    plt.xlabel('recall')
    plt.ylabel('precision')
    
    plt.savefig(f'figs/{model_name}_pr.png')
    
    # ROC curve
    fpr = fp / (fp + tn)
    plt.figure(2)
    plt.xticks(np.arange(0, 1.1, .1))
    plt.yticks(np.arange(0, 1.1, .1))
    plt.plot(fpr, recall)
    plt.title('TPR(recall) vs. FPR ')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.savefig(f'figs/{model_name}_roc.png')
    
    
    
if __name__=='__main__':
    args = get_args()
    device = torch.device('cuda:1')
    model = get_model(args.model_name)
    model.load_state_dict(torch.load(args.model_path))
    model.to(device)
    
    model.eval()
    
    dataloader = DataLoader(LFWEvalDataset(args.label_file, args.data_dir), batch_size=32)
    acc, rec, prec = 0, 0, 0
    with torch.no_grad():
        preds = []
        for i, (im1, im2, isSame) in enumerate(dataloader):
            im1 = im1.type(torch.FloatTensor)
            im2 = im2.type(torch.FloatTensor)
            emb1 = model(im1.to(device))
            emb2 = model(im2.to(device))
            emb1 = torch.nn.functional.normalize(emb1, dim=-1).cpu()
            emb2 = torch.nn.functional.normalize(emb2, dim=-1).cpu()
            for j in range(emb1.shape[0]):
                preds.append([cosine_dist(emb1[j], emb2[j]), isSame[j].item()])
        print_preds(preds)
        tp, tn, fp, fn = roc(preds)
        plot(tp, tn, fp, fn, args.model_path.split('/')[0])
