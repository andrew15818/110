import numpy as np
import argparse

from graph import Graph
from algos.hits import HITS
from algos.pagerank import PageRank
from algos.simrank import SimRank

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
    parser.add_argument(
        '-d', '--damping',
        type=float, default=0.15,
        help='Likelihood our graph algorithm stops at a given node.'
    )
    parser.add_argument(
        '--out_dir',
        type=str, default='output',
        help='Output directory where relevant algorithm data is stored.'
    )
    return parser.parse_args()

# Call the appropriate algorithm
def run(args, graph:Graph):
    args.algorithm = args.algorithm.lower()
    algo = None
    print(f'[INFO] Running {args.algorithm}')
    if args.algorithm == 'hits':
        algo = HITS()
    elif args.algorithm == 'pagerank':
        algo = PageRank(damping=args.damping)

    algo.run(graph)
    algo.output(args.out_dir)


def main():
    args = parse_args()
    graph = Graph(args.file)
    run(args, graph)

if __name__=='__main__':
    main()
