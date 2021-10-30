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
    def insert(self, itemset, support=0):
        self.insert_recursively(self.root, itemset, support)

    # Insert leaf node or split node if too big
    def insert_recursively(self, node, itemset: tuple, support=0, index=0):
       
        if index == len(itemset):
            node.buckets[itemset]+= support
            node.cum_support += support 
            return 
        hash_index = self.hash(index, itemset)
        if not node.is_leaf:
            self.insert_recursively(node.children[hash_index], itemset, index=index+1)
        else:
            # Only the leaf nodes have buckets
            #print(f'\tChecking if {itemset} in {node.buckets.keys()}')
            if itemset in node.buckets.keys():
                node.buckets[itemset] += support 
                node.cum_support += support
            else:
                #print(f"Adding {itemset} with suppor,t {support}")
                node.buckets[itemset] = support

            # Create a new node if too manybuckets
            if len(node.buckets) == node.max_leaf_nodes:
                node.is_leaf = False 
                #print(node.buckets)
                for old_item, old_support in node.buckets.items():
                    node.cum_support += old_support
                    old_hash = self.hash(index , old_item)
                    node.children[old_hash].index = node.index + 1
                    self.insert_recursively(node.children[old_hash], old_item, old_support, index=index+1)
                #del node.buckets

    def _print_tree(self, node): 

        for hash_index, child in node.children.items():
            #print(f'\t Going to child {hash_index}, support: {node.cum_support}')
            self._print_tree(child)

        if node.is_leaf:
            print(f'{node.buckets}, support: {node.cum_support}')
        #print('\tReturning')

    def hash(self, index, item, max_leaf_nodes=3):
        # Hash based on the digit of the number
        # To avoid index error
        answer = int(item[index % (len(item))]) % max_leaf_nodes
        return answer 

    def add_subset_support(self, node, itemset, index=0):
        if node.is_leaf:
            if itemset in node.buckets:
                node.buckets[itemset] += 1
                #print(f'\tSupport for {itemset}: {node.buckets[itemset]}')
        elif len(itemset) == index:
            node.buckets[itemset] += 1
        else:
            hsh = self.hash(index , itemset)
            self.add_subset_support(node.children[hsh], itemset, index+1)
                
        
    def get_frequent_itemsets(self, node, frequent_items, min_sup):
        if node.is_leaf:
            for item, sup in node.buckets.items():
                if int(sup) >= min_sup:
                    frequent_items.append((item, sup))
        else:
            for idx in node.children:
                self.get_frequent_itemsets(node.children[idx], frequent_items, min_sup)


