import numpy as np

from graph import Graph

class HITS:
    def __init__(self):
        print('In the hitter')
    # Use the hubness of parents
    def authority(self, node_id:int):

        pass

    # Use the auth of children 
    def hubness(self, node_id:int):
        pass

    def run(self, graph:Graph):
        self.authorities = np.ones(len(graph.vertices))
        self.hubs = np.ones(len(graph.vertices))
        i = 0
        while i < 2:
            for id, vertex in graph.vertices.items():
                # Update the authorities and hubs for each node

            i += 1
