import argparse
import itertools
import copy

from hashtree import Node, HashTree

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
        '--dataset',
        default='ibm'
    )
    args = parser.parse_args()
    return args 

def get_dataset(filename):
    parsed = []
    with open(filename, 'r') as file:
        data = file.readlines()
       
        for transaction in data:
            parsed.append(get_transaction_entries(transaction))
    return parsed

# TODO: Add support for differently-formated files
def get_transaction_entries(transaction):
    if args.file == 'out.data':
        return transaction.split()[3:]
    elif args.file == 'test.data':
        return transaction.split()[1:]

# Get the 1-frequent itemsets
def gen_1_itemsets(dataset):

    min_support = int(len(dataset) / 1000)
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
    L1 = [[str(i)] for i in range(1, len(dataset)) if ((str(i) in candidates) and (candidates[str(i)] > min_support))]
    
    return L1

# Check if the first k-2 items are similar 
def share_common_prefix(l1, l2):
    for i in range(len(l1)-2):
        if l1[i] != l2[i]:
            return False 
    return True 
# Generate all the candidate itemsets
def gen_candidate_itemsets(LK_minus_one, htree):

    candidates = []
    for l1 in LK_minus_one:
        for l2 in LK_minus_one:
            # Possible candidate
            if share_common_prefix(l1, l2) and (l1[-1] < l2[-1]):
                c =  [i for i in l1]
                c.append(l2[-1])
                #print(f"Inserting {c}")
                htree.insert(tuple(c))
                candidates.append(c)

    return candidates

# Return all k-subsets of a transaciton
def gen_k_subsets(transaction: tuple, k:int) -> list:
    return itertools.combinations(transaction, k)

# TODO: Different name for func and htree method!
def get_frequent_itemsets(dataset, htree, k=2, min_sup=1):
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
    print(frequent_items)
    return frequent_items


def apriori(dataset):
    L1 = gen_1_itemsets(dataset)
    LK_minus_one = L1
    
    min_support = int(len(dataset) / 1000)
    k=2 
    while LK_minus_one:
        htree = HashTree()
        CK = gen_candidate_itemsets(LK_minus_one, htree)
        # Scan database for support count of each candidate
        
        LK_minus_one = get_frequent_itemsets(dataset, htree, k,min_sup=2) 
        htree._print_tree(htree.root)
        k += 1 
    # TODO: Generate rules from frequent itemsets
        

def main():
    global args
    args = parseArgs()
    print(f'Reading from {args.file}')

    entries = get_dataset(args.file)
    apriori(entries)

if __name__=="__main__":
    main()
