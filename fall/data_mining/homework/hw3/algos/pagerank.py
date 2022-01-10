import numpy as np
from graph import Graph

class PageRank:
    def __init__(self, damping):
        self.damping = damping
        self.x = None

    # TODO: Get rid of the iterations and 
    # figure out when algo converges
    def run(self, graph:Graph, iterations:int=3):
        N = max(graph.vertices)
        # Use the children of each vertex for adj. matrix
        adj = graph.adjacency_matrix()

        #print(np.linalg.norm(adj,1 ))
        # Get transition matrix
        M = []
        for i, row in enumerate(adj):
            count = (row==1).sum()
            M.append(row/count if count > 0 else row)

        M = np.array(M)
        M = self.damping*M + (1-self.damping) / N

        z = np.ones(shape=(N, 1)) / N
        x = np.random.rand(N, 1)
        x /= np.linalg.norm(x, 1)
        x_prev = np.zeros(shape=(N, 1))
        i=0

        delta = 1
        while delta > .005: 
           
            i+=1
            x_prev = x
            x = M @ x

            # Other resources use fixed number of iterations,
            # These lines just evluate the difference in norms
            # b/w this iteration and previous
            dt = np.linalg.norm(x_prev) - np.linalg.norm(x)
            x += dt * z
            delta = np.linalg.norm(x_prev - x)
        
        # Save for printing later
        self.x = x
    def output(self, out_path):
        try:
            np.savetxt(out_path+'_PageRank.txt', self.x, fmt='%.4e', newline=' ', delimiter=', ')
        except FileNotFoundError:
            print('[Error] Make sure the output directory exists first!')
        print(f'PageRank:\n{self.x.T}')
