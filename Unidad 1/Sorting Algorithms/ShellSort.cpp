#include <iostream>
#include <fstream>
#include <chrono>
#include <vector>
using namespace std;
using namespace std::chrono;

void SortShell(vector<float>& arr) {
    int n = arr.size();
    for (int i = n / 2; i > 0; i /= 2) {
        for (int j = i; j < n; j += 1) {
            int temp = arr[j];
            int k;
            for (k = j; k >= i && arr[k - i] > temp; k -= i) {
                arr[k] = arr[k - i];
            }
            arr[k] = temp;
        }
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

    SortShell(arr);

    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);

    cout << duracion.count() << endl;

    return 0;
}