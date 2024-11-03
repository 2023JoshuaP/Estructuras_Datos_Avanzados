import matplotlib.pyplot as plt
import cv2
import numpy as np

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
        
        if point == node.point:
            return node
        
        if point[cd] < node.point[cd]:
            node.left = self.insert_recursive(node.left, point, depth + 1)
        else:
            node.right = self.insert_recursive(node.right, point, depth + 1)
        
        return node

    def insert(self, point):
        self.root = self.insert_recursive(self.root, point, 0)
    
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

class ImageSegmenter:
    def __init__(self, image_path, k=3):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("Error: No se pudo cargar la imagen.")
        self.kdtree = KDTree(k)
        self.load_colors()
        
    def load_colors(self):
        img_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        pixels = img_hsv.reshape(-1, 3)
        for pixel in pixels:
            self.kdtree.insert(tuple(pixel))

    def segment(self, color_range):
        # convertimos a formato HSV
        min_bound = np.array(color_range[0], dtype=np.uint8)
        max_bound = np.array(color_range[1], dtype=np.uint8)
        segmented_colors = self.kdtree.range_search(min_bound, max_bound)

        # Crear una máscara de ceros (negra)
        mask = np.zeros(self.image.shape[:2], dtype=np.uint8)

        # creamos la nueva mascara con los colores que encontramos
        for color in segmented_colors:
            color = np.array(color, dtype=np.uint8)
            matches = np.all(cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV) == color, axis=-1)
            mask[matches] = 255  # Marcar los píxeles que coinciden en la máscara

        # Aplicar la mascara a la imagen original
        segmented_image = cv2.bitwise_and(self.image, self.image, mask=mask)
        return segmented_image

    def display_results(self, mask):
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title('Imagen Original')
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Imagen Segmentada')
        plt.imshow(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.show()

if __name__ == "__main__":
    # Ruta de la imagen
    image_path = 'imagen2.jpg'
    
    # Definimos el rango de colores a segmentar en formato HSV
    
    # en este caso Azul
    color_range = [(90, 50, 50), (130, 255, 255)]
    
    # en este caso Rojo
    # color_range = [(0, 50, 50), (10, 255, 255)]
    
    # en este caso Verde
    # color_range = [(35, 50, 50), (85, 255, 255)]
    
    # en este caso Amarillo
    # color_range = [(20, 50, 50), (30, 255, 255)]
    
    # en este caso Negro
    # color_range = [(0, 0, 0), (180, 255, 30)]
    
    # en este caso Blanco
    # color_range = [(0, 0, 200), (180, 20, 255)]

    segmenter = ImageSegmenter(image_path)
    mask = segmenter.segment(color_range)
    segmenter.display_results(mask)
