import os
import argparse
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# TODO: Load the csvs
# Normalize the features
# Remove the percentage from the features
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

# Open file, return full dataset
def get_dataset() -> pd.DataFrame:
    pass
def main():
    pass

if __name__=='__main__':
    main()

