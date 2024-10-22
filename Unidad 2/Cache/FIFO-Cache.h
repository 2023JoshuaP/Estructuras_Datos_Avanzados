#ifndef FIFO_CACHE_H
#define FIFO_CACHE_H

#include <iostream>
#include <unordered_map>

class Cola {
    struct Nodo {
        int dato;
        Nodo* siguiente;
        Nodo(int dato) : dato(dato), siguiente(nullptr) {}
    };

    Nodo* primero;
    Nodo* ultimo;

    public:
        Cola() : primero(nullptr), ultimo(nullptr) {}

        void push(int dato) {
            Nodo* nuevo = new Nodo(dato);
            if (primero == nullptr) {
                primero = nuevo;
                ultimo = nuevo;
            } else {
                ultimo->siguiente = nuevo;
                ultimo = nuevo;
            }
        }

        int pop() {
            if (primero == nullptr) {
                return -1;
            }

            int dato = primero->dato;
            Nodo* temp = primero;
            primero = primero->siguiente;
            delete temp;
            return dato;
        }

        int front() {
            if (primero == nullptr) {
                return -1;
            }
            return primero->dato;
        }

        bool empty() {
            return primero == nullptr;
        }
};

class FIFOCache {
    private:
        std::unordered_map<int, int> cache;
        Cola cola;
        int capacidad;
    public:
        FIFOCache(int capacidad) : capacidad(capacidad) {}

        int get(int key);
        void put(int key, int value);
        void display();
};

#endif