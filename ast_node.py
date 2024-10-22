class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.node_type == "operand": 
            return f"Operand({self.value})"
        else:
            return f"Operator({self.value}, {self.left}, {self.right})"
