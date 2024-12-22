from graphviz import Digraph

class PHNode:
    def __init__(self, prefix=None):
        self.prefix = prefix  # Prefix of this node
        self.children = {}    # Dictionary to store child nodes
        self.point = None     # Point stored at this node (if any)

    def is_leaf(self):
        return len(self.children) == 0 and self.point is not None

class PH1DTree:
    def __init__(self, key_bits=8):
        self.root = PHNode()
        self.key_bits = key_bits  # Number of bits for keys

    def insert(self, key):
        key_bin = f"{key:0{self.key_bits}b}"  # Convert key to binary string
        node = self.root

        for depth in range(self.key_bits):
            bit = key_bin[depth]
            if bit not in node.children:
                node.children[bit] = PHNode(prefix=key_bin[:depth + 1])

            node = node.children[bit]

        node.point = key  # Assign the key to the leaf node

    def find_root_path(self):
        """Find the path corresponding to the root based on the unique critical bit."""
        node = self.root
        root_path = []

        while not node.is_leaf() and len(node.children) == 1:
            bit = list(node.children.keys())[0]
            root_path.append((node, bit))
            node = node.children[bit]

        root_path.append((node, None))  # Add the final leaf node in the root path
        return root_path

    def generate_graph(self):
        dot = Digraph()
        root_path = self.find_root_path()
        root_nodes = {id(node): True for node, _ in root_path}

        def add_nodes_edges(node, parent_id=None, edge_color="black"):
            node_id = id(node)

            # Determine node label
            if node == self.root:
                label = "Root\n"
                label += (f"Prefix: {node.prefix if node.prefix else '-'}")
            elif node.is_leaf():
                prefix = node.prefix
                infix = "-"  # No infix for leaf nodes
                postfix = prefix[self.key_bits:] if prefix else "-"  # Bits below this node
                label = (f"Leaf\n{node.point}\n"
                         f"Prefix: {prefix}\n"
                         f"Infix: {infix}\nPostfix: {postfix}")
            else:
                prefix = node.prefix
                critical_bit = prefix[-1] if prefix else "-"
                infix = prefix[:-1] if prefix else "-"  # Bits between parent and current node
                label = (f"Subnode\nPrefix: {prefix}\n"
                         f"Infix: {infix}\nCritical Bit: {critical_bit}")

            # Set node color
            node_color = "red" if id(node) in root_nodes else "green"
            dot.node(str(node_id), label, color=node_color, style="filled", fillcolor=node_color)

            if parent_id is not None:
                dot.edge(str(parent_id), str(node_id), color=edge_color)

            for bit, child in node.children.items():
                child_edge_color = "red" if id(child) in root_nodes else "green"
                add_nodes_edges(child, node_id, edge_color=child_edge_color)

        add_nodes_edges(self.root)
        return dot

# Uso del PH1DTree
ph_tree = PH1DTree(key_bits=8)  # Cambiar key_bits si necesitas más bits para los números

# Inserción de puntos
keys_to_insert = [1, 4, 35]
for key in keys_to_insert:
    ph_tree.insert(key)

# Generar y guardar visualización del árbol
graph = ph_tree.generate_graph()
graph.render("ph_tree", format="png", cleanup=True)
