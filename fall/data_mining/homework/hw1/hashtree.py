import hashlib
from collections import defaultdict

# 
class Node:
    def __init__(self, index=0):
        self.buckets = defaultdict(int) # Creates an entry with 0 instead of KeyError if item not inserted yet
        self.children = defaultdict(Node)
        self.cum_support = 0            # Cumulative support of children
        self.index = index              # Index to hash on
        self.max_leaf_nodes = 3         # Max amount of children per node
        self.is_leaf = True

# Used when checking for frequent itemsets
class HashTree:
    def __init__(self): 
        self.root = Node() 

    # Calls the actual insert method
    def insert(self, itemset, support=1):
        self.insert_recursively(self.root, itemset, support)

    # Insert leaf node or split node if too big
    def insert_recursively(self, node, itemset: tuple, support=1, index=0):
        hash_index = self.hash(node, itemset)
        if index == len(itemset):
            node.buckets[itemset] += support
            return 

        if not node.is_leaf:
            self.insert_recursively(node.children[hash_index], itemset, index=node.index+1)
        else:
            # Only the leaf nodes have buckets
            if itemset in node.buckets:
                node.buckets[itemset] += support 
            else:
                node.buckets[itemset] = support

            # Create a new node if too manybuckets
            if len(node.buckets) == node.max_leaf_nodes:
                node.is_leaf = False
                print(node.buckets)
                for old_item, old_support in node.buckets.items():
                    node.cum_support += old_support
                    old_hash = self.hash(node, old_item)
                    node.children[old_hash].index = node.index + 1
                    self.insert_recursively(node.children[old_hash], old_item, old_support, index=node.index+1)
                del node.buckets

    def _print_tree(self, node): 

        for hash_index, child in node.children.items():
            print('Going to next child')
            self._print_tree(child)

        if node.is_leaf:
            print(f'{node.buckets}')

    def hash(self, node, item):
        # Hash based on the digit of the number
        # To avoid index error
        check_digit = node.index % len(item)
        return int(item[check_digit]) % node.max_leaf_nodes

