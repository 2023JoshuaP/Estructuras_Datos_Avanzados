from PIL import Image
from graphviz import Digraph

class Color:
    def __init__(self, r=0, g=0, b=0, alpha=None):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha

class Node:
    def __init__(self, level, parent):
        self.color = Color(0, 0, 0)
        self.pixel_count = 0
        self.palette_index = 0
        self.children = [None] * 8
        if level < OcTree.MAX_DEPTH - 1:
            parent.add_level_node(level, self)
    
    def is_leaf(self):
        return self.pixel_count > 0
    
    def get_leaf_nodes(self):
        leaf_nodes = []
        for i in range(8):
            node = self.children[i]
            if node:
                if node.is_leaf():
                    leaf_nodes.append(node)
                else:
                    leaf_nodes.extend(node.get_leaf_nodes())
        return leaf_nodes
    
    def add_colors(self, color, level, parent):
        if level >= OcTree.MAX_DEPTH:
            self.color.r += color.r
            self.color.g += color.g
            self.color.b += color.b
            self.pixel_count += 1
            return
        index = self.get_color_index(color, level)
        if not self.children[index]:
            self.children[index] = Node(level, parent)
        self.children[index].add_colors(color, level + 1, parent)
    
    def get_palette_index(self, color, level):
        if self.is_leaf():
            return self.palette_index
        index = self.get_color_index(color, level)
        if self.children[index]:
            return self.children[index].get_palette_index(color, level + 1)
        else:
            for i in range(8):
                if self.children[i]:
                    return self.children[i].get_palette_index(color, level + 1)
    
    def remove(self):
        result = 0
        for i in range(8):
            node = self.children[i]
            if node:
                self.color.r += node.color.r
                self.color.g += node.color.g
                self.color.b += node.color.b
                self.pixel_count += node.pixel_count
                result += 1
        return result - 1
    
    def get_color_index(self, color, level):
        index = 0
        mask = 0x80 >> level
        if color.r & mask:
            index |= 4
        if color.g & mask:
            index |= 2
        if color.b & mask:
            index |= 1
        return index
    
    def get_color(self):
        return Color(
            self.color.r / self.pixel_count,
            self.color.g / self.pixel_count,
            self.color.b / self.pixel_count
        )

class OcTree:
    MAX_DEPTH = 8
    def __init__(self):
        self.levels = {i: [] for i in range(OcTree.MAX_DEPTH)}
        self.root = Node(0, self)
        
    def get_leaves(self):
        return [node for node in self.root.get_leaf_nodes()]
    
    def add_level_node(self, level, node):
        self.levels[level].append(node)
    
    def add_color(self, color):
        self.root.add_colors(color, 0, self)
    
    def make_palette(self, colors):
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())
        for level in range(OcTree.MAX_DEPTH - 1, -1, -1):
            if self.levels[level]:
                for node in self.levels[level]:
                    leaf_count -= node.remove()
                    if leaf_count <= colors:
                        break
                if leaf_count <= colors:
                    break
                self.levels[level] = []
        for node in self.get_leaves():
            if palette_index >= colors:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette
    
    def get_palette_index(self, color):
        return self.root.get_palette_index(color, 0)

# Visualización del Octree en texto
def print_tree(node, level=0):
    indent = "  " * level
    if node.is_leaf():
        print(f"{indent}Leaf: Color({node.color.r:.1f}, {node.color.g:.1f}, {node.color.b:.1f}), Pixels: {node.pixel_count}")
    else:
        print(f"{indent}Node at level {level}")
        for i, child in enumerate(node.children):
            if child:
                print(f"{indent}  Child {i}:")
                print_tree(child, level + 1)

# Exportar el Octree a Graphviz
def export_tree(node, graph, parent=None, node_id=0):
    current_id = str(node_id)
    if node.is_leaf():
        label = f"Leaf\nR:{node.color.r:.1f}\nG:{node.color.g:.1f}\nB:{node.color.b:.1f}\nPixels:{node.pixel_count}"
    else:
        label = f"Node\nLevel:{node_id}"
    graph.node(current_id, label)
    
    if parent is not None:
        graph.edge(str(parent), current_id)
    
    child_id = node_id + 1
    for i, child in enumerate(node.children):
        if child:
            child_id = export_tree(child, graph, current_id, child_id)
    
    return child_id

def main():
    image = Image.open('rainbow.png')
    pixels = image.load()
    width, height = image.size
    
    octree = OcTree()
    
    for j in range(height):
        for i in range(width):
            octree.add_color(Color(*pixels[i, j]))
    
    # Generar la visualización gráfica
    graph = Digraph(format="png")
    export_tree(octree.root, graph)
    graph.render("octree_visualization", cleanup=True)
    print("Visualización gráfica generada: octree_visualization.png")
    
    palette = octree.make_palette(4)
    palette_image = Image.new('RGB', (2, 2))
    palette_pixels = palette_image.load()
    
    for i, color in enumerate(palette):
        palette_pixels[i % 2, i // 2] = (int(color.r), int(color.g), int(color.b))
    
    palette_image.save('paletterainbow.png')
    output_image = Image.new('RGB', (width, height))
    output_pixels = output_image.load()
    for j in range(height):
        for i in range(width):
            index = octree.get_palette_index(Color(*pixels[i, j]))
            color = palette[index]
            output_pixels[i, j] = (int(color.r), int(color.g), int(color.b))
    
    output_image.save('outputrainbow.png')
    
if __name__ == '__main__':
    main()