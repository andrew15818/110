import argparse
from hashtree import HashTree

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

def getEntries(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    return data

# TODO: Add support for differently-formated files
def get_transaction_entries(transaction):
    return transaction.split()[3:]

# Get the 1-frequent itemsets
def get_1_itemsets(dataset):

    min_support = int(len(dataset) / 1000)
    candidates = {}
    print(f"Minimum support is {min_support}")

    for transaction in dataset:
        trans_items = get_transaction_entries(transaction)
        
        for item in trans_items:
            # keep count
            candidates[item] = 0 if item not in candidates else candidates[item] + 1
                    
    # Get only the candidates with high enough min_support
    L1 = [query for query in candidates if candidates[query] > min_support]
    print(L1)
    return L1

def apriori(dataset):
    L1 = get_1_itemsets(dataset)

def main():
    args = parseArgs()
    print(f'Reading from {args.file}')

    entries = getEntries(args.file)
    apriori(entries)

if __name__=="__main__":
    main()
