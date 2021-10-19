import argparse
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
    with open(filename, 'r') as file:
        data = file.readlines()
    return data

# TODO: Add support for differently-formated files
def get_transaction_entries(transaction):
    if args.file == 'out.data':
        return transaction.split()[3:]
    elif args.file == 'test.data':
        return transaction.split()[1:]

# Get the 1-frequent itemsets
def get_1_itemsets(dataset):

    min_support = int(len(dataset) / 1000)
    # Can we use a list instead to maintain lexi ordering?
    candidates = {}
    cnd = [0] * len(dataset)
    print(f"Minimum support is {min_support}")

    for transaction in dataset:
        trans_items = get_transaction_entries(transaction)
        print(trans_items) 
        for item in trans_items:
            # keep count
            candidates[item] = 0 if item not in candidates else candidates[item] + 1

                    
    # Get only the candidates with high enough min_support
    # Loop to maintain lexi ordering needed later, bit slower tho...
    L1 = [[str(i)] for i in range(1, len(dataset)) if ((str(i) in candidates) and (candidates[str(i)] > min_support))]
    
    return L1

# Check if the first k-2 items are similar 
def common_sublist(l1, l2):
    for i in range(len(l1)-2):
        if l1[i] != l2[i]:
            return False 
    return True 

def get_candidate_itemsets(LK_minus_one):
    htree = HashTree()

    candidates = []
    for l1 in LK_minus_one:
        for l2 in LK_minus_one:
            # Possible candidate
            if common_sublist(l1, l2) and (l1[-1] < l2[-1]):
                #print(f'{l1} and {l2} share common sublist.')
                c =  [i for i in l1]
                c.append(l2[-1])
                print(c)
                # Check if candidate is frequent subset, prune otherwise
                # in hash tree
                htree.insert(c, support=1)

    return candidates


def apriori(dataset):
    L1 = get_1_itemsets(dataset)
    LK_minus_one = L1
    CK = get_candidate_itemsets(LK_minus_one)
    print(CK)

        

def main():
    global args
    args = parseArgs()
    print(f'Reading from {args.file}')

    entries = get_dataset(args.file)
    apriori(entries)

if __name__=="__main__":
    main()
