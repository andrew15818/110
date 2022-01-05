import numpy as np
from graph import Graph

class PageRank:
    def __init__(self, damping):
        self.damping = damping
        self.x = None

    # TODO: Get rid of the iterations and 
    # figure out when algo converges
    def run(self, graph:Graph, iterations:int=3):
        N = len(graph.vertices)
        # Use the children of each vertex for adj. matrix
        adj = graph.adjacency_matrix()

        print(np.linalg.norm(adj,1 ))
        # Get transition matrix
        M = []
        for i, row in enumerate(adj):
            count = (row==1).sum()
            M.append(row/count if count > 0 else row)

        M = np.array(M)
        M = self.damping*M + (1-self.damping) / N
        z = np.ones(shape=(N, 1)) / N
        x = np.ones(shape=(N, 1)) / N
        x_prev = np.zeros(shape=(N, 1))
        i=0
        delta = 1
        #TODO: Fix the convergence check, use threshold
        while delta < .005: #not (x_prev == x).all():
            i+=1
            x_prev = x
            x = M @ x
            
            # Not sure about this bottom part, ppt says x1 + dt*z, can't find that anywher else
            dt = np.linalg.norm(x) - np.linalg.norm(x_prev)
            x += dt * z
            delta = np.linalg.norm(x_prev - x)
            print(delta)
        
        self.x = x
    def output(self, out_path):
        try:
            np.savetxt(out_path+'_PageRank.txt', self.x, fmt='%.4e', newline=' ', delimiter=', ')
        except FileNotFoundError:
            print('[Error] Make sure the output directory exists first!')
        print(f'PageRank:\n{self.x.T}')
