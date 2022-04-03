import os
import glob
import argparse
import math
import random
import missingno as msno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import methods
TRIAL_NO = 5 # Number of runs per missing ratio

METHODS = ['mean',
            #    'knn',
            #    'mice',
                #'gain',
                #'grape',
                #'mean-mi',
                #'knn-mi',
                #'mice-mi'
            ]
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


# Call the appropriate value from methods module
def impute_values(features, method='mean'):
    imputed = None
    method = method.lower()
    # TODO: delegate function call to function in methods file?
    if method == 'mean':
        imputed = methods.mean_imp(features)
    elif method == 'knn':
        imputed = methods.knn(features)
    elif method == 'mice':
        imputed = methods.mice(features)
    elif '-mi' in method:
        imputed = methods.missing_indicator(features, method)
    elif method == 'gain':
        imputed = methods.gain(features)
    elif method == 'grape':
        imputed = methods.grape(features)

    if imputed is None:
        print('Unrecognized imputing method!')


    return imputed 
def mae(preds:np.array, labels:np.array):
    return abs(preds - labels) / preds.shape[0]

# Open file, return full dataset
# Some files are separated by spaces, others w/ tabs
def get_dataset() -> np.array:
    tabs = ['power', 'energy'] # These files use tabs to separate values
    # All datasets are in their own dir
    for filename in glob.iglob(f'{args.datadir}/*.txt'):
        sep = None
        for tabfile in tabs:
            sep = '\t' if tabfile in filename else sep
        print(filename)
        rows = get_rows(filename, sep=sep)
        yield rows, filename


def remove_feature_values(features:np.array, ratio=0.3):
    hideNum = int(features.size * ratio)
    #print(f'Removing {features.size}*{ratio} = {hideNum}')
    for i in range(hideNum):
        hrow = random.randint(0, features.shape[0]) - 1
        hcol = random.randint(0, features.shape[1]) - 1
        features[hrow][hcol] = np.nan
    
    
def preprocess(features, labels):
    x_train, x_test, y_train, y_test = \
            train_test_split(features, labels, test_size=0.3)
    scaler = MinMaxScaler()
    scaler.fit_transform(x_train, y_train) 
    return x_train, x_test, y_train, y_test


def plot_missing_values(features:np.array):
    msno.matrix(pd.DataFrame(features))
    plt.show()

def plot_error(errors,  ratios=[0.1, 0.3, 0.5, 0.7]):
    print(errors)
    fig, axis = plt.subplots(3, 3)
    for idx, file in enumerate(errors):
        plt.subplot(3, 3, idx+1)
        # TODO: Ugly way of getting filename
        plt.title(file.split('/')[-1])
        fileErrors = errors[file]
        for method in fileErrors:
            plt.plot(ratios, fileErrors[method], label=method)
        plt.legend()
    plt.show()


    
def main():
    missingRatios = [0.1, 0.3, 0.5, 0.7]
    plot = None
    total_errors = {}
    for dataset, filename in get_dataset():
        total_errors[filename] = {}
        for imp_method in METHODS:
            total_errors[filename][imp_method] = []

            for ratio in missingRatios:
                ratio_error = 0
                for i in range(5):

                    copy = dataset.copy()
                    # Only remove from the features
                    features, labels  = copy[:,:-1], copy[:,-1]

                    remove_feature_values(features, ratio)
                    x_train, x_test, y_train, y_test = preprocess(features, labels)

                    # Change imputation methods
                    imputed_train = impute_values(x_train, imp_method)
                    imputed_test = impute_values(x_test, imp_method) 

                    # Train a linear regression model
                    model = LinearRegression()
                    model.fit(imputed_train, y_train)

                    # Get our predictions with imputed data
                    preds = model.predict(imputed_test)
                    error = mae(preds, y_test)
                    print(f'[{imp_method}] -- Test {i+1}: Missing data: {ratio}: \
                        error: {error.mean()}')

                    ratio_error += error.mean()

                total_errors[filename][imp_method].append(ratio_error / TRIAL_NO)

            #break # debug
        #break
    #print(total_errors)
    plot_error(total_errors, missingRatios)

if __name__=='__main__':
    main()

