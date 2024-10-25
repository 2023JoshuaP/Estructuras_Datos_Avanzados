import matplotlib.pyplot as plt
import itertools

class KDTree:
    class Node:
        def __init__(self, point, color):
            self.point = point
            self.color = color  # Asignar color al nodo
            self.left = None
            self.right = None

    def __init__(self, k):
        self.k = k
        self.root = None
        self.colors = itertools.cycle(['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta'])

    def insert_recursive(self, node, point, depth):
        if node is None:
            return self.Node(point, next(self.colors))  # Obtener el siguiente color para el nodo

        cd = depth % self.k  # Dimensión actual

        if point[cd] < node.point[cd]:
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
            node.right = self.insert_recursive(node.right, point, depth + 1)

        return node

    def insert(self, point):
        self.root = self.insert_recursive(self.root, point, 0)

    # Función auxiliar para dibujar las divisiones del KD-Tree
    def plot_2d_recursive(self, ax, node, depth, xmin, xmax, ymin, ymax):
        if node is None:
            return

        cd = depth % self.k  # Dimensión de división actual (0 para x, 1 para y)

        # Dibujar la división actual
        if cd == 0:  # Dividir por x
            ax.plot([node.point[0], node.point[0]], [ymin, ymax], 'k-')  # Línea vertical
            self.plot_2d_recursive(ax, node.left, depth + 1, xmin, node.point[0], ymin, ymax)
            self.plot_2d_recursive(ax, node.right, depth + 1, node.point[0], xmax, ymin, ymax)
        else:  # Dividir por y
            ax.plot([xmin, xmax], [node.point[1], node.point[1]], 'k-')  # Línea horizontal
            self.plot_2d_recursive(ax, node.left, depth + 1, xmin, xmax, ymin, node.point[1])
            self.plot_2d_recursive(ax, node.right, depth + 1, xmin, xmax, node.point[1], ymax)

        # Dibujar el punto actual con su color asignado
        ax.plot(node.point[0], node.point[1], 'o', color=node.color, markersize=8)

    # Función principal para graficar el KD-Tree en 2D
    def plot_2d(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 600)  # Ajusta según el rango de tus puntos
        ax.set_ylim(0, 400)  # Ajusta según el rango de tus puntos

        # Llamar a la función recursiva para dibujar las divisiones
        self.plot_2d_recursive(ax, self.root, 0, 0, 600, 0, 400)

        # Mostrar el gráfico
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

if __name__ == "__main__":
    # Crear un KDTree con 2 dimensiones
    kdtree = KDTree(2)

    # Insertar puntos en el KDTree
    points = [
        [268, 254], [262, 351], [42, 358], [283, 293], [219, 266],
        [421, 166], [500, 283], [369, 157], [417, 210], [399, 376]
    ]

    for point in points:
        kdtree.insert(point)

    # Dibujar el KD-Tree en 2D
    kdtree.plot_2d()

#'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta'