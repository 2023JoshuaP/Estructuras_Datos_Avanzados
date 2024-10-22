#include <iostream>
#include "./LRU-Cache.cpp"
#include "./LFU-Cache.cpp"
#include "./FIFO-Cache.cpp"

void showMenuLRU() {
    std::cout << "\n--- LRU Cache Menu ---\n";
    std::cout << "1. PUT (Agregar/Actualizar un valor)\n";
    std::cout << "2. GET (Obtener un valor)\n";
    std::cout << "3. EXIT (Salir)\n";
    std::cout << "Elija una opcion: ";
}

void showMenuLFU() {
    std::cout << "\n--- LFU Cache Menu ---\n";
    std::cout << "1. PUT (Agregar/Actualizar un valor)\n";
    std::cout << "2. GET (Obtener un valor)\n";
    std::cout << "3. EXIT (Salir)\n";
    std::cout << "Elija una opcion: ";
}

void showMenuFIFO() {
    std::cout << "\n--- FIFO Cache Menu ---\n";
    std::cout << "1. PUT (Agregar/Actualizar un valor)\n";
    std::cout << "2. GET (Obtener un valor)\n";
    std::cout << "3. EXIT (Salir)\n";
    std::cout << "Elija una opcion: ";
}

int main() {
    int cacheSize;
    int optionCache;

    std::cout << "Ingrese la capacidad del LRU Cache: ";
    std::cin >> cacheSize;
    std::cout << "Selecciona el tipo de cache:\n";
    std::cout << "1. LRU Cache\n";
    std::cout << "2. LFU Cache\n";
    std::cout << "3. FIFO Cache\n";
    std::cout << "Elija una opcion: ";
    std::cin >> optionCache;

    if (optionCache == 1) {
        LRUCache lru(cacheSize);
        int key, value;
        int option;
        do {
            showMenuLRU();
            std::cin >> option;
            switch (option) {
                case 1:
                    std::cout << "Ingrese la clave y el valor a agregar: ";
                    std::cin >> key >> value;
                    lru.put(key, value);
                    lru.display();
                    break;
                case 2:
                    std::cout << "Ingrese la clave a buscar: ";
                    std::cin >> key;
                    std::cout << "El valor es: " << lru.get(key) << std::endl;
                    lru.display();
                    break;
                case 3:
                    std::cout << "Saliendo del programa...\n";
                    break;
                default:
                    std::cout << "Opcion invalida\n";
            }
        } while (option != 3);
    } else if (optionCache == 2) {
        LFUCache lfu(cacheSize);
        int key, value;
        int option;
        do {
            showMenuLFU();
            std::cin >> option;
            switch (option) {
                case 1:
                    std::cout << "Ingrese la clave y el valor a agregar: ";
                    std::cin >> key >> value;
                    lfu.put(key, value);
                    lfu.display();
                    break;
                case 2:
                    std::cout << "Ingrese la clave a buscar: ";
                    std::cin >> key;
                    std::cout << "El valor es: " << lfu.get(key) << std::endl;
                    lfu.display();
                    break;
                case 3:
                    std::cout << "Saliendo del programa...\n";
                    break;
                default:
                    std::cout << "Opcion invalida\n";
            }
        } while (option != 3);
    } else if (optionCache == 3) {
        FIFOCache fifo(cacheSize);
        int key, value;
        int option;
        do {
            showMenuFIFO();
            std::cin >> option;
            switch (option) {
                case 1:
                    std::cout << "Ingrese la clave y el valor a agregar: ";
                    std::cin >> key >> value;
                    fifo.put(key, value);
                    fifo.display();
                    break;
                case 2:
                    std::cout << "Ingrese la clave a buscar: ";
                    std::cin >> key;
                    std::cout << "El valor es: " << fifo.get(key) << std::endl;
                    fifo.display();
                case 3:
                    std::cout << "Saliendo del programa...\n";
                    break;
            }
        } while (option != 3);
    }
    return 0;
}
