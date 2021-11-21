from sklearn import tree
from sklearn.datasets import load_iris
import argparse
from matplotlib import pyplot as plt
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
    return algo

def user_test(algo, test_data:pd.DataFrame) -> list:
    classes = algo.test(test_data) 
    return classes

def compare():
    dt = tree.DecisionTreeClassifier()
    iris = load_iris()
    dt = dt.fit(iris.data, iris.target)
    fig = plt.figure(figsize=(25,20))
    _ = tree.plot_tree(dt, 
            feature_names=iris.feature_names,
            class_names=iris.target_names,
            filled=True)
    #plt.savefig("Figure-1.png")
    return dt
def main():
    # Training
    args = get_args() 
    data = get_data(args.file)
    algo = run(args.algorithm, data)

    # Testing 
    test_data = get_data('data/iris_test.csv')
    model = compare()
    model_classes = model.predict(test_data.to_numpy()[:,:-1])
    user_classes = user_test(algo, test_data)
    print(f'models preds: {model_classes} len={len(model_classes)}')
    print(f'Ours: {user_classes} len={len(user_classes)}')
    
if __name__=='__main__':
    main()
