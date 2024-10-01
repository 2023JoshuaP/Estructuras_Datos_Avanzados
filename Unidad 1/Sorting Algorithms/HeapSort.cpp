#include <iostream>
#include <chrono>
#include <fstream>
#include <vector>
using namespace std;
using namespace std::chrono;

void Heapify(vector<float>& arr, int n, int i) {
    int largest = i;
    int izquierda = 2 * i + 1;
    int derecha = 2 * i + 2;

    if (izquierda < n && arr[izquierda] > arr[largest]) {
        largest = izquierda;
    }
    if (derecha < n && arr[derecha] > arr[largest]) {
        largest = derecha;
    }
    if (largest != i) {
        swap(arr[i], arr[largest]);
        Heapify(arr, n, largest);
    }
}

void SortHeap(vector<float>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--) {
        Heapify(arr, n, i);
    }
    for (int i = n - 1; i >= 0; i--) {
        swap(arr[0], arr[i]);
        Heapify(arr, n, 0);
    }
}

int main() {
    ifstream inputFile("DataGen1.txt");
    vector<float> arr;
    float valor;
    
    while (inputFile >> valor) {
        arr.push_back(valor);
    }

    auto inicio = high_resolution_clock::now();

    SortHeap(arr);

    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);

    cout << duracion.count() << endl;
    return 0;
}