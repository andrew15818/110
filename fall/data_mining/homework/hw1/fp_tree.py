from util import get_transaction_entries 
class Node:
    def __init__(self, itemset):
        self.itemset = itemset
        self.children = {}

class FP:
    # TODO: How to store the node link?
    def __init__(self, source, index):
        self.header = {}
        self.source = source
        self.index = 1          # Index on which to split the transaction string
        self.count = {}         # item, count pair used for sorting
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

    def fp(self):
        L = self._get_one_itemsets()

        for trans in self.fp_next_trans():
            trans.sort(key= lambda i:self.count[i], reverse=True)
            

