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
k_values = [100, 200, 300, 400, 500, 600, 700, 800, 900]

with open("execution_times_bruce_force_k_diferent.csv", mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["File Name", "K", "Execution Time (seconds)"])
    
    for file_name in file_names:
        points = load_points(file_name)
        
        for k in k_values:
            print(f"Processing {file_name} with k = {k}...")
            start_time = time.perf_counter()
            query_point = generate_random_query()
            nearest_negihbors = bruce_force_knn(points, query_point, k)
            end_time = time.perf_counter()
            
            exec_time = end_time - start_time
            csv_writer.writerow([file_name, k, exec_time])
            
            print("Query Point:", query_point)
            print(f"Execution Time for k={k}: {exec_time:.5f} seconds\n")

print("Execution times for different k values saved to execution_times_bruce_force_k_diferent.csv")