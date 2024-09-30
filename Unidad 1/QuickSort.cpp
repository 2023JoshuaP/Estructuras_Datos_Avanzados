#include <iostream>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <vector>
using namespace std;
using namespace std::chrono;

int Particion(vector<float>& arr, int bajo, int alto) {
    float pivote = arr[alto];
    int i = bajo - 1;

    for (int j = bajo; j <= alto - 1; j++) {
        if (arr[j] < pivote) {
            i++;
            swap(arr[i], arr[j]);
        }
    }

    swap(arr[i + 1], arr[alto]);
    return i + 1;
}

void SortQuick(vector<float>& arr, int bajo, int alto) {
    if (bajo < alto) {
        int pi = Particion(arr, bajo, alto);
        SortQuick(arr, bajo, pi - 1);
        SortQuick(arr, pi + 1, alto);
    }
}

int main() {
    ifstream inputFile("DataGen025.txt");
    vector<float> arr;
    float valor;
    
    while (inputFile >> valor) {
        arr.push_back(valor);
    }

    auto inicio = high_resolution_clock::now();

    SortQuick(arr, 0, arr.size() - 1);

    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);

    cout << fixed << setprecision(6);  // Se fija la precisión a 6 decimales

    cout << duracion.count() << endl;

    cout << "Primeros 10 elementos ordenados:" << endl;
    int end = arr.size() > 10 ? 10 : arr.size();
    for (int i = 0; i < end; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}