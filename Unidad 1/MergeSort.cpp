#include <iostream>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <vector>
using namespace std;
using namespace std::chrono;

void Merge(vector<float>& arr, int izquierda, int medio, int derecha) {
    int n1 = medio - izquierda + 1;
    int n2 = derecha - medio;

    vector<float> L(n1), R(n2);

    for (int i = 0; i < n1; i++) {
        L[i] = arr[izquierda + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = arr[medio + 1 + j];
    }

    int i = 0;
    int j = 0;
    int k = izquierda;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void SortMerge(vector<float>& arr, int izquierda, int derecha) {
    if (izquierda >= derecha) {
        return;
    }
    int medio = izquierda + (derecha - izquierda) / 2;
    SortMerge(arr, izquierda, medio);
    SortMerge(arr, medio + 1, derecha);
    Merge(arr, izquierda, medio, derecha);
}

int main() {
    ifstream inputFile("DataGen025.txt");
    vector<float> arr;
    float valor;
    
    while (inputFile >> valor) {
        arr.push_back(valor);
    }

    auto inicio = high_resolution_clock::now();

    SortMerge(arr, 0, arr.size() - 1);

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