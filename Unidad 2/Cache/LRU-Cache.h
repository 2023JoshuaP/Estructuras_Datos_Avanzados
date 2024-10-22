#ifndef LRU_CACHE
#define LRU_CACHE

#include <iostream>
#include <unordered_map>
using namespace std;

class NodeLRU {
    public:
        int key, value;
        NodeLRU* prev;
        NodeLRU* next;
        NodeLRU(int k, int v): key(k), value(v), prev(nullptr), next(nullptr) {}
};

class LRUCache {
    private:
        int capacity;
        unordered_map<int, NodeLRU*> cache;
        NodeLRU* head;
        NodeLRU* tail;

        void removeNode(NodeLRU* node) {
            if (node->prev) node->prev->next = node->next;
            if (node->next) node->next->prev = node->prev;
            if (node == head) head = node->next;
            if (node == tail) tail = node->prev;
        }

        void moveToFront(NodeLRU* node) {
            node->next = head;
            node->prev = nullptr;
            if (head) {
                head->prev = node;
            }
            head = node;
            if (!tail) {
                tail = head;
            }
        }

        void removeTail() {
            if (tail) {
                cache.erase(tail->key);
                NodeLRU* prevTail = tail;
                tail = tail->prev;
                if (tail) {
                    tail->next = nullptr;
                }
                delete prevTail;
            }
        }
    public:
        LRUCache(int capacity) : capacity(capacity), head(nullptr), tail(nullptr) {}

        int get(int key);
        void put(int key, int value);
        void display();

        ~LRUCache() {
            while (head) {
                NodeLRU* temp = head;
                head = head->next;
                delete temp;
            }
        }
};

#endif