from graphviz import Digraph
import timeit

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

        cd = depth % self.k # Current dimension
        
        if point[cd] < node.point[cd]:
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
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
        start_time = timeit.default_timer()  # Inicio del temporizador
        result = self.search_recursive(self.root, point, 0)
        end_time = timeit.default_timer()  # Fin del temporizador
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución de la búsqueda: {execution_time:.6f} segundos")
        return result

    def find_min(self, node, d, depth):
        # Find the minimun node in the d-th dimension of the KD Tree
        if node is None:
            return None
        
        cd = depth % self.k
        
        if cd == d:
            if node.left is None:
                return node
            return self.find_min(node.left, d, depth + 1)

        left_min = self.find_min(node.left, d, depth + 1)
        right_min = self.find_min(node.right, d, depth + 1)
        
        min_node = node
        if left_min is not None and left_min.point[d] < min_node.point[d]:
            min_node = left_min
        if right_min is not None and right_min.point[d] < min_node.point[d]:
            min_node = right_min
        
        return min_node
    
    def delete_recursive(self, node, point, depth):
        if node is None:
            return None
        
        cd = depth % self.k
        
        # If the node to be deleted is found
        if node.point == point:
            # Case 1: Node with right child
            if node.right is not None:
                min_node = self.find_min(node.right, cd, depth + 1)
                node.point = min_node.point
                node.right = self.delete_recursive(node.right, min_node.point, depth + 1)
            # Case 2: Node with left child
            elif node.left is not None:
                min_node = self.find_min(node.left, cd, depth + 1)
                node.point = min_node.point
                node.right = self.delete_recursive(node.left, min_node.point, depth + 1)
                node.left = None
            # Case 3: Leaf node
            else:
                return None
            
            return node

        # Recursively search for the node to be deleted
        if point[cd] < node.point[cd]:
            node.left = self.delete_recursive(node.left, point, depth + 1)
        else:
            node.right = self.delete_recursive(node.right, point, depth + 1)
        
        return node
    
    def delete(self, point):
        self.root = self.delete_recursive(self.root, point, 0)
    
    def range_search_recursive(self, node, depth, min_bound, max_bound, points_in_range):
        if node is None:
            return
        if all([min_bound[i] <= node.point[i] <= max_bound[i] for i in range(self.k)]):
            points_in_range.append(node.point)
        
        cd = depth % self.k
        
        if min_bound[cd] <= node.point[cd]:
            self.range_search_recursive(node.left, depth + 1, min_bound, max_bound, points_in_range)
        if max_bound[cd] >= node.point[cd]:
            self.range_search_recursive(node.right, depth + 1, min_bound, max_bound, points_in_range)
    
    def range_search(self, min_bound, max_bound):
        start_time = timeit.default_timer()
        points_in_range = []
        self.range_search_recursive(self.root, 0, min_bound, max_bound, points_in_range)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Tiempo de ejecución de la búsqueda por rango: {execution_time:.6f} segundos")
        return points_in_range
        
    def add_edges(self, dot, node):
        if node is None:
            return
        
        # Add the current node
        dot.node(str(node.point), f"x: {node.point[0]},\ny: {node.point[1]}")
        
        # Add edges to the left and right subtrees
        if node.left is not None:
            dot.edge(str(node.point), str(node.left.point), label="left")
            self.add_edges(dot, node.left)
        
        if node.right is not None:
            dot.edge(str(node.point), str(node.right.point), label="right")
            self.add_edges(dot, node.right)
    
    def plot_tree(self):
        dot = Digraph()
        
        # Create the graph from the root
        if self.root is not None:
            self.add_edges(dot, self.root)
            
        dot.render('kd_tree_range_search', format='png', cleanup=True)
        dot.view()

if __name__ == "__main__":
    # Create a KD Tree
    kdtree = KDTree(2)
    
    points = [
        [5, 10],
        [15, 20],
        [30, 30],
        [25, 5],
        [10, 15],
        [12, 7],
        [18, 12],
        [22, 25],
        [27, 18],
        [3, 8],
        [8, 12],
        [14, 9],
        [11, 14],
        [16, 5],
        [4, 6],
        [9, 3],
        [19, 17],
        [13, 22],
        [7, 11],
        [20, 8]
    ]
    
    for point in points:
        kdtree.insert(point)
        
    kdtree.plot_tree()
    
    search_point = [10, 19]
    result = kdtree.search(search_point)
    if result:
        print(f"Point {search_point} found")
    else:
        print(f"Point {search_point} not found")
    
    min_bound = [1, 1]
    max_bound = [20, 20]
    
    points_in_range = kdtree.range_search(min_bound, max_bound)
    
    print(f"Points in the range {min_bound} to {max_bound}: {points_in_range}")
    
    # kdtree.plot_tree()
    
    # delete_point = [30, 40]
    # kdtree.delete(delete_point)
    # search_point = [165, 147]
    # result = kdtree.search(search_point)
    # if result:
        # print(f"Point {search_point} found")
    # else:
        # print(f"Point {search_point} not found")