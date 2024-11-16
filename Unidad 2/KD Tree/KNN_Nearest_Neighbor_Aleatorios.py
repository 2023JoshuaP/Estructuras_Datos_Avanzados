import time
import random
import csv

def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)**0.5

def bruce_force_knn(points, query_point, k):
    distances = []
    for point in points:
        distances.append((point, euclidean_distance(point, query_point)))
    distances = sorted(distances, key=lambda x: x[1])
    return distances[:k]

def load_points(filename):
    points = []
    with open(filename, "r") as file:
        for line in file:
            x, y, z = map(float, line.strip().split(','))
            points.append((x, y, z))
    return points

def generate_random_query():
    return (random.randint(0, 999), random.randint(0, 999), random.randint(0, 999))

file_names = ["1000.csv", "10000.csv", "20000.csv"]
k = 600

with open("execution_times_bruce_force.csv", mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["File", "Query Point", "Execution Time (seconds)"])
    
    for file_name in file_names:
        print(f"Processing {file_name}...")
        points = load_points(file_name)
        
        start_time = time.perf_counter()
        query_point = generate_random_query()
        nearest_negihbors = bruce_force_knn(points, query_point, k)
        end_time = time.perf_counter()
        
        exec_time = end_time - start_time
        csv_writer.writerow([file_name, query_point, exec_time])
        
        print("Query Point:", query_point)
        print("k-Nearest Neighbors:")
        for neighbor, distance in nearest_negihbors:
            print(f"Point: {neighbor}, Distance: {distance:.2f}")
        print(f"Execution Time: {exec_time:.5f} seconds\n")

print("Execution times saved to execution_times_bruce_force.csv")