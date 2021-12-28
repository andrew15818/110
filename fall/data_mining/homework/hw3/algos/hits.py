import math
import numpy as np

from graph import Graph

class HITS:
    def __init__(self):
        pass

    # Auth and hub can be calculated by just taking the 
    # sum of the auth/hubs in the arrays whose indices are
    # in parents and children, respectively
    # Hopefully graphs always start with node id 1 :D
    def update_auth(self, parents: list) -> float:
        ret = sum(self.hubs[i-1] for i in parents)
        return ret

    def update_hub(self, children:list) -> float:
        ret = sum(self.authorities[i-1] for i in children)
        return ret

    def run(self, graph:Graph):
        # Adjust for index
        self.authorities = np.ones(len(graph.vertices))
        self.hubs = np.ones(len(graph.vertices))
        i = 1
        threshold = 1
        prev_auth, prev_hub = 1, 1
        while True:
            prev_auth, prev_hub = self.authorities.sum(), self.hubs.sum()
            # Update the auth and hub for each node
            for id, vertex in graph.vertices.items():

                # Authority depends on the innodes' hubness
                node_auth = self.update_auth(vertex.get_parents())
                node_hub = self.update_hub(vertex.get_children())

                self.authorities[id-1] = node_auth
                self.hubs[id-1] = node_hub

            self.authorities /= self.authorities.sum()
            self.hubs /= self.hubs.sum()

            if ((prev_auth - self.authorities.sum()) +
                (prev_hub  - self.hubs.sum())) < threshold:
                break


            i += 1

    # Print contents to stdout and filename
    def output(self, out_dir:str):
        try:
            np.savetxt(out_dir+'/HITS_authority.txt', self.authorities)
            np.savetxt(out_dir+'/HITS_hub.txt', self.hubs)
        except FileNotFoundError:
            print(f'[Error] Try making the {out_dir} directory first!')
        print(f'Authority:\n{self.authorities}')
        print(f'Hub:\n{self.hubs}')
