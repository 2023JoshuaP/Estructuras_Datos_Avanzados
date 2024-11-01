import random
import matplotlib.pyplot as plt
from graphviz import Digraph

class QuadTreeNode:
    def __init__(self, x, y, data):
        self.x = x  # Coordenada x del punto
        self.y = y  # Coordenada y del punto
        self.data = data  # Datos asociados al punto
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None

class PointQuadTree:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.root = None
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.fig, self.ax = plt.subplots()  # Inicializa el gráfico
        self.graph = Digraph()  # Inicializa el grafo de Graphviz
    
    def insert(self, x, y, data):
        if self.root is None:
            self.root = QuadTreeNode(x, y, data)
            self._add_to_graph(None, self.root, "Root")
        else:
            self._insert(self.root, x, y, data, self.x_min, self.x_max, self.y_min, self.y_max)
        
        # Dibujar el resultado
        self.ax.clear()
        self._draw(self.root, self.x_min, self.x_max, self.y_min, self.y_max)
        plt.pause(0.5)
    
    def _insert(self, node, x, y, data, x_min, x_max, y_min, y_max):
        if node is None:
            new_node = QuadTreeNode(x, y, data)
            self._add_to_graph(None, new_node, f"({x},{y})")  # Agrega el nodo al grafo
            return new_node
        
        if (x, y) == (node.x, node.y):
            node.data = data
            return node
        
        # Cambiar la lógica de los cuadrantes para que sea correcta:
        if x < node.x and y >= node.y:  # Cuadrante NW (arriba izquierda)
            if node.NW is None:
                self._add_to_graph(node, QuadTreeNode(x, y, data), "NW")
            node.NW = self._insert(node.NW, x, y, data, x_min, node.x, node.y, y_max)
        elif x >= node.x and y >= node.y:  # Cuadrante NE (arriba derecha)
            if node.NE is None:
                self._add_to_graph(node, QuadTreeNode(x, y, data), "NE")
            node.NE = self._insert(node.NE, x, y, data, node.x, x_max, node.y, y_max)
        elif x < node.x and y < node.y:  # Cuadrante SW (abajo izquierda)
            if node.SW is None:
                self._add_to_graph(node, QuadTreeNode(x, y, data), "SW")
            node.SW = self._insert(node.SW, x, y, data, x_min, node.x, y_min, node.y)
        else:  # Cuadrante SE (abajo derecha)
            if node.SE is None:
                self._add_to_graph(node, QuadTreeNode(x, y, data), "SE")
            node.SE = self._insert(node.SE, x, y, data, node.x, x_max, y_min, node.y)
        
        return node
    
    def range_search(self, x_min, x_max, y_min, y_max):
        result = []
        self._range_search(self.root, x_min, x_max, y_min, y_max, result)
        
        # Dibujar el rectángulo de búsqueda
        self.ax.add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                        edgecolor='green', fill=False, linewidth=2, linestyle='--'))
        
        # Resaltar los puntos encontrados
        for x, y, data in result:
            self.ax.plot(x, y, 'go')  # Resalta los puntos en verde dentro del rango
        
        plt.pause(0.5)  # Pausa para mostrar la actualización
        return result
    
    def _range_search(self, node, x_min, x_max, y_min, y_max, result):
        if node is None:
            return
        
        # Verificar si el nodo actual está en el rango
        if x_min <= node.x <= x_max and y_min <= node.y <= y_max:
            result.append((node.x, node.y, node.data))
            print(f"Punto dentro del rango: ({node.x}, {node.y}) con data: {node.data}")
        
        # Condiciones para entrar en cada cuadrante basado en los límites de búsqueda
        # Exploramos el NW si el cuadrante NW tiene posibilidades de contener puntos en el rango
        if node.x >= x_min and node.y <= y_max:
            print("Entrando al cuadrante NW")
            self._range_search(node.NW, x_min, x_max, y_min, y_max, result)
        
        # Exploramos el NE si el cuadrante NE tiene posibilidades de contener puntos en el rango
        if node.x <= x_max and node.y <= y_max:
            print("Entrando al cuadrante NE")
            self._range_search(node.NE, x_min, x_max, y_min, y_max, result)
        
        # Exploramos el SW si el cuadrante SW tiene posibilidades de contener puntos en el rango
        if node.x >= x_min and node.y >= y_min:
            print("Entrando al cuadrante SW")
            self._range_search(node.SW, x_min, x_max, y_min, y_max, result)
        
        # Exploramos el SE si el cuadrante SE tiene posibilidades de contener puntos en el rango
        if node.x <= x_max and node.y >= y_min:
            print("Entrando al cuadrante SE")
            self._range_search(node.SE, x_min, x_max, y_min, y_max, result)

    def _draw(self, node, x_min, x_max, y_min, y_max):
        if node is None:
            return
        
        # Dibujar el punto
        self.ax.plot(node.x, node.y, 'ro')  # Dibuja el punto rojo
        
        # Mostrar el texto con las coordenadas y el dato
        self.ax.text(node.x + 1, node.y + 1, f'({node.x}, {node.y})\n{node.data}', fontsize=9, color='blue')
        
        # Dibujar solo las líneas correspondientes si hay subárboles en los cuadrantes
        if node.NW or node.NE or node.SW or node.SE:
            self.ax.plot([node.x, node.x], [y_min, y_max], 'k-')  # Línea vertical
            self.ax.plot([x_min, x_max], [node.y, node.y], 'k-')  # Línea horizontal
        
        # Dibujar los subárboles
        if node.NW:
            self._draw(node.NW, x_min, node.x, node.y, y_max)  # NW
        if node.NE:
            self._draw(node.NE, node.x, x_max, node.y, y_max)  # NE
        if node.SW:
            self._draw(node.SW, x_min, node.x, y_min, node.y)  # SW
        if node.SE:
            self._draw(node.SE, node.x, x_max, y_min, node.y)  # SE
    
    def _add_to_graph(self, parent, child, direction):
        """Agrega un nodo al grafo de Graphviz."""        
        child_label = f'({child.x}, {child.y})\n{child.data}'
        self.graph.node(child_label)  # Crea el nodo en Graphviz
        if parent:
            parent_label = f'({parent.x}, {parent.y})\n{parent.data}'
            self.graph.edge(parent_label, child_label, label=direction)  # Crea el borde con dirección

    def render_graph(self, filename="quadtree"):
        """Renderiza el grafo en un archivo .png."""
        self.graph.render(filename, format='png', cleanup=False)
    
    def show(self):
        plt.show()

# Ejemplo de uso
tree = PointQuadTree(0, 200, 0, 200)  # Define el rango del área

# Insertar 50 puntos aleatorios
for i in range(50):
    x_random = random.randint(0, 200)
    y_random = random.randint(0, 200)
    tree.insert(x_random, y_random, f"Point {i+1}")

# Realiza una búsqueda por rango para probar
result = tree.range_search(25, 75, 25, 75)
print("Puntos encontrados en el rango (25,75) x (25,75): ", result)

# Renderiza el gráfico con Graphviz
tree.render_graph("quadtree_visualization")

tree.show()  # Muestra el gráfico en una ventana