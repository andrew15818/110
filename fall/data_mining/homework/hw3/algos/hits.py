import math
import numpy as np

from graph import Graph

class HITS:
    def __init__(self):
        pass
    # Use the hubness of parents
    def authority(self, node_id:int):
        pass

    # Use the auth of children 
    def hubness(self, node_id:int):
        pass

    # Get the top k pages
    def get_root_set(self, k=3):
        pass

    def run(self, graph:Graph):
        self.authorities = np.ones(len(graph.vertices))
        self.hubs = np.ones(len(graph.vertices))
        i = 0
        while i < 2:
            auth_norm, hub_norm = 0, 0
            for id, vertex in graph.vertices.items():
                new_auth, new_hub = 0, 0
                

                # Authority depends on the innodes' hubness
                for parent in vertex.get_parents():
                    parent = graph.get(parent)
                    new_auth += parent.get_hub()
                auth_norm += new_auth ** 2

                # Hub dependss on the auth of the children
                for child in vertex.get_children():
                    child = graph.get(child)
                    new_hub += child.get_authority()
                hub_norm += new_hub ** 2

                auth_norm /= math.sqrt(auth_norm)
                hub_norm /= math.sqrt(hub_norm)

                graph.set_authority(node_id=id, auth=auth_norm)
                graph.set_hub(node_id=id, hub=hub_norm)
                print(f'[{id}] auth: {auth_norm} hub: {hub_norm}')
            i += 1
