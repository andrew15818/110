import math
import pandas as pd
import numpy as np

from dataclasses import dataclass

class Node:
    def __init__(self, is_leaf:bool=False, label:str=""):
        self.is_leaf = is_leaf
        self.attribute = label
        self.split_point = None
        self.purity = None
        self.parent = None
        self.children = []

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    
class DecisionTree:
    def __init__(self, continuous=True, method='gini'):
        self.continuous = continuous 
        self.root = Node()
        self.method = method
        self.classes = [] 

    # Check if all the classLabels are the same
    def _all_single_class(self, classes) -> bool:
        return len(classes.unique()) == 1
     
    def gini(self, data):
        if len(data) == 0:
            return 1
        pi = 0
        for c in self.classes:
            # Get the count of class items and square
            instances = (data.iloc[:,-1] == c).sum()
            rows = data.shape[0]
            p = instances / rows 
            p = p ** 2
            pi += p
        return 1 - pi

    def purity(self, data: pd.DataFrame, feature_name:str, split_point:float) -> float:
        # TODO: Implement the other selection methods
        if self.method == 'gini':
            lesser = data[data[feature_name] <= split_point]
            greater = data[data[feature_name] > split_point]
            return self.gini(lesser) + self.gini(greater)
            

        
    def _attribute_best_split_cont(self, data:pd.DataFrame, featcol:list) -> (float, float):

        best_purity = 2
        best_split_point = 0
        srt = featcol.sort_values(0,ascending=True)
        for i in range(len(srt)-1):
            n1 = srt.values[i]
            n2 = srt.values[i+1]
            split_point = (n1 + n2) / 2
            
            split_purity = self.purity(data, featcol.name, split_point)
            if split_purity < best_purity:
            
                best_purity = split_purity
                best_split_point = split_point
        return best_purity, best_split_point

    # TODO: Also allow for discrete values
    def _get_best_attribute(self, data: pd.DataFrame) -> (str, float, float):
        best_split_value, best_purity = None, 10000 
        best_attribute = ""
        for attribute in self.features:
            purity, point = self._attribute_best_split_cont(data, data[attribute])
            if purity < best_purity:
                best_purity = purity
                best_split_point = point
                best_attribute = attribute
               
        return best_attribute, best_purity, best_split_point

    def insert(self, data:pd.DataFrame, attributes:list, parent:Node) -> Node:
        #print(f'Inserting item of size {len(data)}')
        column_len = len(data.columns)
        node = Node()
        classes = data.iloc[:,column_len-1]
        
        # All nodes belong to same class
        if self._all_single_class(classes):
            # Create a leaf node with current label
            node.is_leaf = True
            node.attribute = classes.iloc[0]
            return node
        
        # No more attributes to split on
        if len(attributes) == 0:
            # TODO: Maybe index error
            majority = classes.mode()[0]
            node.is_leaf = True
            node.label = majority
            return node

       # TODO: If list is discrete and multi-branching allowed 

        attribute, purity, split_point = self._get_best_attribute(data)
        print(f'purity: {purity}, split point: {split_point}, {attribute}')
        left = data[data[attribute] <= split_point] 
        right = data[data[attribute] > split_point] 
            

        node.attribute = attribute
        node.split_point = split_point
        node.parent = parent
        node.purity = purity
        parent.add_child(node)
        
        if len(left) == 0 or len(right) == 0:
            node.is_leaf = True
            return

        self.insert(left, attributes, node)
        self.insert(right, attributes, node)

    # For debug
    def print_tree(self, node):
        print(f'Node attribute: {node.attribute}\t split_point: {node.split_point}, purity: {node.purity}')
        for child in node.children:
            self.print_tree(child)
        print('Returning')

    # Start the building process
    def run(self, data):
        self.features = data.columns[:-1]
        self.classes = data.iloc[:,-1].unique()
        self.insert(data, data.columns, self.root)
        #self.print_tree(self.root)

    def fit(self, data):
        pass
        
