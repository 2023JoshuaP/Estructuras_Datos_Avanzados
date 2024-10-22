#include "./FIFO-Cache.h"

int FIFOCache::get(int key) {
    if (cache.find(key) == cache.end()) {
        return -1;
    }
    return cache[key];
}

void FIFOCache::put(int key, int value) {
    if (cache.find(key) != cache.end()) {
        return;
    }

    if (cache.size() == capacidad) {
        int key = cola.pop();
        cache.erase(key);
    }

    cache[key] = value;
    cola.push(key);
}

void FIFOCache::display() {
    std::cout << "Estado actual del cache:\n";
    if (cache.empty()) {
        std::cout << "Cache vacío\n";
        return;
    }
    for (auto it = cache.begin(); it != cache.end(); it++) {
        std::cout << it->first << ": " << it->second << "\n";
    }
}