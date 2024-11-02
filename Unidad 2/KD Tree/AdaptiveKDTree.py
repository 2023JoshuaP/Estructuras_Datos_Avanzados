import numpy as np
import timeit
import matplotlib.pyplot as plt

class AdaptiveKDTree:
    class Node:
        def __init__(self, point, axis=None):
            self.point = point
            self.left = None
            self.right = None
            self.axis = axis

    def __init__(self, k):
        self.k = k
        self.root = None

    def find_axis_with_max_spread(self, points):
        points_array = np.array(points)
        spreads = points_array.max(axis=0) - points_array.min(axis=0)
        axis = np.argmax(spreads)
        return axis

    def build_tree(self, points):
        if not points:
            return None

        axis = self.find_axis_with_max_spread(points)
        points.sort(key=lambda x: x[axis])
        median_index = len(points) // 2
        median_point = points[median_index]

        node = self.Node(median_point, axis)
        node.left = self.build_tree(points[:median_index])
        node.right = self.build_tree(points[median_index + 1:])
        return node

    def insert_points(self, points, show_step=False):
        plt.ion()
        for i in range(len(points)):
            self.root = self.build_tree(points[:i+1])
            if show_step:
                self.show_2d_plot(step=i+1)
                plt.pause(0.5)

        plt.ioff()
        plt.show()

    def search_recursive(self, node, point):
        if node is None:
            return False

        if node.point == point:
            return True

        axis = node.axis
        if point[axis] < node.point[axis]:
            return self.search_recursive(node.left, point)
        else:
            return self.search_recursive(node.right, point)

    def search(self, point):
        start_time = timeit.default_timer()
        found = self.search_recursive(self.root, point)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Resultado de búsqueda para {point}: {'encontrado' if found else 'no encontrado'}.")
        print(f"Tiempo de ejecución de la búsqueda: {execution_time:.6f} segundos")
        return found

    def range_search_recursive(self, node, min_bound, max_bound, points_in_range):
        if node is None:
            return

        if all(min_bound[i] <= node.point[i] <= max_bound[i] for i in range(self.k)):
            points_in_range.append(node.point)

        axis = node.axis

        if min_bound[axis] <= node.point[axis]:
            self.range_search_recursive(node.left, min_bound, max_bound, points_in_range)
        if max_bound[axis] >= node.point[axis]:
            self.range_search_recursive(node.right, min_bound, max_bound, points_in_range)

    def range_search(self, min_bound, max_bound):
        start_time = timeit.default_timer()
        points_in_range = []
        self.range_search_recursive(self.root, min_bound, max_bound, points_in_range)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Puntos encontrados en el rango {min_bound} a {max_bound}: {points_in_range}")
        print(f"Tiempo de ejecución de la búsqueda por rango: {execution_time:.6f} segundos")
        return points_in_range

    def plot_2d_recursive(self, node, min_x, max_x, min_y, max_y):
        if node is None:
            return

        axis = node.axis
        plt.plot(node.point[0], node.point[1], 'ro')

        if axis == 0:
            plt.plot([node.point[0], node.point[0]], [min_y, max_y], 'b--')
            self.plot_2d_recursive(node.left, min_x, node.point[0], min_y, max_y)
            self.plot_2d_recursive(node.right, node.point[0], max_x, min_y, max_y)
        else:
            plt.plot([min_x, max_x], [node.point[1], node.point[1]], 'g--')
            self.plot_2d_recursive(node.left, min_x, max_x, min_y, node.point[1])
            self.plot_2d_recursive(node.right, min_x, max_x, node.point[1], max_y)

    def show_2d_plot(self, step=None):
        plt.clf()
        self.plot_2d_recursive(self.root, min_x=0, max_x=30, min_y=0, max_y=30)
        plt.xlabel("x")
        plt.ylabel("y")
        title = "2D View of Adaptive KD-Tree"
        if step is not None:
            title += f" - Step {step}"
        plt.title(title)
        plt.grid(True)
        plt.draw()

# Ejemplo de uso
if __name__ == "__main__":
    points = [
        [3, 6], [17, 15], [13, 15], [6, 12], [9, 1], [2, 7], [10, 19]
    ]
    adaptive_tree = AdaptiveKDTree(2)
    adaptive_tree.insert_points(points, show_step=True)

    point_to_search = [10, 15]
    adaptive_tree.search(point_to_search)

    min_bound = [5, 5]
    max_bound = [20, 20]
    adaptive_tree.range_search(min_bound, max_bound)