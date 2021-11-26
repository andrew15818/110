import pandas as pd
import argparse

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from matplotlib import pyplot as plt

from decisiontree import DecisionTree 
from naivebayes import NaiveBayes
from model import NeuralClassifier


def get_args():
    parser = argparse.ArgumentParser(
             usage='(prog) [OPTION]',             
             description='classify the data points based on the data in a csv file.'
            ) 
    parser.add_argument(
            '-f', '--file',
            type=str, default="data/iris_dataset.csv",
            help='Dataset, last column should have the class label.'
            )
    parser.add_argument(
            '-a', '--algorithm',
            type=str, default='decisiontree',
            help='Choose algorithm to use. Can use decisiontree, naivebayes, neural.'
            )
    parser.add_argument(
            '-c', '--continuous',
            type=bool, default=True,
            help='Continous data or discrete.'
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
    # Bayes doesn't need training 
    elif algoName == 'naivebayes':
        algo = NaiveBayes(labels=data.iloc[:,-1].unique())

    algo.run(data) 
    return algo

def user_test(algo, test_data:pd.DataFrame) -> list:
    classes = algo.test(test_data) 
    return classes

def compare(algoname, train):
    algo = None
    x_train = train.iloc[:,:-1]
    y_train = train.iloc[:,-1] 
    if  algoname  == 'decisiontree':
        algo = tree.DecisionTreeClassifier()
        iris = load_iris()

        dt = algo.fit(x_train, y_train)
        #plt.savefig("Figure-1.png")
    elif algoname  == 'naivebayes':
        algo = GaussianNB()
        algo.fit(x_train, y_train) 
    return algo 
def main():
    # Training
    args = get_args() 
    data = get_data(args.file)
    X, y = train_test_split(
                data, 
                test_size=0.2)
    print(y.iloc[:,:-1])
    algo = run(args.algorithm, X)
    ours = algo.run(y)
    sklearn_model = compare(args.algorithm, X)

    # Testing 
    preds = sklearn_model.predict(y.iloc[:,:-1])
    print(f'Sklearn accuracy: {(y.iloc[:,-1] == preds).sum() / y.shape[0]}')
    print(f'Ours: {(y.iloc[:,-1] == ours).sum() / y.shape[0]}')
if __name__=='__main__':
    main()
