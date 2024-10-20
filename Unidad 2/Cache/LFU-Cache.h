#ifndef LFU_CACHE
#define LFU_CACHE

#include <iostream>
#include <unordered_map>
#include <vector>
#include <algorithm>

class Node {
    public:
        int key;
        int value;
        int freq;
        Node* parent;
        std::vector<Node*> children;
        int degree;

        Node(int k, int v, int f) : key(k), value(v), freq(f), parent(nullptr), degree(0) {}
};

class BinomialHeap {
    public:
        std::vector<Node*> trees;
        Node* min_node;
        int count;

        BinomialHeap() : min_node(nullptr), count(0) {}

        void insert(Node* node) {
            // Insertar el nodo en un nuevo heap y fusionar
            BinomialHeap new_heap;
            new_heap.trees.push_back(node);
            new_heap.count = 1;
            merge(new_heap);
            find_min();
        }

        Node* extract_min() {
            // Extraer el nodo mínimo
            Node* min_node = this->min_node;
            trees.erase(std::remove(trees.begin(), trees.end(), min_node), trees.end());

            BinomialHeap new_heap;
            new_heap.trees = min_node->children;
            min_node->children.clear();
            merge(new_heap);
            find_min();
            count--;
            return min_node;
        }

        void decrease_key(Node* node, int new_freq) {
            node->freq = new_freq;
            bubble_up(node);
            find_min();
        }

        void merge(BinomialHeap& other_heap) {
            trees.insert(trees.end(), other_heap.trees.begin(), other_heap.trees.end());
            count += other_heap.count;
            find_min();
        }

        void find_min() {
            min_node = nullptr;
            for (Node* tree : trees) {
                if (!min_node || tree->freq < min_node->freq) {
                    min_node = tree;
                }
            }
        }

        void bubble_up(Node* node) {
            Node* parent = node->parent;
            while (parent && node->freq < parent->freq) {
                std::swap(node->key, parent->key);
                std::swap(node->value, parent->value);
                std::swap(node->freq, parent->freq);
                node = parent;
                parent = node->parent;
            }
        }
};

class LFUCache {
    public:
        int capacity;
        std::unordered_map<int, int> cache;
        BinomialHeap freq_heap;
        std::unordered_map<int, Node*> key_node_map;

        LFUCache(int cap) : capacity(cap) {}

        int get(int key);
        void put(int key, int value);
        void display();
    private:
        void evict() {
            Node* node_to_evict = freq_heap.extract_min();
            cache.erase(node_to_evict->key);
            key_node_map.erase(node_to_evict->key);
            delete node_to_evict;
        }

        void update_freq(Node* node) {
            node->freq++;
            freq_heap.decrease_key(node, node->freq);
        }
};

#endif