from dataclasses import dataclass

@dataclass
class Node:
    is_leaf: bool = False
    label: str    = ""
    
class DecisionTree:
    def __init__(self, continuous=True):
        self.continuous = continuous 
        self.root = None
    # Check if all the classLabels are the same
    def _all_single_class(self, classes) -> bool:
        return len(classes.unique()) == 1


    def insert(self, data, node):
        # TODO: First check if the node is empty
        column_len = len(data.columns)
        # We assume labels are in the last column
        if self._all_single_class(data.iloc[:, column_len-1]):
            # Create a leaf node with current label
            pass

        pass

    # Start the building process
    def run(self, data):
        self.root = Node()
        self.insert(data, self.root)


