from util import get_transaction_entries 
class Node:
    def __init__(self):
        #self.itemset = itemset
        self.children = {}
        self.count = 1
        self.parent = None
        self.link = None            # Link to next node in the header table

class FP:
    # TODO: How to store the node link?
    def __init__(self, source, index):
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
            self.headers[item] = node
        # Insert node at the end of list
        else:
            sent = self.headers[item]
            while sent.link != None:
                sent = sent.link
            sent.link = node


    def fp_recur_insert(self, node, itemset, index):
        # Recursive end
        if index >= len(itemset):
            return
        item = itemset[index]

        if item in node.children:
            node.children[item].count += 1

        else:
            insert = Node()
            insert.parent = node
            node.children[item] = insert
            # TODO: Expand header table
            self.fp_insert_nlink(item, insert)

        self.fp_recur_insert(node.children[item], itemset, index+1)


    def fp_insert(self, itemset):
        self.fp_recur_insert(self.root, itemset, 0)

    # debug print functions
    def _print_tree(self, node):
        print(f'Node with children: {node.children}')
        for key, val in node.children.items():
            self._print_tree(val)
    def _print_table(self):
        for item, node in self.headers.items():
            print(f'{item}: ', end="")
            sent = node
            while sent != None:
                print(f'{sent.count} ', end="")
                sent = sent.link
            print('\n')

    def fp(self):
        L = self._get_one_itemsets()

        for trans in self.fp_next_trans():
            trans.sort(key= lambda i:self.count[i], reverse=True)
            self.fp_insert(trans)
        self._print_tree(self.root)
        self._print_table()
            

