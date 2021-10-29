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
            print(f'Child {insert.item} parent {insert.parent.item}')

        self.fp_recur_insert(node.children[item], itemset, index+1)


    def fp_insert(self, itemset):
        self.fp_recur_insert(self.root, itemset, 0)

    # Get length 2-len(prefix) itemsets, suffix added to end
    # TODO: Change the format of the data for more easy printing
    def subsets(self, prefix, suffix): 
        subs = []
        for i in range(1, len(prefix)+1):
            subi = itertools.combinations(prefix, i) 
            #print(f'{[[j, suffix] for j in subi]}')
            subs.append([[j, suffix] for j in subi])
        return subs
        
    def has_single_path(self, node):
        print(node.item)
        if len(node.children) > 1:
            return False
        else:
            return True and self.has_single_path(node.children[0])

    def get_frequent_items(self, support):
        # 1. If there is single path, create the subsets along the path
        #print(f'Path for {self.root.item}:')
        if self.has_single_path(self.root):
            # Generate subsets along this path
            pass
        else:
            # Mine the different subtrees and add them together 
            self.mine_subtrees(support)
        # 2. For each item in the tree header, generate cond pattern, tree
        # 3. If the tree is not None, call recursively
    def mine_subtrees(self, support): 
        # Go through all the frequent items and their branches
        # Add support count for each item in the branches
        
        for item, link in self.headers.items():
            path = []
            for node in link:
                freq = node.count
                print(freq)
                #print(f'path for {item}: ')
                sent = node.parent
                # Conditional branches for each node
                branch = []
                while sent.parent != None:
                    branch.append(sent.item)
                    sent = sent.parent
                # To preserve counts in conditional tree?
                for fpap in range(freq):
                    path.append(branch)

            # TODO: Generate the conditional fp-tree
            print(f'Tree for {item}')
            print(path)
            cond_tree = FP('', '')
            for p in path:
                cond_tree.fp_insert(list(reversed(p)))
            cond_tree._print_tree(cond_tree.root)
            print('\n')



    # debug print functions
    def _print_tree(self, node):
        print(f'Node with item {node.item} count {node.count}, children: {node.children}')
        for key, val in node.children.items():
            self._print_tree(val)

    # Deal with awkward formatiing
    def _print_frequent_items(self, frequent_items):
        print(frequent_items)
        for item in frequent_items:
            if item == None:
                continue
            for ri in item:
                for rule in ri:
                    for j in range(len(rule)-1):
                        for p in rule[j]:
                            print(f'{p[0]}, ', end="")
                print(f' => {rule[-1]}')
                
            #print(item)
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
        self._print_tree(self.root)
        self._print_table()
         

