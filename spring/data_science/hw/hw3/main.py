import os
import glob
import argparse
import math
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

parser = argparse.ArgumentParser(
            usage='%(prog) [OPTIONS]',
            description='Practice regression with missing values.'
        )
parser.add_argument('-d', '--datadir',
        default='data'
)
parser.add_argument('--dataset',
        default='concrete'
)
args = parser.parse_args()

# Remove unnecessary spaces, etc...
# If lines are \n, skip them
def get_rows(filename:str, sep=None):
    with open(filename) as f:
        rows = []
        # Ugly, but works with tabs and spaces, empty lines
        for line in f:
            line = line.strip('\n ,')
            line = line.split(sep) if sep else line.split()
            try:
                line = [float(i) for i in line]
            except ValueError: # Usually means encountered \n
                continue
            if len(line) == 0:
                continue
            rows.append(line)
        return np.array(rows, dtype=np.float64)

# Open file, return full dataset
# Sep is because some files use tabs, others spaces
def get_dataset() -> np.array:
    tabs = ['power', 'energy'] # These files use tabs to separate values
    # All datasets are in their own dir
    for filename in glob.iglob(f'{args.datadir}/*.txt'):
        sep = None
        for tabfile in tabs:
            sep = '\t' if tabfile in filename else sep
        print(filename)
        rows = get_rows(filename, sep=sep)
        yield rows 

def remove_feature_values(features:np.array, ratio=0.3):
    hideNum = int(features.size * ratio)
    print(f'Removing {features.size}*{ratio} = {hideNum}')
    for i in range(hideNum):
        hrow = random.randint(0, features.shape[0]) - 1
        hcol = random.randint(0, features.shape[1]) - 1
        features[hrow][hcol] = math.nan
        print(features[hrow])
    
    


def main():
    missingRatios = [0.1, 0.3, 0.5, 0.7]
    for dataset in get_dataset():

        copy = dataset.copy()
        # Only remove from the features
        features, labels  = copy[:,:-1], copy[:,-1]

        remove_feature_values(features)
        print(features)
        break

if __name__=='__main__':
    main()

