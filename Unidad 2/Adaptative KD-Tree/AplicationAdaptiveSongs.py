import pandas as pd
from sklearn.neighbors import KDTree
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors
import time

####################################################################### IMPLMENTACIÓN ADAPTIVE KD TREE #######################################################################

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

        if len(points) == 0:
            return None

        axis = self.find_axis_with_max_spread(points)
        points = sorted(points, key=lambda x: x[axis])  # para q funque sort
        median_index = len(points) // 2
        median_point = points[median_index]

        node = self.Node(median_point, axis)
        node.left = self.build_tree(points[:median_index])
        node.right = self.build_tree(points[median_index + 1:])
        return node

    def insert_points(self, points):
        self.root = self.build_tree(points)

    def search_recursive(self, node, point):

        if node is None:
            return False

        if np.array_equal(node.point, point):
            return True

        axis = node.axis

        if point[axis] < node.point[axis]:
            return self.search_recursive(node.left, point)
        else:
            return self.search_recursive(node.right, point)

    def query(self, point, k=5):
        return self.knn_recursive(self.root, point, k, [])

    def knn_recursive(self, node, point, k, neighbors):

        if node is None:
            return neighbors

        distance = np.linalg.norm(np.array(node.point) - np.array(point))
        neighbors.append((node.point, distance))
        neighbors = sorted(neighbors, key=lambda x: x[1])[:k]

        axis = node.axis

        if point[axis] < node.point[axis]:
            neighbors = self.knn_recursive(node.left, point, k, neighbors)
            if len(neighbors) < k or abs(point[axis] - node.point[axis]) < neighbors[-1][1]:
                neighbors = self.knn_recursive(node.right, point, k, neighbors)
        else:
            neighbors = self.knn_recursive(node.right, point, k, neighbors)
            if len(neighbors) < k or abs(point[axis] - node.point[axis]) < neighbors[-1][1]:
                neighbors = self.knn_recursive(node.left, point, k, neighbors)

        return neighbors

# var globales
data = pd.read_csv('canciones2.csv')
features = data[['BPM', 'Energía', 'Danza', 'Valencia']].values
scaler = MinMaxScaler()
features_normalized = scaler.fit_transform(features)
tree = KDTree(features_normalized, leaf_size=2)
adaptive_tree = AdaptiveKDTree(k=4)
adaptive_tree.insert_points(features_normalized)
ultimos_vecinos_adaptive = [] # para graficar

def encontrar_canciones_similares_kdtree(cancion_indice, k=5):

    cancion_consulta = features_normalized[cancion_indice].reshape(1, -1)
    start_time = time.perf_counter()
    distancias, indices = tree.query(cancion_consulta, k=k + 1)
    tiempo = time.perf_counter() - start_time
    
    print(f"\nCanciones similares a: {data.iloc[cancion_indice]['Título']} por {data.iloc[cancion_indice]['Artista']} (KDTree)")
    print(f"Atributos de la canción seleccionada: BPM: {data.iloc[cancion_indice]['BPM']}, Energía: {data.iloc[cancion_indice]['Energía']}, Danza: {data.iloc[cancion_indice]['Danza']}, Valencia: {data.iloc[cancion_indice]['Valencia']}\n")

    for i in indices[0]:
        if i != cancion_indice:
            print(f" -> {data.iloc[i]['Título']} por {data.iloc[i]['Artista']} (Género: {data.iloc[i]['Género']})")
            print(f"  Atributos: BPM: {data.iloc[i]['BPM']}, Energía: {data.iloc[i]['Energía']}, Danza: {data.iloc[i]['Danza']}, Valencia: {data.iloc[i]['Valencia']}")

    print(f"Tiempo de bisqueda con KDTree: {tiempo:.6f} segundos")


