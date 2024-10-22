#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <cmath>
#include <numeric>
#include <chrono>
#include "./RedBlackTree.cpp"

int main() {
    std::ofstream file("Resultados_tiempo.csv");
    file << "Numero de Claves,Comparaciones Promedio,Desviacion Estandar,Tiempo Promedio (ns)\n";

    std::vector<int> keys;
    std::srand(std::time(0));

    const int num_experimentos = 5;
    for (int n = 100; n <= 10000; n += 100) {
        std::vector<double> comparaciones_acumuladas;
        std::vector<double> tiempos_acumulados;

        for (int experimento = 0; experimento < num_experimentos; ++experimento) {
            RedBlackTree RBTree;
            keys.clear();

            for (int i = 1; i <= n; i++) {
                keys.push_back(i);
                RBTree.Insert(i);
            }

            int comparaciones_totales = 0;
            int repeticiones = 100;
            double tiempo_total = 0.0;

            for (int i = 0; i < repeticiones; i++) {
                int claves_random = keys[std::rand() % n];
                int comparaciones = 0;

                auto inicio = std::chrono::high_resolution_clock::now();
                RBTree.Search(claves_random, comparaciones);
                auto fin = std::chrono::high_resolution_clock::now();
                std::chrono::duration<double, std::nano> duracion = fin - inicio;

                comparaciones_totales += comparaciones;
                tiempo_total += duracion.count();
            }

            double promedio_comparaciones = comparaciones_totales / (double)repeticiones;
            double tiempo_promedio = tiempo_total / repeticiones;

            comparaciones_acumuladas.push_back(promedio_comparaciones);
            tiempos_acumulados.push_back(tiempo_promedio);
        }

        double promedio_comparaciones_total = std::accumulate(comparaciones_acumuladas.begin(), comparaciones_acumuladas.end(), 0.0) / num_experimentos;
        double promedio_tiempo_total = std::accumulate(tiempos_acumulados.begin(), tiempos_acumulados.end(), 0.0) / num_experimentos;
        double suma_diferencias_cuadrado = 0.0;

        for (const auto& valor : comparaciones_acumuladas) {
            suma_diferencias_cuadrado += (valor - promedio_comparaciones_total) * (valor - promedio_comparaciones_total);
        }
        double desviacion_estandar = std::sqrt(suma_diferencias_cuadrado / num_experimentos);

        file << n << "," << promedio_comparaciones_total << "," << desviacion_estandar << "," << promedio_tiempo_total << "\n";
    }

    file.close();
    return 0;
}