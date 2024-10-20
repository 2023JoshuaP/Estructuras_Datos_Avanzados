import math
## Codigo LFU - Binomial Heap

class Node:
    def __init__(self, key, value, freq):
        self.key = key
        self.value = value
        self.freq = freq
        self.parent = None
        self.children = []
        self.degree = 0

class BinomialHeap:
    def __init__(self):
        self.trees = []
        self.min_node = None
        self.count = 0
    
    def insert(self, node):
        # Insertar nodo como un nuevo heap y luego combinar
        print(f"Insertando nodo: clave={node.key}, valor={node.value}, frecuencia={node.freq}")
        new_heap = BinomialHeap()
        new_heap.trees.append(node)
        new_heap.count = 1
        self.merge(new_heap)
        self._find_min()

    def extract_min(self):
        # Extraer el nodo con menor frecuencia (mínimo)
        print(f"Extrayendo nodo mínimo: clave={self.min_node.key}, valor={self.min_node.value}, frecuencia={self.min_node.freq}")
        min_node = self.min_node
        self.trees.remove(min_node)
        new_heap = BinomialHeap()
        new_heap.trees = min_node.children
        self.merge(new_heap)
        self._find_min()
        self.count -= 1
        return min_node

    def decrease_key(self, node, new_freq):
        # Disminuir frecuencia y reorganizar
        node.freq = new_freq
        print(f"Disminuyendo frecuencia del nodo: clave={node.key}, nueva frecuencia={node.freq}")
        self._bubble_up(node)
        self._find_min()

    def merge(self, other_heap):
        # Fusionar otro heap con el actual
        print(f"Fusionando heap. Tamaño actual del heap: {len(self.trees)}. Tamaño del otro heap: {len(other_heap.trees)}")
        self.trees.extend(other_heap.trees)
        self.count += other_heap.count
        self._find_min()

    def _find_min(self):
        # Encontrar el nodo con la frecuencia más baja
        print("Buscando nuevo nodo mínimo...")
        self.min_node = None
        for tree in self.trees:
            if self.min_node is None or tree.freq < self.min_node.freq:
                self.min_node = tree
        if self.min_node:
            print(f"Nuevo nodo mínimo: clave={self.min_node.key}, frecuencia={self.min_node.freq}")

    def _bubble_up(self, node):
        # Reorganizar nodo para mantener la propiedad del heap
        parent = node.parent
        while parent and node.freq < parent.freq:
            # Intercambiar nodos si la frecuencia es menor
            node.key, parent.key = parent.key, node.key
            node.value, parent.value = parent.value, node.value
            node.freq, parent.freq = parent.freq, node.freq
            node = parent
            parent = node.parent

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Almacena clave -> valor
        self.freq_heap = BinomialHeap()  # Gestiona nodos por frecuencia
        self.key_node_map = {}  # Almacena clave -> nodo para acceso rápido

    def get(self, key: int) -> int:
        if key not in self.cache:
            print(f"Clave {key} no encontrada.")
            return -1
        
        # Obtener el nodo de la clave y actualizar la frecuencia
        node = self.key_node_map[key]
        print(f"Obteniendo clave {key}. Valor={node.value}, Frecuencia={node.freq}")
        self._update_freq(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.cache:
            # Actualizar valor y frecuencia si la clave ya existe
            node = self.key_node_map[key]
            node.value = value
            self._update_freq(node)
        else:
            if len(self.cache) >= self.capacity:
                # Eliminar el elemento con menor frecuencia
                print("Capacidad máxima alcanzada. Evictando nodo.")
                self._evict()

            # Crear un nuevo nodo y agregarlo al heap
            new_node = Node(key, value, 1)
            self.freq_heap.insert(new_node)
            self.cache[key] = value
            self.key_node_map[key] = new_node

    def _evict(self):
        # Extraer el nodo con menor frecuencia del heap binomial
        print("Evictando el nodo con menor frecuencia...")
        node_to_evict = self.freq_heap.extract_min()
        del self.cache[node_to_evict.key]
        del self.key_node_map[node_to_evict.key]

    def _update_freq(self, node: Node):
        # Incrementar la frecuencia y reorganizar el heap
        print(f"Actualizando frecuencia del nodo: clave={node.key}, frecuencia actual={node.freq}")
        node.freq += 1
        self.freq_heap.decrease_key(node, node.freq)

    def display_cache(self):
        print("\nEstado actual de la cache (LFU Cache):")
        for key, node in self.key_node_map.items():
            print(f"Key: {key}, Value: {node.value}, Freq: {node.freq}")
        print("\n")

def main():
    print("Bienvenido al sistema de LFU Cache con Binomial Heap.")
    
    # Solicitar capacidad de la cache
    capacity = int(input("Ingresa la capacidad de la cache: "))
    cache = LFUCache(capacity)

    while True:
        print("\nOperaciones disponibles:")
        print("1. put <key> <value> - Insertar un nuevo valor o actualizar una clave existente")
        print("2. get <key> - Obtener el valor de una clave existente")
        print("3. Mostrar estado de la cache")
        print("4. Salir")

        option = input("\nSelecciona una operación (1, 2, 3 o 4): ")

        if option == "1":
            try:
                key_value = input("Ingresa la clave y el valor separados por un espacio (ejemplo: 1 100): ")
                key, value = map(int, key_value.split())
                cache.put(key, value)
                print(f"Clave {key} agregada/actualizada con valor {value}.")
            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar dos números separados por un espacio.")

        elif option == "2":
            try:
                key = int(input("Ingresa la clave que quieres buscar: "))
                result = cache.get(key)
                if result == -1:
                    print(f"Clave {key} no encontrada.")
                else:
                    print(f"Valor para la clave {key}: {result}")
            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar un número para la clave.")

        elif option == "3":
            cache.display_cache()

        elif option == "4":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 4.")

if __name__ == "__main__":
    main()
