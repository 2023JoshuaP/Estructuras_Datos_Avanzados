#include <iostream>
#include <chrono>
#include <fstream>
#include <vector>
using namespace std;
using namespace std::chrono;

void SortBubble(vector<float>& arr) {
    int n = arr.size();
    int i, j;
    bool swaped;
    for (i = 0; i < n - 1; i++) {
        swaped = false;
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                float temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swaped = true;
            }
        }
        if (swaped == false) {
            break;
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

    //SortBubble(arr);

    auto fin = high_resolution_clock::now();

    auto duracion = duration_cast<microseconds>(fin - inicio);

    cout << duracion.count() << endl;
    return 0;
}