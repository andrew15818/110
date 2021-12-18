class Vertex:
    def __init__(self, value):
        self.value = value
        self.parents = []
        self.children = []

    def add_parent(self, vertex):
        pass

    def add_child(self, vertex): 
        pass

class Graph:
    def __init__(self, file:str):
        self.vertices = {}
        self.file = file

        self.build()
        pass

    def add_parent(self, child:int, parent:int):
        self.vertices[child].add_parent(parent)
        pass

    def add_child(self, parent:int, child:int):
        self.vertices[parent].add_child(child)
        pass

    def add_vertex(self, src:int):
        if src in self.vertices.keys():
            return
        self.vertices[src] = Vertex(src)
        pass

    # Get the src and dest ids
    # Change this if file format changes
    def get_endpoints(self, line):
        src, dst = line.split()
        return int(src), int(dst)

    def build(self):
        with open(self.file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                src, dst = self.get_endpoints(line)
                self.add_vertex(src)
                self.add_vertex(dst)

                self.add_parent(dst, src)
                self.add_child(src, dst)



