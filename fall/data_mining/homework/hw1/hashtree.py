from dataclasses import dataclass

class Node:
    def __init__(self, key):
        self. key = key
        self.right, self.left = None, None
        self.child_count = 0

class HashTree:
    def __init__(self): 
        self.root = None

