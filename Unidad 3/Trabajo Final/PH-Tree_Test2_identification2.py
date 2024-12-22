from graphviz import Digraph

class PHNode:
    def __init__(self, prefix=None, critical_bit=None):
        self.prefix = prefix  # Prefix of this node
        self.critical_bit = critical_bit  # Position of the critical bit
        self.children = {}    # Dictionary to store child nodes
        self.point = None     # Point stored at this node (if any)

    def is_leaf(self):
        return len(self.children) == 0 and self.point is not None


class PH1DTree:
    def __init__(self, key_bits=8):
        self.root = PHNode(prefix="", critical_bit=0)  # Root node with empty prefix
        self.key_bits = key_bits  # Number of bits for keys

    def insert(self, key):
        key_bin = f"{key:0{self.key_bits}b}"  # Convert key to binary string
        node = self.root

        for depth in range(self.key_bits):
            bit = key_bin[depth]
            if bit not in node.children:
                node.children[bit] = PHNode(prefix=key_bin[:depth + 1], critical_bit=depth)

            node = node.children[bit]

        node.point = key  # Assign the key to the leaf node

    def generate_graph(self):
        dot = Digraph()

        def add_nodes_edges(node, parent_id=None):
            node_id = id(node)

            # Node label construction
            if node.is_leaf():
                label = f"Leaf\n{node.point}\nPrefix: {node.prefix}\nInfix: -\nPostfix: -"
            else:
                prefix = node.prefix
                infix = prefix[node.critical_bit:] if node.critical_bit else prefix
                critical_bit = node.critical_bit
                label = (f"Subnode\nPrefix: {prefix}\n"
                         f"Infix: {infix}\nCritical Bit: {critical_bit}")

            # Set node color
            node_color = "green" if node != self.root else "red"
            dot.node(str(node_id), label, color="black", style="filled", fillcolor=node_color)

            # Add edges
            if parent_id:
                dot.edge(str(parent_id), str(node_id))

            # Recursively add children
            for child in node.children.values():
                add_nodes_edges(child, node_id)

        add_nodes_edges(self.root)
        return dot


# Uso del PH1DTree
ph_tree = PH1DTree(key_bits=8)

# Inserción de puntos
keys_to_insert = [1, 4, 35]
for key in keys_to_insert:
    ph_tree.insert(key)

# Generar y guardar visualización del árbol
graph = ph_tree.generate_graph()
graph.render("ph_tree_corrected", format="png", cleanup=True)
