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
        self.label= ""

    def add_child(self, node):
        node.parent = self
        self.children.append(node)
    # Decided to just do binary tree at the last minute :(
    def get_left(self):
        return self.children[0]
    def get_right(self):
        return self.children[1]
    
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
            x = (len(lesser)* self.gini(lesser) + len(greater) * self.gini(greater)) / len(data)
            return x
            

        
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
                #print(f'\t\tConsidering {split_purity}')
                best_purity = split_purity
                best_split_point = split_point
        return best_purity, best_split_point

    # TODO: Also allow for discrete values
    def _get_best_attribute(self, data: pd.DataFrame) -> (str, float, float):
        best_split_point, best_purity = None, 10000 
        best_attribute = ""
        gini_data = self.gini(data)

        for attribute in self.features:
            purity, point = self._attribute_best_split_cont(data, data[attribute])
           
            imp_reduction =  purity#gini_data - purity
            if imp_reduction < best_purity:
                #print(f'\tNew best impurity: {imp_reduction}')
                best_purity = imp_reduction
                best_split_point = point
                best_attribute = attribute
            #print(f'\t{gini_data}, {purity}, current best {best_purity}')    
        return best_attribute, best_purity, best_split_point

    def insert(self, data:pd.DataFrame) -> Node:
        '''
        TODO: 
        1. Check if the data is empty or purity is zero.
        2. Find the best feature to split on.
        3. Split the node into left and right.
        4. Recurse on two halves.
        '''
        node = Node()

        #if data.shape[0] == 0:
        #    return None

        data_purity = self.gini(data) 
        if data_purity == 0:
            node.is_leaf = True 
            # Get the last label
            node.label = data.iloc[0].iloc[-1]
            return node

        attribute, purity, split = self._get_best_attribute(data) 
        print(f'Chose {attribute}')
        if purity <= 0:
            node.is_leaf = True
            node.label = data.iloc[0].iloc[-1]
            return node
        node.attribute = attribute
        node.purity = purity
        node.split_point = split

       
        left = data[data[attribute] <= split]
        right = data[data[attribute] > split]
        #print(f'Left: {len(left)} Right: {len(right)}')
        if left.shape[0] > 0:
            node.add_child(self.insert(left))
        if right.shape[0] > 0:
            node.add_child(self.insert(right))

        return node

    # For debug
    def print_tree(self, node):
        if node.is_leaf:
            print(f'Class: {node.label} ', end="")
        else:
            print(f'Attribute: {node.attribute} ', end="")

        print(f'split_point: {node.split_point}, purity: {node.purity}')
        for child in node.children:
            self.print_tree(child)
        print('Returning\n')

    # Start the building process
    def run(self, data):
        self.features = data.columns[:-1]
        self.classes = data.iloc[:,-1].unique()
        self.root = self.insert(data)
        #self.print_tree(self.root)

    def get_class(self, row: pd.Series, node=None) -> str:
        # For the first assignment
        node = self.root if not node else node

        if node.is_leaf:
            return node.label
        attr = node.attribute
        #print(f'Checking {attr} {row[attr]} <= {node.split_point}')
        if row[attr] <= node.split_point:
            left = node.get_left()
            return self.get_class(row, left)
        else:
            right = node.get_right()
            return self.get_class(row, right)

    def test(self, data: pd.DataFrame) -> list:
        # Get the class assignment for every element
        classes = []
        for index, row in data.iterrows():
            classes.append(self.get_class(row))
            
        return classes
