#include "./LFU-Cache.h"

int LFUCache::get(int key) {
    if (cache.find(key) == cache.end()) {
        std::cout << "Clave " << key << " no encontrada." << std::endl;
        return -1;
    }
    Node* node = key_node_map[key];
    std::cout << "Obteniendo clave " << key << ". Valor = " << node->value << ", Frecuencia = " << node->freq << std::endl;
    update_freq(node);
    return node->value;
}

void LFUCache::put(int key, int value) {
    if (capacity == 0) {
        return;
    }
    if (cache.find(key) != cache.end()) {
        Node* node = key_node_map[key];
        node->value = value;
        update_freq(node);
    }
    else {
        if (cache.size() >= capacity) {
            std::cout << "Capacidad maxima alcanzada." << std::endl;
            evict();
        }
        Node* new_node = new Node(key, value, 1);
        freq_heap.insert(new_node);
        cache[key] = value;
        key_node_map[key] = new_node;
    }
}

void LFUCache::display() {
    std::cout << "\nEstado actual de la cache (LFU Cache):\n";
    for (const auto& pair : key_node_map) {
        Node* node = pair.second;
        std::cout << "Key: " << node->key << ", Value: " << node->value << ", Freq: " << node->freq << std::endl;
    }
    std::cout << std::endl;
}