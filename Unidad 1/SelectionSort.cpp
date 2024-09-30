#include <iostream>
#include <chrono>
#include <vector>
#include <fstream>
using namespace std;
using namespace std::chrono;

void SortSelection(vector<float>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        int idxMinimo = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[idxMinimo]) {
                idxMinimo = j;
            }
        }
        if (idxMinimo != i) {
            swap(arr[idxMinimo], arr[i]);
        }
    }
}

int main() {
    ifstream inputFile("DataGen025.txt");
    vector<float> arr;
    float valor;
    int count = 0;
    
    while (inputFile >> valor && count < 250000) {
        arr.push_back(valor);
        count++;
    }

    auto inicio = high_resolution_clock::now();

    SortSelection(arr);

    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);

    cout << duracion.count() << endl;
    return 0;
}