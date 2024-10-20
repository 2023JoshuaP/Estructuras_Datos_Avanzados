#ifndef LRU_CACHE
#define LRU_CACHE

#include <iostream>
#include <unordered_map>
using namespace std;

class Node {
    public:
        int key, value;
        Node* prev;
        Node* next;
        Node(int k, int v): key(k), value(v), prev(nullptr), next(nullptr) {}
};

class LRUCache {
    private:
        int capacity;
        unordered_map<int, Node*> cache;
        Node* head;
        Node* tail;

        void removeNode(Node* node) {
            if (node->prev) node->prev->next = node->next;
            if (node->next) node->next->prev = node->prev;
            if (node == head) head = node->next;
            if (node == tail) tail = node->prev;
        }

        void moveToFront(Node* node) {
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
                Node* prevTail = tail;
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
                Node* temp = head;
                head = head->next;
                delete temp;
            }
        }
};

#endif