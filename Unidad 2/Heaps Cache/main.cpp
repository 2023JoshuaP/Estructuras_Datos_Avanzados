#include <bits/stdc++.h>
#include "./BinaryHeap.cpp"

int main() {
    int arr[] = {9, 5, 6, 2, 3};
    std::vector<int> a(arr, arr + (sizeof(arr) / sizeof(arr[0])));
    std::vector<int> vec;
    vec.push_back(0);

    BinaryHeap* HeapBinary = new BinaryHeap(vec);
    HeapBinary->buildHeap(a);

    std::cout << HeapBinary->delMin() << std::endl;
    std::cout << HeapBinary->delMin() << std::endl;
    std::cout << HeapBinary->delMin() << std::endl;
    std::cout << HeapBinary->delMin() << std::endl;
    std::cout << HeapBinary->delMin() << std::endl;
}