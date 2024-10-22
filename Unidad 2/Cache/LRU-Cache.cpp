#include "./LRU-Cache.h"

int LRUCache::get(int key) {
    if (cache.find(key) != cache.end()) {
        NodeLRU* node = cache[key];
        if (node != head) {
            removeNode(node);
            moveToFront(node);
        }
        return node->value;
    }
    return -1;
}

void LRUCache::put(int key, int value) {
    if (cache.find(key) != cache.end()) {
        NodeLRU* node = cache[key];
        node->value = value;
        removeNode(node);
        moveToFront(node);
    }
    else {
        if (cache.size() == capacity) {
            removeTail();
        }
        NodeLRU* newNode = new NodeLRU(key, value);
        moveToFront(newNode);
        cache[key] = newNode;
    }
}

void LRUCache::display() {
    NodeLRU* current = head;
    cout << "Estado actual del cache: ";
    while (current) {
        cout << "(" << current->key << ", " << current->value << ") ";
        current = current->next;
    }
    cout << endl;
}