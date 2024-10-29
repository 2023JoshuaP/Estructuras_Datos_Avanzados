from graphviz import Digraph
import matplotlib.pyplot as plt

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
        return self.search_recursive(self.root, point, 0)

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
        points_in_range = []
        self.range_search_recursive(self.root, 0, min_bound, max_bound, points_in_range)
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
    
    def plot_2d_recursive(self, node, depth, min_bound, max_bound):
        if node is None:
            return

        cd = depth % self.k  # Current division dimension (0 for x, 1 for y)
        plt.plot(node.point[0], node.point[1], 'bo')
        
        # Draw the current division
        if cd == 0:  # Divide by x
            plt.plot([node.point[0], node.point[0]], [min_bound[1], max_bound[1]], 'r-')
            # Recursion for left and right children with updated bounds
            self.plot_2d_recursive(node.left, depth + 1, min_bound, [node.point[0], max_bound[1]])
            self.plot_2d_recursive(node.right, depth + 1, [node.point[0], min_bound[1]], max_bound)
        else:  # Divide by y
            plt.plot([min_bound[0], max_bound[0]], [node.point[1], node.point[1]], 'g-')
            # Recursion for top and bottom children with updated bounds
            self.plot_2d_recursive(node.left, depth + 1, min_bound, [max_bound[0], node.point[1]])
            self.plot_2d_recursive(node.right, depth + 1, [min_bound[0], node.point[1]], max_bound)
    
    def plot_2d(self):
        plt.figure(figsize=(8, 8))
        plt.xlim(0, 75)
        plt.ylim(0, 75)

        # Recursively plot the tree, starting with infinite bounds
        self.plot_2d_recursive(self.root, 0, [0, 0], [75, 75])

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('2D KD-Tree')
        plt.grid(True)
        plt.show()

class KDTreeMenu:
    def __init__(self):
        self.kdtree = KDTree(2)  # KD Tree de 2 dimensiones
    
    def display_menu(self):
        print("\n--- Menú KD-Tree ---")
        print("1. Insertar un punto")
        print("2. Buscar un punto")
        print("3. Eliminar un punto")
        print("4. Búsqueda por rango")
        print("5. Visualizar el KD-Tree")
        print("6. Visualizar KD-Tree 2D")
        print("7. Salir")
    
    def insert_point(self):
        point = list(map(int, input("Ingrese las coordenadas del punto (x, y): ").split()))
        self.kdtree.insert(point)
        print(f"Punto {point} insertado.")
    
    def search_point(self):
        point = list(map(int, input("Ingrese las coordenadas del punto a buscar (x, y): ").split()))
        found = self.kdtree.search(point)
        if found:
            print(f"Punto {point} encontrado en el KD-Tree.")
        else:
            print(f"Punto {point} no encontrado en el KD-Tree.")
    
    def delete_point(self):
        point = list(map(int, input("Ingrese las coordenadas del punto a eliminar (x, y): ").split()))
        self.kdtree.delete(point)
        print(f"Punto {point} eliminado, si existía.")
    
    def range_search(self):
        min_bound = list(map(int, input("Ingrese las coordenadas mínimas (x_min, y_min): ").split()))
        max_bound = list(map(int, input("Ingrese las coordenadas máximas (x_max, y_max): ").split()))
        points_in_range = self.kdtree.range_search(min_bound, max_bound)
        print(f"Puntos en el rango {min_bound} a {max_bound}: {points_in_range}")
    
    def plot_tree(self):
        self.kdtree.plot_tree()
        print("El KD-Tree ha sido visualizado.")
    
    def plot_2d_tree(self):
        self.kdtree.plot_2d()
        print("El KD-Tree ha sido visualizado en 2D.")
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Seleccione una opción: ")
            
            if choice == '1':
                self.insert_point()
            elif choice == '2':
                self.search_point()
            elif choice == '3':
                self.delete_point()
            elif choice == '4':
                self.range_search()
            elif choice == '5':
                self.plot_tree()
            elif choice == '6':
                self.plot_2d_tree()
            elif choice == '7':
                print("Saliendo del menú KD-Tree.")
                break
            else:
                print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    menu = KDTreeMenu()
    menu.run()