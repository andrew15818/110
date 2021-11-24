import pandas as pd
import argparse

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from matplotlib import pyplot as plt

from decisiontree import DecisionTree 
from naivebayes import NaiveBayes


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
            help='Choose algorithm to use. Can use decisiontree, naivebayes, knn'
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

def compare():
    algo = None
    if args.algo.lower()  == 'decision_tree':
        algo = tree.DecisionTreeClassifier()
        iris = load_iris()
        dt = algo.fit(iris.data, iris.target)
        fig = plt.figure(figsize=(25,20))
        _ = tree.plot_tree(dt, 
                feature_names=iris.feature_names,
                class_names=iris.target_names,
                filled=True)
        #plt.savefig("Figure-1.png")
    elif args.algo.lower() == 'naivebayes':
        algo = GaussianNB()
        X, Y = load_iris(return_X_y=True)
        x_train, y_train, x_test, y_test = train_test_split(X, Y) 
        preds = algo.fit(x_train, y_train).predict(x_test)

    return algo 
def main():
    # Training
    args = get_args() 
    data = get_data(args.file)
    x_train, y_train, x_test, y_test = train_test_split(data, )
    algo = run(args.algorithm, data)
    '''
    # Testing 
    test_data = get_data('data/iris_test.csv')
    model = compare()
    model_classes = model.predict(test_data.to_numpy()[:,:-1])
    user_classes = user_test(algo, test_data)
    print(f'models preds: {model_classes} len={len(model_classes)}')
    print(f'Ours: {user_classes} len={len(user_classes)}')
    '''
    
if __name__=='__main__':
    main()
