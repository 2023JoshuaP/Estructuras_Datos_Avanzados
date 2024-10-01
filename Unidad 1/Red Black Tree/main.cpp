#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include "./RedBlackTree.cpp"

int main() {
    std::vector<int> keys;
    std::srand(std::time(0));

    for (int n = 100; n <= 10000; n *= 10) {
        RedBlackTree RBTree;
        keys.clear();

        for (int i = 1; i <= n; i++) {
            keys.push_back(i);
            RBTree.Insert(i);
        }
        
        int comparaciones_totales = 0;
        int repeticiones = 100;

        for (int i = 0; i < repeticiones; i++) {
            int claves_random = keys[std::rand() % n];
            int comparaciones = 0;
            RBTree.Search(claves_random, comparaciones);
            comparaciones_totales += comparaciones;
        }

        double promedio_comparaciones = comparaciones_totales / (double)repeticiones;
        std::cout << "Numero de claves: " << n << " | Comparaciones promedio: " << promedio_comparaciones << std::endl;
    }

    return 0;
}