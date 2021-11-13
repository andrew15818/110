
import argparse
import pandas as pd

from decisiontree import DecisionTree 

def get_args():
    parser = argparse.ArgumentParser(
             usage='(prog) [OPTION]',             
             description='classify the data points based on the data in a csv file.'
            ) 
    parser.add_argument(
            '-f', '--file',
            type=str, default="data/iris_dataset.csv"
            )
    parser.add_argument(
            '-a', '--algorithm',
            type=str, default='decisiontree',
            help='choose algorithm to use. Can use decisiontree, bayes, knn'
            )
    parser.add_argument(
            '-c', '--continuous',
            type=bool, default=True,
            help='continous data or discrete.'
            )
    return parser.parse_args()

# Get data from csv
def get_data(filename):
    file =  pd.read_csv(filename)
    return file

def run(algorithm, data):
    algoName = algorithm.lower()
    algo = None
    if algoName == 'decisiontree':
        algo = DecisionTree()
    algo.run(data)

def main():
    args = get_args() 
    data = get_data(args.file)
    run(args.algorithm, data)
    

if __name__=='__main__':
    main()
