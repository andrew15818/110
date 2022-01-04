import numpy as np
from graph import Graph

class PageRank:
    def __init__(self, damping):
        self.damping = damping

    # TODO: Get rid of the iterations and 
    # figure out when algo converges
    def run(self, graph:Graph, iterations:int):
        N = len(graph.vertices)
        # Use the children of each vertex for adj. matrix
        adj = graph.adjacency_matrix()

        print(np.linalg.norm(adj,1 ))
        # Get transition matrix
        M = []
        for i, row in enumerate(adj):
            count = (row==1).sum()
            M.append(row/count if count > 0 else row)
        
        for i in range(iterations):
            pass



        
