def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)**0.5

def bruce_force_knn(points, query_point, k):
    distances = []
    for point in points:
        distances.append((point, euclidean_distance(point, query_point)))
    distances = sorted(distances, key=lambda x: x[1])
    return distances[:k]

points = [
    (2, 3, 1),
    (5, 4, 7),
    (9, 6, 3),
    (4, 7, 8),
    (8, 1, 5),
    (7, 2, 6)
]

query_point = (9, 2, 4)
k = 3

nearest_neighbors = bruce_force_knn(points, query_point, k)
print("k-Nearest Neighbors:")
for neighbor, distance in nearest_neighbors:
    print(f"Point: {neighbor}, Distance: {distance:.2f}")