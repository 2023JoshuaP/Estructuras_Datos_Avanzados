#include "./BinaryHeap.h"

void BinaryHeap::percUp(int i) {
    while ((i / 2) > 0) {
        if (this->heapVector[i] < this->heapVector[i/2]) {
            int tmp = this->heapVector[i/2];
            this->heapVector[i/2] = this->heapVector[i];
            this->heapVector[i] = tmp;
        }
        i = i / 2;
    }
}

void BinaryHeap::insert(int k) {
    this->heapVector.push_back(k);
    this->currentSize = this->currentSize + 1;
    this->percUp(this->currentSize);
}

void BinaryHeap::percDown(int i) {
    while ((i * 2) <= this->currentSize) {
        int mc = this->minChild(i);
        if (this->heapVector[i] > this->heapVector[mc]) {
            int tmp = this->heapVector[i];
            this->heapVector[i] = this->heapVector[mc];
            this->heapVector[mc] = tmp;
        }
        i = mc;
    }
}

int BinaryHeap::minChild(int i) {
    if (((i * 2) + 1) > this->currentSize) {
        return i * 2;
    }
    else {
        if (this->heapVector[i*2] < this->heapVector[(i*2)+1]) {
            return i * 2;
        }
        else {
            return (i * 2) + 1;
        }
    }
}

int BinaryHeap::delMin() {
    int retval = this->heapVector[1];
    this->heapVector[1] = this->heapVector[this->currentSize];
    this->currentSize = this->currentSize - 1;
    this->heapVector.pop_back();
    this->percDown(1);
    return retval;
}

void BinaryHeap::buildHeap(std::vector<int> avector) {
    int i = avector.size() / 2;
    this->currentSize = avector.size();
    this->heapVector.insert(this->heapVector.end(), avector.begin(), avector.end());
    while (i > 0) {
        this->percDown(i);;
        i = i - 1;
    }
}

bool BinaryHeap::isEmpty() {
    if (this->heapVector.size() > 0) {
        return false;
    }
    return true;
}

int BinaryHeap::findMin() {
    return this->heapVector[1];
}