from graphviz import Digraph

class PHNode:
    def __init__(self, prefix="", critical_bit=0, infix=""):
        self.prefix = prefix          # Prefix of this node
        self.infix = infix            # Infix: bits between parent and this node
        self.critical_bit = critical_bit  # Position of the critical bit
        self.postfix = ""             # Bits below this node
        self.children = {}            # Child nodes
        self.point = None             # Value stored at this node

    def is_leaf(self):
        return len(self.children) == 0 and self.point is not None


class PH1DTree:
    def __init__(self, key_bits=8):
        self.root = PHNode(prefix="", critical_bit=0)
        self.key_bits = key_bits  # Total number of bits in the keys

    def insert(self, key):
        key_bin = f"{key:0{self.key_bits}b}"  # Convert key to binary
        node = self.root
        prev_prefix = ""

        for depth in range(self.key_bits):
            bit = key_bin[depth]
            infix = key_bin[len(prev_prefix):depth]
            if bit not in node.children:
                node.children[bit] = PHNode(prefix=key_bin[:depth + 1],
                                            critical_bit=depth,
                                            infix=infix)
            prev_prefix = node.prefix
            node = node.children[bit]

        # Set the leaf node with postfix
        node.point = key
        node.postfix = key_bin[len(node.prefix):]  # Remaining bits

    def generate_graph(self):
        dot = Digraph()

        def add_nodes_edges(node, parent_id=None):
            node_id = id(node)

            # Node label construction
            if node.is_leaf():
                label = (f"Leaf\n{node.point}\n"
                         f"Prefix: {node.prefix}\n"
                         f"Infix: {node.infix}\n"
                         f"Postfix: {node.postfix}")
            else:
                label = (f"Subnode\nPrefix: {node.prefix}\n"
                         f"Infix: {node.infix}\n"
                         f"Critical Bit: {node.critical_bit}")

            # Node color: red for root, green for others
            node_color = "red" if node == self.root else "green"
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
