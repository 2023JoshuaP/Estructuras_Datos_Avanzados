from graphviz import Digraph

class KDTree:
    class Node:
        def __init__(self, point):
            self.point = point
            self.left = None
            self.right = None
    
    def __init__(self, k):
        self.k = k
        self.root = None
        
    def insert_recursive(self, node, point, depth):
        # Debug message
        print(f"Inserting point {point} at depth {depth}")
        
        if node is None:
            print(f"Inserted into a new node: {point}")
            return self.Node(point)
        
        cd = depth % self.k  # Current dimension
        print(f"Current dimension: {cd}, Current node: {node.point}")
        
        if point[cd] < node.point[cd]:
            print(f"Going to the left subtree of {node.point}")
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
            print(f"Going to the right subtree of {node.point}")
            node.right = self.insert_recursive(node.right, point, depth + 1)
        
        return node
    
    def insert(self, point):
        self.root = self.insert_recursive(self.root, point, 0)
    
    def search_recursive(self, node, point, depth):
        print(f"Searching for point {point} at depth {depth}")
        if node is None:
            print("Node not found")
            return False
        
        if node.point == point:
            print(f"Node found: {node.point}")
            return True
        
        cd = depth % self.k
        
        if point[cd] < node.point[cd]:
            print(f"Going to the left subtree of {node.point}")
            return self.search_recursive(node.left, point, depth + 1)
        else:
            print(f"Going to the right subtree of {node.point}")
            return self.search_recursive(node.right, point, depth + 1)
    
    def search(self, point):
        return self.search_recursive(self.root, point, 0)  
    
    def add_edges(self, dot, node):
        if node is None:
            return
        
        # Add the current node
        dot.node(str(node.point), f"x: {node.point[0]}\ny: {node.point[1]}")
        
        # Connect the node with its children
        if node.left:
            dot.edge(str(node.point), str(node.left.point), label="left")
            self.add_edges(dot, node.left)
        
        if node.right:
            dot.edge(str(node.point), str(node.right.point), label="right")
            self.add_edges(dot, node.right)
            
    def plot_tree(self):
        dot = Digraph()
        
        # Create the tree from the root
        if self.root is not None:
            self.add_edges(dot, self.root)
        
        # Render and show the graph
        dot.render('KDTree', format='png', cleanup=True)
        dot.view()

if __name__ == "__main__":
    kdtree = KDTree(2)
    
    points = [
        [165, 147], [231, 102], [378, 181], [317, 48], [114, 308],
        [422, 403], [147, 436], [28, 197], [179, 361], [205, 304]
    ]
    
    for point in points:
        kdtree.insert(point)
    
    kdtree.plot_tree()
    
    search_point = [165, 147]
    result = kdtree.search(search_point)
    if result:
        print(f"Point {search_point} found")
    else:
        print(f"Point {search_point} not found")