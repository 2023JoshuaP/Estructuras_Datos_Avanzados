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
        # Mensaje de depuración
        print(f"Insertando punto {point} en profundidad {depth}")

        if node is None:
            print(f"Insertado en un nodo nuevo: {point}")
            return self.Node(point)

        cd = depth % self.k  # Dimensión actual
        print(f"Dimensión actual: {cd}, Nodo actual: {node.point}")

        if point[cd] < node.point[cd]:
            print(f"Va al subárbol izquierdo de {node.point}")
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
            print(f"Va al subárbol derecho de {node.point}")
            node.right = self.insert_recursive(node.right, point, depth + 1)

        return node

    def insert(self, point):
        self.root = self.insert_recursive(self.root, point, 0)

    def add_edges(self, dot, node):
        if node is None:
            return

        # Agregar el nodo actual
        dot.node(str(node.point), f"x: {node.point[0]}\ny: {node.point[1]}")

        # Conectar el nodo con sus hijos
        if node.left:
            dot.edge(str(node.point), str(node.left.point), label="left")
            self.add_edges(dot, node.left)

        if node.right:
            dot.edge(str(node.point), str(node.right.point), label="right")
            self.add_edges(dot, node.right)

    def plot_tree(self):
        dot = Digraph()

        # Crear el árbol a partir de la raíz
        if self.root is not None:
            self.add_edges(dot, self.root)

        # Renderizar y mostrar el gráfico
        dot.render('kdtree', view=True, format='png')

if __name__ == "__main__":
    # Crear un KDTree con 2 dimensiones
    kdtree = KDTree(2)

    # Insertar puntos en el KDTree
    points = [
        [165, 147], [231, 102], [378, 181], [317, 48], [114, 308],
        [422, 403], [147, 436], [28, 197], [179, 361], [205, 304]
    ]

    for point in points:
        kdtree.insert(point)

    # Dibujar el árbol
    kdtree.plot_tree()
