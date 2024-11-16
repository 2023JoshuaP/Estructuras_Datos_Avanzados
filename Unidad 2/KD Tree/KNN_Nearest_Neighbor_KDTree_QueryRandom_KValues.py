import math
import heapq
import time
import random
import csv

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

def read_points(file_name):
    points = []
    with open(file_name, "r") as file:
        for line in file:
            points.append(tuple(map(int, line.strip().split(','))))
    # print(f"First 5 points from {file_name}: {points[:5]}") - Verificación de los primeros 5 puntos
    return points

def find_coordinate_ranges(points):
    min_values = [float('inf')] * len(points[0])
    max_values = [-float('inf')] * len(points[0])

    for point in points:
        for i in range(len(point)):
            min_values[i] = min(min_values[i], point[i])
            max_values[i] = max(max_values[i], point[i])

    return min_values, max_values

def generate_random_query(min_values, max_values):
    return tuple(random.randint(min_value, max_value) for min_value, max_value in zip(min_values, max_values))

file_name = ['1000.csv', '10000.csv', '20000.csv']
k_values = [100, 200, 300, 400, 500, 600, 700, 800, 900]
results = []

for file in file_name:
    print(f"\nProcessing file: {file}")
    kdtree = KDTree(3)
    points = read_points(file)
    for p in points:
        kdtree.insert(p)

    min_values, max_values = find_coordinate_ranges(points)
    
    for k in k_values:
        query_point = generate_random_query(min_values, max_values)

        start_time = time.perf_counter()
        nearest_neighbors = kdtree.knn_nearest_neighbor(query_point, k)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        results.append([file, k, execution_time])

        print(f"File: {file}, k: {k}, Execution time: {execution_time:.10f} seconds")

with open('execution_times_vs_k.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File Name", "k", "Execution Time (seconds)"])
    writer.writerows(results)

print("\nExecution times for varying k have been saved to 'execution_times_vs_k.csv'.")