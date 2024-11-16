import math
import heapq

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
        if node is None:
            return self.Node(point)

        cd = depth % self.k

        if point[cd] < node.point[cd]:
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
            node.right = self.insert_recursive(node.right, point, depth + 1)
        return node

    def insert(self, point):
        self.root = self.insert_recursive(self.root, point, 0)

    def euclidean_distance(self, point1, point2):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

    def knn_recursive(self, node, query_point, k, depth, heap):
        if node is None:
            return

        distance = self.euclidean_distance(query_point, node.point)

        if len(heap) < k:
            heapq.heappush(heap, (-distance, node.point))
        else:
            if -heap[0][0] > distance:
                heapq.heappushpop(heap, (-distance, node.point))

        cd = depth % self.k
        next_branch = node.left if query_point[cd] < node.point[cd] else node.right
        opposite_branch = node.right if next_branch == node.left else node.left

        self.knn_recursive(next_branch, query_point, k, depth + 1, heap)

        if len(heap) < k or abs(query_point[cd] - node.point[cd]) < -heap[0][0]:
            self.knn_recursive(opposite_branch, query_point, k, depth + 1, heap)

    def knn_nearest_neighbor(self, query_point, k):
        heap = []
        self.knn_recursive(self.root, query_point, k, 0, heap)
        return [(-distance, point) for distance, point in sorted(heap, reverse=True)]

    def to_dot(self):
        def node_to_dot(node):
            if not node:
                return ""
            node_str = f'"{node.point}" [label="{node.point}"];\n'
            if node.left:
                node_str += f'"{node.point}" -> "{node.left.point}" [label="L"];\n'
                node_str += node_to_dot(node.left)
            if node.right:
                node_str += f'"{node.point}" -> "{node.right.point}" [label="R"];\n'
                node_str += node_to_dot(node.right)
            return node_str

        return "digraph KDTree {\n" + node_to_dot(self.root) + "}\n"

kdtree = KDTree(3)
points = [
    (2, 3, 1),
    (5, 4, 7),
    (9, 6, 3),
    (4, 7, 8),
    (8, 1, 5),
    (7, 2, 6)
]

for p in points:
    kdtree.insert(p)

query_point = (9, 2, 4)
k = 3
nearest_neighbors = kdtree.knn_nearest_neighbor(query_point, k)

print("Query Point:", query_point)
print("k-Nearest Neighbors:")
for distance, neighbor in nearest_neighbors:
    print(f"Point: {neighbor}, Distance: {distance:.2f}")

dot_representation = kdtree.to_dot()
print("\nGraphviz DOT representation:\n")
print(dot_representation)