def encontrar_canciones_similares_adaptive(cancion_indice, k=5):

    global ultimos_vecinos_adaptive, adaptive_tree

    cancion_consulta = features_normalized[cancion_indice]
    start_time = time.perf_counter()
    vecinos = adaptive_tree.query(cancion_consulta, k=k + 1)
    tiempo = time.perf_counter() - start_time

    print(f"\nCanciones similares a: {data.iloc[cancion_indice]['Título']} por {data.iloc[cancion_indice]['Artista']} (Adaptive KDTree)")
    print(f"Atributos de la canción seleccionada: BPM: {data.iloc[cancion_indice]['BPM']}, Energía: {data.iloc[cancion_indice]['Energía']}, Danza: {data.iloc[cancion_indice]['Danza']}, Valencia: {data.iloc[cancion_indice]['Valencia']}\n")
    ultimos_vecinos_adaptive = [cancion_indice]

    for punto, distancia in vecinos:
        if not np.array_equal(punto, cancion_consulta):
            indice = np.where(np.all(features_normalized == punto, axis=1))[0][0]
            print(f" -> {data.iloc[indice]['Título']} por {data.iloc[indice]['Artista']} (Género: {data.iloc[indice]['Género']})")
            print(f"  Atributos: BPM: {data.iloc[indice]['BPM']}, Energía: {data.iloc[indice]['Energía']}, Danza: {data.iloc[indice]['Danza']}, Valencia: {data.iloc[indice]['Valencia']}")
            ultimos_vecinos_adaptive.append(indice)

    print(f"Tiempo de busqueda con Adaptive KDTree: {tiempo:.6f} segundos\n")

def visualizar_arbol_3d(puntos_vecinos, caracteristica1='BPM', caracteristica2='Energía', caracteristica3='Danza'):

    indices_caracteristicas = {'BPM': 0, 'Energía': 1, 'Danza': 2, 'Valencia': 3}
    idx1, idx2, idx3 = indices_caracteristicas[caracteristica1], indices_caracteristicas[caracteristica2], indices_caracteristicas[caracteristica3]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(features_normalized[:, idx1], features_normalized[:, idx2], features_normalized[:, idx3], c='blue', label='Canciones')

    for vecino in puntos_vecinos:
        ax.scatter(features_normalized[vecino, idx1], features_normalized[vecino, idx2], features_normalized[vecino, idx3], c='red', marker='x', s=100)

    for i in range(1, len(puntos_vecinos)):
        punto_origen = features_normalized[puntos_vecinos[0]]
        punto_vecino = features_normalized[puntos_vecinos[i]]
        ax.plot([punto_origen[idx1], punto_vecino[idx1]],
                [punto_origen[idx2], punto_vecino[idx2]],
                [punto_origen[idx3], punto_vecino[idx3]],
                c='black', linestyle='--')

    ax.set_xlabel(f'{caracteristica1} (Normalizado)')
    ax.set_ylabel(f'{caracteristica2} (Normalizado)')
    ax.set_zlabel(f'{caracteristica3} (Normalizado)')
    ax.set_title(f'Visualización 3D del Arbol y sus vecinos recomendados ({caracteristica1}, {caracteristica2}, {caracteristica3})')
    ax.legend()


    # para ver el name de la cancion
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        indice = sel.index
        titulo = data.iloc[indice]['Título']
        artista = data.iloc[indice]['Artista']
        sel.annotation.set_text(f"{titulo}\n{artista}")

    plt.savefig('Recomendaciones.png')


def menu_principal():

    while 1:
        print(">>>>>>>>>>>>>>>>>>   KD TREE VS ADAPTIVE KD TREE   <<<<<<<<<<<<<<<<<<\n")
        print("Opciones:")
        print("1: Recomendar canciones similares usando KDTree y Adaptive KDTree")
        print("2: Visualizar en 3D los vecinos encontrados (KDTree y Adaptive KDTree)")
        print("3: Salir")
        try:
            opcion = int(input("\nSeleccione una opcion: "))

            if opcion == 1:
                mostrar_lista_canciones()
                try:
                    cancion_indice = int(input("\nSeleccione el índice de la cancion para obtener recomendaciones: ")) - 1
                    if 0 <= cancion_indice < len(data):
                        encontrar_canciones_similares_kdtree(cancion_indice)
                        encontrar_canciones_similares_adaptive(cancion_indice)
                    else:
                        print("Numero invalido")
                except ValueError:
                    print("Entrada no valida")

            elif opcion == 2:
                if ultimos_vecinos_adaptive:
                    visualizar_arbol_3d(ultimos_vecinos_adaptive)
                else:
                    print("Debe realizar una busqueda primero (op 1)\n")

            elif opcion == 3:
                print("Gracias por usar el programa")
                break

            else:
                print("Opcion invalida")

        except ValueError:
            print("Error")

def mostrar_lista_canciones():

    print("\nLista de Canciones en el CSV:")
    for idx, row in data.iterrows():
        print(f"{idx + 1}: {row['Título']} por {row['Artista']}")

if __name__ == "__main__":
    menu_principal()