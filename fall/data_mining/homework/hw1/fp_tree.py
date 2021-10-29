import itertools

from util import get_transaction_entries 

class Node:
    def __init__(self):
        self.item = None
        self.children = {}
        self.count = 1
        self.parent = None
        self.link = None            # Link to next node in the header table

class FP:
    def __init__(self, source, index, inputLists=None):
        self.headers = {}           # Header table for each node
        self.source = source
        self.index = index          # Index on which to split the transaction string
        self.count = {}             # item, count pair used for sorting
        self.root = Node()
        self.item = None

    def fp_next_trans(self):
        for row in open(self.source, 'r'):
            yield get_transaction_entries(row, self.index)

    def _get_one_itemsets(self):
        #count = {}
        # Get support count of each item
        for trans in self.fp_next_trans():
            for item in trans:
                self.count[item] = 1 if not item in self.count else self.count[item] + 1

        L = [tuple((key, val)) for key, val in self.count.items()]
        L.sort(key= lambda i: i[1], reverse=True)

        return L
    # Expand the header table with reference to node
    def fp_insert_nlink(self, item, node):
        if item not in self.headers:
            self.headers[item] = [node] 
        # Insert node at the end of list
        else:
            self.headers[item].append(node)

    def fp_recur_insert(self, node, itemset, index):
        # Recursive end
        if index >= len(itemset):
            return
        item = itemset[index]

        if item in node.children:
            node.children[item].count += 1

        else:
            insert = Node()
            insert.item = item
            insert.parent = node
            node.children[item] = insert
            self.fp_insert_nlink(item, insert)

        self.fp_recur_insert(node.children[item], itemset, index+1)


    def fp_insert(self, itemset):
        self.fp_recur_insert(self.root, itemset, 0)

    # Loop through all the branches in path
    def subsets(self):
        items = self.headers.keys()
        subs = []
        for i in range(len(items) + 1):
             subs.append(tuple(itertools.combinations(items, i)))
        return subs

    def has_single_path(self, node):
        if not node.children:
            return True
        if len(node.children) > 1:
            return False
        else:
            child = list(node.children)[0]
            return True and self.has_single_path(node.children[child])

    def comb_itemsets(self, prefixes):
        itemsets = []
        suffix = self.item
        if not suffix:
            return None
        for prefix in prefixes:
            for iset in prefix:
                itemsets.append(tuple((iset) + tuple(suffix)))
        return itemsets

    def get_frequent_items(self, support):
        # 1. If there is single path, create the subsets along the path
        #print(f'Analyzing frequent items of {item}')
        if self.has_single_path(self.root):
            # Generate subsets along this path
            a = self.comb_itemsets(self.subsets())
            return a
        else:
            # Mine the different subtrees and add them together 
            s = (self.mine_subtrees(support))
            return s
    def zip(self, patterns):
        suffix = self.item
        if not suffix:
            return
        new_patterns = {}
        for pattern in patterns:
            new_patterns[tuple(sorted(pattern + tuple(suffix)))]  = patterns[pattern]

        return new_patterns
    def mine_subtrees(self, support): 
        # Go through all the frequent items and their branches
        # Add support count for each item in the branches
        patterns = {} # Patterns from the different branches
        for item, link in self.headers.items():
            path = []
            for node in link:
                freq = node.count
                #print(freq)
                sent = node.parent
                # Conditional branches for each node
                branch = []
                while sent.parent != None:
                    branch.append(sent.item)
                    sent = sent.parent
                # To preserve counts in conditional tree?
                for f in range(freq):
                    path.append(branch)
            cond_tree = FP('', '')
            for p in path:
                cond_tree.fp_insert(list(reversed(p)))
            cond_tree.prune(support)
            cond_tree.item = item
            sub_patterns = cond_tree.get_frequent_items(support)
            #print(f'sub_patterns: {sub_patterns}')
            for pattern in sub_patterns:
                if pattern in patterns:
                    patterns[pattern] += sub_patterns[pattern]
                else:
                    patterns[pattern] = 0
            #print(f'Patterns: {patterns}')
        return patterns 
            


    # Remove the itemsets with too low support
    def prune(self, support):
        for value, nlist in self.headers.items():
            currsup = 0 
            for node in nlist:
                currsup += node.count
            if currsup < support: 
                d = self.headers.copy()
                del d[value]
                self.headers = d


    # debug print functions
    def _print_tree(self, node):
        print(f'Node with item {node.item} count {node.count}, children: {node.children}')
        for key, val in node.children.items():
            self._print_tree(val)

    # Deal with awkward formatiing
    def _print_frequent_items(self, frequent_items):
        pass
    def _print_table(self):
        for item, nlist in self.headers.items():
            print(f'{item}: ', end="")
            for node in nlist:
                print(f'(item={node.item}, parent={node.parent.item}) ', end="")
            print('\n')

    def fp(self, support):
        L = self._get_one_itemsets()

        for trans in self.fp_next_trans():
            trans.sort(key= lambda i:self.count[i], reverse=True)
            self.fp_insert(trans)
        fi = self.get_frequent_items(support)
        #self._print_tree(self.root)
        #self._print_table()
        print(f'FINALLY: {fi}')
         

