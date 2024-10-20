#ifndef BINARY_HEAP
#define BINARY_HEAP

#include <bits/stdc++.h>

class BinaryHeap {
    private:
        std::vector<int> heapVector;
        int currentSize;
    public:
        BinaryHeap(std::vector<int> heapVector) {
            this->heapVector = heapVector;
            this->currentSize = 0;
        }
        void percUp(int i);
        void insert(int k);
        void percDown(int i);
        int minChild(int i);
        int delMin();
        void buildHeap(std::vector<int> avector);
        bool isEmpty();
        int findMin();
};

#endif