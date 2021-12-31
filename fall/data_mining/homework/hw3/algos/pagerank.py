import numpy as np
from graph import Graph

class PageRank:
    def __init__(self, damping):
        self.damping = damping

    def run(self, graph:Graph):
        N = len(graph.vertices)
        # Use the children of each vertex for adj. matrix
        adj = graph.adjacency_matrix()
        # TODO: Get the pagerank value for each child
        
