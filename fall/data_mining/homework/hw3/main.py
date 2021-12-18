import numpy as np
import argparse

from graph import Graph
def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="$(prog) OPTIONS",
        description="Perform link analysis on the given input file."
    )
    parser.add_argument(
        '-f', '--file',
        type=str, default='./data/web-Stanford.txt',
        help='File where the initial data is lcoated.'
    )
    parser.add_argument(
        '-a', '--algorithm',
        type=str, default='pagerank',
        help='Specify the algorithm used in link analysis.'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    graph = Graph(args.file)
if __name__=='__main__':
    main()