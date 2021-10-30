import argparse
import itertools
import copy
# For profiling
import resource
import time 

from util import get_transaction_entries
from hashtree import Node, HashTree
from fp_tree import FP

def parseArgs():
    parser = argparse.ArgumentParser(
        usage='%(prog) [OPTION]',
        description='Given a csv or text-file with columns, find common itemsets.'
    )
    parser.add_argument(
        '-f', '--file',
        default='out.data'
    )
    parser.add_argument(
        '--dataIndex',
        type=int, default=1
    )
    parser.add_argument(
        '--support', '-s',
        type=float, default=2,
        #description='Support needed to generate frequent itemsets.'
    )
    parser.add_argument(
        '--confidence', '-c',
        type=float, default=0.8,
        #description='Confidence needed for generating association rules.'
    )
    parser.add_argument(
        '--algorithm', '-a',
        default='apriori'
    )
    args = parser.parse_args()
    return args 

def get_dataset(filename):
    parsed = []
    for trans in open(filename, 'r'):
        parsed.append(get_transaction_entries(trans))
    return parsed

# Get the 1-frequent itemsets
def gen_1_itemsets(dataset):

    min_support = args.support
    # Can we use a list instead to maintain lexi ordering?
    candidates = {}
    cnd = [0] * len(dataset)
    print(f"Minimum support is {min_support}")

    for trans_items in dataset:
        #trans_items = get_transaction_entries(transaction)
        for item in trans_items:
            # keep count
            candidates[item] = 0 if item not in candidates else candidates[item] + 1
    # Get only the candidates with high enough min_support
    # Loop to maintain lexi ordering needed later, bit slower tho...
    L1 = [(tuple(str(i)), candidates[str(i)])for i in range(1, len(dataset)) if ((str(i) in candidates) and (candidates[str(i)] > min_support))]
    return L1

# Check if the first k-2 items are similar 
def share_common_prefix(l1, l2):
    # Why are there different dims?
    if len(l1) != len(l2):
        return False

    for i in range(len(l1)-2):
        if l1[i] != l2[i]:
            return False 
    return True 

# Insert all candidates into tree and return tree
def gen_hash_tree(candidates):
    htree = HashTree()
    for candidate in candidates:
        htree.insert(tuple(candidate))
    return htree
# Generate all the candidate itemsets
def gen_candidate_itemsets(LK_minus_one: list((tuple, int))):

    candidates = []
    for l1 in LK_minus_one:
        for l2 in LK_minus_one:
            # Possible candidate
            if share_common_prefix(l1[0], l2[0]) and (l1[0][-1] < l2[0][-1]):
                c =  [i for i in l1[0]]
                c.append(l2[0][-1])
                #print(f"Inserting {c}")
                candidates.append(c)

    return candidates

# Return all k-subsets of a transaciton
def gen_k_subsets(transaction: tuple, k:int) -> list:
    return itertools.combinations(transaction, k)

# Return the frequent itemset and support count
def get_frequent_itemsets(dataset, htree, k=2, min_sup=1) -> list((tuple, int)):
    for transaction in dataset:
        # 1. Generate k-length subsets
        subsets = gen_k_subsets(tuple(transaction), k) 
        for subset in subsets:
            # 2. Add support for each subset
            htree.add_subset_support(htree.root, subset, index=0)
    # 3. Return those with min_support
    frequent_items = []
    # TODO: Change the min sup
    htree.get_frequent_itemsets(htree.root, frequent_items, min_sup)
    return frequent_items

def gen_association_rules(frequent_itemsets, min_conf=0.7)->list(tuple()):
    # Turn the fk into dictionary for quick access to (fk - h)
    support = {}
    for item in frequent_itemsets:
        support[item[0]] = item[1]
    rules = []
    for fk in frequent_itemsets:
        fk0 = fk[0]
        m = 1
        k = len(fk0)
        
        # 1. Get the 1-itemset of frequent_itemsets
        Hm = itertools.combinations(fk0, m)
        while m <= k:
            #print(f'Finding RHS of {m}')
            if k > (m ):
                Hm1 = itertools.combinations(Hm, m)
                for h in Hm1:
                    fk_comp = [i for i in fk0 if tuple(i) not in h]
                    # Concatenate h into a single tuple
                    h = sum((h),())
                    # If keyerror, one subset was not frequent
                    try:
                        conf = support[fk0] / support[tuple(fk_comp)]
                    except KeyError:
                        print(f'Either {fk0} or {fk_comp} KeyError')
                        continue

                    #print(f'Rule: {fk_comp} => {tuple(h)}: {conf}')
                    if conf >= min_conf:
                        rules.append((fk_comp, h, conf))
            m += 1
    return rules
def apriori(dataset):
    L1 = gen_1_itemsets(dataset)
    LK_minus_one = L1
    min_support = args.support
    k=2 
    frequent = []
    while LK_minus_one:
        frequent.extend(LK_minus_one)
        CK = gen_candidate_itemsets(LK_minus_one)
       
        htree = gen_hash_tree(CK)
        # Scan database for support count of each candidate
        
        LK_minus_one = get_frequent_itemsets(dataset, htree, k,min_sup=2) 
        print(LK_minus_one)
        #htree._print_tree(htree.root)
        k += 1 

    return frequent 
def _print_rules(rules: list(tuple())):
    for rule in rules:
        print(f'{rule[0]} => {rule[1]} conf: {rule[2]}')
def _print_args():
    print(f'[Reading from {args.file}  ]')
    print(f'[Running {args.algorithm}  ]')
    print(f'[Min Support {args.support}]')
    print(f'[Rule Confidence {args.confidence}]')

def main():
    global args
    args = parseArgs()
    _print_args() 
    start = time.time()
    if args.algorithm == 'apriori':
        entries = get_dataset(args.file)
        frequent = apriori(entries)
        assoc_rules = gen_association_rules(frequent, args.confidence)
        _print_rules(assoc_rules)

    else:
        fp_tree = FP(args.file, args.dataIndex) 
        patt = fp_tree.fp(args.support)
        rules = fp_tree.gen_association_rules(patt, args.confidence)
        fp_tree._print_frequent_rules(rules)
        #fp_tree._print_frequent_items(fi)
    end = time.time()
    print(f'Memory: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} Mb Time: {end-start} s')

if __name__=="__main__":
    main()
