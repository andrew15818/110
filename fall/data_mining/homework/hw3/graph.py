import numpy as np

class Vertex:
    def __init__(self, value):
        self.value = value
        self.parents = []
        self.children = []
        self.authority, self.hub = 1, 1

    # Store only the id of the parents and children
    def add_parent(self, vertex_id:int):
        self.parents.append(vertex_id)

    def add_child(self, vertex_id:int):
        self.children.append(vertex_id)

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children
    def get_authority(self):
        return self.authority
    def get_hub(self):
        return self.hub

class Graph:
    def __init__(self, file:str):
        self.vertices = {}
        self.file = file
        self.adj = None
        self.ibm = True if 'ibm' in self.file else False

        self.build()
        print('Graph built.')

    def add_parent(self, child:int, parent:int):
        self.vertices[child].add_parent(parent)

    def add_child(self, parent:int, child:int):
        self.vertices[parent].add_child(child)
    
    def get_children(self, node_id:int) -> list:
        return self.vertices[node_id].children

    def get_node_count(self):
        return len(self.vertices)

    def get(self, node_id:int):
        return self.vertices[node_id]

    def get_parents(self, node_id:int) -> list:
        return self.vertices[node_id].parent

    def add_vertex(self, src:int):
        if src in self.vertices.keys():
            return
        self.vertices[src] = Vertex(src)
        
    def set_authority(self, node_id, auth):
        self.vertices[node_id].authority = auth

    def set_hub(self, node_id, hub):
        self.vertices[node_id].hub = hub 

    # Get the src and dest ids
    # Change this if file format changes
    def get_endpoints(self, line):
        line = line.rstrip()
        if self.ibm:
            line = line.split() 
            src, dst = line[1], line[2]
            return int(src), int(dst)

        line = line.split(',')
        src, dst = line[0], line[1]
        return int(src), int(dst)

    def build(self):
        with open(self.file, 'r') as f:
            for line in f:
                src, dst = self.get_endpoints(line)
                #print(f'Adding {src} -> {dst}')
                self.add_vertex(src)
                self.add_vertex(dst)

                self.add_parent(dst, src)
                self.add_child(src, dst)
        #self._print()

    # Get the graph information as an adjacency matrix
    def adjacency_matrix(self) -> np.array:
        # Only calculate adjacency once
        if self.adj:
            return self.adj

        N = max(self.vertices)
        adj = np.zeros(shape=(N,N))
        for idx, vertex in self.vertices.items():
            for child in vertex.get_children():
                adj[idx-1][child-1] = 1
        self.adj = adj
        return adj

    # Debug function
    def _print(self):
        for id, node in self.vertices.items():
            print(f'[{id}], children: {node.children}\t \
            parents: {node.parents}')
