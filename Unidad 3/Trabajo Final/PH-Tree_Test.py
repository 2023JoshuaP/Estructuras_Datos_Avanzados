from graphviz import Digraph

class PHTree1DNode:
    def __init__(self):
        self.children = {}
        self.values = []
        self.prefix = None
        self.critical_bit = None

class PHTree1D:
    def __init__(self, bit_length = 8):
        self.root = PHTree1DNode()
        self.bit_lenght = bit_length
    
    def _find_critical_bit(self, key1, key2):
        for i in range(self.bit_lenght):
            if ((key1 >> i) & 1) != ((key2 >> i) & 1):
                return i
        return None
    
    def _navigate_to_node(self, key):
        current_node = self.root
        depth = 0
        while True:
            if current_node.prefix is None:
                current_node.prefix = key
                return current_node
            critical_bit = self._find_critical_bit(current_node.prefix, key)
            if critical_bit is None or depth > critical_bit:
                return current_node
            direction = (key >> critical_bit) & 1
            if direction not in current_node.children:
                current_node.children[direction] = PHTree1DNode()
                current_node.children[direction].critical_bit = critical_bit
            current_node = current_node.children[direction]
            depth = critical_bit + 1
    
    def insert(self, value):
        key = value
        target_node = self._navigate_to_node(key)
        target_node.values.append(value)
    
    def to_graphviz(self):
        dot = Digraph()
        
        def _add_node_to_graphviz(node, node_id):
            label = f"Prefix: {node.prefix if node.prefix is not None else 'None'}\nValues: {', '.join(map(str, node.values))}"
            if node.critical_bit is not None:
                label += f"\nCritical Bit: {node.critical_bit}"
            dot.node(node_id, label=label)
            for child_key, child_node in node.children.items():
                child_id = f"{node_id}_{child_key}"
                dot.edge(node_id, child_id, label=f"{child_key}")
                _add_node_to_graphviz(child_node, child_id)
                
        root_id = "root"
        _add_node_to_graphviz(self.root, root_id)
        return dot

if __name__ == "__main__":
    tree = PHTree1D(bit_length=8)
    tree.insert(1)
    tree.insert(4)
    tree.insert(35)
    dot = tree.to_graphviz()
    dot.render("ph_tree_1d", format="png", cleanup=True)
    print("PH-Tree 1D created and saved as 'ph_tree_1d.png'")