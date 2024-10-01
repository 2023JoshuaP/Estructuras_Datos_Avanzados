#include <iostream>
#include <chrono>
#include <vector>
#include <iomanip>
#include <fstream>
using namespace std;
using namespace std::chrono;

void SortInsertion(vector<float>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        float clave = arr[i];
        int j = i - 1;
        while (arr[j] > clave && j >= 0) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = clave;
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

    SortInsertion(arr);

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