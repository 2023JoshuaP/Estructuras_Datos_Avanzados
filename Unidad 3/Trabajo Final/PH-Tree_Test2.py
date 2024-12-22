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

    def visualize(self, node=None, depth=0):
        if node is None:
            node = self.root

        indent = "  " * depth
        if node.is_leaf():
            print(f"{indent}- Leaf: {node.point} (Prefix: {node.prefix})")
        else:
            print(f"{indent}- Node (Prefix: {node.prefix})")
            for bit, child in sorted(node.children.items()):
                print(f"{indent}  Bit {bit}:")
                self.visualize(child, depth + 2)

    def generate_graph(self):
        dot = Digraph()

        def add_nodes_edges(node, parent_id=None):
            node_id = id(node)
            if node.is_leaf():
                prefix = node.prefix
                infix = "-"  # No infix for leaf nodes
                postfix = prefix[self.key_bits:] if prefix else "-"  # Bits below this node
                label = (f"Leaf\n{node.point}\n"
                         f"Prefix: {prefix}\n"
                         f"Infix: {infix}\nPostfix: {postfix}")
            else:
                prefix = node.prefix
                infix = prefix[:-1] if prefix else "-"  # Bits between parent and current node
                postfix = "-"  # Postfix not used at internal nodes
                label = (f"Node\nPrefix: {prefix}\n"
                         f"Infix: {infix}\nPostfix: {postfix}")

            dot.node(str(node_id), label)

            if parent_id is not None:
                dot.edge(str(parent_id), str(node_id))

            for bit, child in node.children.items():
                add_nodes_edges(child, node_id)

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
