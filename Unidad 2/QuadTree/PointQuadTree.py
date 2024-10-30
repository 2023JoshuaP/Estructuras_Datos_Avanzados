import matplotlib.pyplot as plt

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
    
    def insert(self, x, y, data):
        if self.root is None:
            self.root = QuadTreeNode(x, y, data)
        else:
            self._insert(self.root, x, y, data, self.x_min, self.x_max, self.y_min, self.y_max)
        
        # Dibujar el resultado
        self.ax.clear()
        self._draw(self.root, self.x_min, self.x_max, self.y_min, self.y_max)
        plt.pause(0.5)
    
    def _insert(self, node, x, y, data, x_min, x_max, y_min, y_max):
        if node is None:
            return QuadTreeNode(x, y, data)
        
        if (x, y) == (node.x, node.y):
            node.data = data
            return node
        
        if x < node.x and y < node.y:  # Cuadrante NW
            node.NW = self._insert(node.NW, x, y, data, x_min, node.x, y_min, node.y)
        elif x >= node.x and y < node.y:  # Cuadrante NE
            node.NE = self._insert(node.NE, x, y, data, node.x, x_max, y_min, node.y)
        elif x < node.x and y >= node.y:  # Cuadrante SW
            node.SW = self._insert(node.SW, x, y, data, x_min, node.x, node.y, y_max)
        else:  # Cuadrante SE
            node.SE = self._insert(node.SE, x, y, data, node.x, x_max, node.y, y_max)
        
        return node

    def _draw(self, node, x_min, x_max, y_min, y_max):
        if node is None:
            return
        
        # Dibujar el punto
        self.ax.plot(node.x, node.y, 'ro')  # Dibuja el punto rojo
        
        # Mostrar las coordenadas y los datos asociados al punto
        self.ax.text(node.x + 1, node.y + 1, f'({node.x}, {node.y})\n{node.data}', fontsize=9, color='blue')
        
        # Dibujar solo las líneas correspondientes si hay subárboles en los cuadrantes
        if node.NW or node.NE or node.SW or node.SE:
            self.ax.plot([node.x, node.x], [y_min, y_max], 'k-')  # Línea vertical
            self.ax.plot([x_min, x_max], [node.y, node.y], 'k-')  # Línea horizontal
        
        # Dibujar los subárboles
        if node.NW:
            self._draw(node.NW, x_min, node.x, y_min, node.y)  # NW
        if node.NE:
            self._draw(node.NE, node.x, x_max, y_min, node.y)  # NE
        if node.SW:
            self._draw(node.SW, x_min, node.x, node.y, y_max)  # SW
        if node.SE:
            self._draw(node.SE, node.x, x_max, node.y, y_max)  # SE
    
    def show(self):
        plt.show()

tree = PointQuadTree(0, 100, 0, 100)  # Define el rango del área

# Insertar algunos puntos y visualizar
tree.insert(35, 42, "Chicago")
tree.insert(52, 10, "Mobile")
tree.insert(62, 77, "Toronto")
tree.insert(82, 65, "Buffalo")
tree.insert(5, 45, "Denver")
tree.insert(27, 35, "Omaha")
tree.insert(85, 15, "Atlanta")
tree.show()  # Muestra el gráfico en una ventana