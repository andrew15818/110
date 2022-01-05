import numpy as np
from graph import Graph
class SimRank:
    def __init__(self, decay):
        self.sim_scores = None
        self.decay = decay
    def calc_simrank(self, n1, n2)-> None:

        if n1.value == n2.value:
            return 1

        elif len(n1.children) == 0 or len(n2.children) == 0:
            return 0

        psim = 0 # parent sim scores
        for p1 in n1.parents:
            for p2 in n2.parents:
                psim += self.sim_scores[p1-1][p2-1]
        return psim 

    def run(self, graph, iterations=10):
        nodes = graph.get_node_count()
        # nxn
        self.sim_scores = np.identity(nodes)
        adj = graph.adjacency_matrix()
        #print(self.sim_scores,'\n',  adj) 
        print(self.sim_scores.shape)
        for i in range(iterations):
            for n1 in graph.vertices:
                for n2 in graph.vertices:
                    sim = self.calc_simrank(graph.get(n1), graph.get(n2))
                    self.sim_scores[n1-1,n2-1] = sim
                    # Get simrank score for two nodes
                    # Update matrix
        # TODO: see if we can do it with matrix operations instead.

   
    def output(self, out_path:str):
        np.savetxt(out_path+'_SimRank.txt', self.sim_scores, fmt='%.4f')
        print(f'SimRank: \n{self.sim_scores}')
        pass
