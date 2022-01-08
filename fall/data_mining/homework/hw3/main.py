import numpy as np
import argparse

from graph import Graph
from algos.hits import HITS
from algos.pagerank import PageRank
from algos.simrank import SimRank
ALGOS = ['hits', 'pagerank', 'simrank']

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
        type=str, default='all',
        help='Specify the algorithm used in link analysis.'
    )
    parser.add_argument(
        '-d', '--damping',
        type=float, default=0.15,
        help='Likelihood our graph algorithm stops at a given node.'
    )
    parser.add_argument(
        '-C', '--decay',
        type=float, default=0.85,
        help='Decay factor for the SimRank algorithm.'
    )
    parser.add_argument(
        '--out_dir',
        type=str, default='output',
        help='Output directory where relevant algorithm data is stored.'
    )
    return parser.parse_args()

# Get the filename w/o file extension, path prefix
def get_output_file(path:str)->str:
    # If file is in another directory
    # otherwise will be just filename
    filename = path.split('/')[-1]
    # Remove the file extenstion
    return filename.split('.')[0]


# Call the appropriate algorithm
def run(args, graph:Graph):
    args.algorithm = args.algorithm.lower()
    algo = None
    print(f'\n[INFO] Running {args.algorithm}')

    if args.algorithm == 'hits':
        algo = HITS()
    elif args.algorithm == 'pagerank':
        algo = PageRank(damping=args.damping)
    elif args.algorithm == 'simrank':
        algo = SimRank(args.decay)

    algo.run(graph)
    outfile = get_output_file(args.file)
    outpath = args.out_dir+'/'+outfile
    algo.output(outpath)
    print(f'\n[INFO] Output results to {outpath}')


def main():
    args = parse_args()
    graph = Graph(args.file)
    run(args, graph)

if __name__=='__main__':
    main()
