import hashlib
from collections import defaultdict

# 
class Node:
    def __init__(self):
        self.buckets = defaultdict(int) # Creates an entry with 0 instead of KeyError if item not inserted yet
        self.children = defaultdict(Node)
        self.cum_hash = 0 # TODO: necessary?
        self.index = 0      # Index to hash on
        self.max_leaf_nodes = 3 # Maybe need to extend it
        self.is_leaf = True

# Used when checking for frequent itemsets
class HashTree:
    def __init__(self): 
        self.root = Node() 

    # Calls the actual insert method
    def insert(self, itemset, support):
        self.insert_recursively(self.root, itemset, support)

    # Insert leaf node or split node if too big
    def insert_recursively(self, node, itemset: list, support=0):
        #TODO: Change the references to node.children from node.buckets
        # where appropriate.
        print(f'Inserting {itemset}')
        hash_index = self.hash(node, itemset)
        if not node.is_leaf:
            self.insert_recursively(node.buckets[hash_index], itemset)
            return 

        if len(node.buckets) == node.max_leaf_nodes:
            # Split the node
            node.is_leaf = False 
            new_node = Node()
            new_node.index = node.index + 1
            print(node.buckets)
            new_itemset = node.buckets[hash_index].items
            print(f'Splitting dataset into: {new_itemset}')
            for item, support in new_itemset:
                self.insert_recursively(new_node, item, support)

            node.buckets[hash_index] = new_node
        else:
            # Tuples can serve as keys in dict
            itemset = tuple(itemset)
            node.buckets[itemset] += 1  
            print(node.buckets)
            
            

        
    def hash(self, node, item):
        # Hash based on the digit of the number
        # To avoid index error
        check_digit = node.index % len(item)
        return int(item[check_digit]) % node.max_leaf_nodes

