#include <stdio.h>
#include "./FibHeap.h"

//Add dotty output to our heap, which produces nice diagrams
class DotFibonacciHeap : public FibonacciHeap<int> {
public:
	void dump() {
		printf("digraph G {\n");
		if(heap==NULL) {
			printf("empty;\n}\n");
			return;
		}
		printf("minimum -> \"%p\" [constraint=false];\n",heap);
		node<int>* c=heap;
		do {
			_dumpChildren(c);
			c=c->getNext();
		} while(c!=heap);
		printf("}\n");
	}

private:

	void _dumpChildren(node<int>* n) {
		printf("\"%p\" -> \"%p\" [constraint=false,arrowhead=lnormal];\n",n,n->getNext());
		printf("\"%p\" -> \"%p\" [constraint=false,arrowhead=ornormal];\n",n,n->getPrev());
		if(n->isMarked())printf("\"%p\" [style=filled,fillcolor=grey];\n",n);
		if(n->hasParent()) {
			printf("\"%p\" -> \"%p\" [constraint=false,arrowhead=onormal];\n",n,n->getParent());
		}
		printf("\"%p\" [label=%d];\n",n,n->getValue());
		if(n->hasChildren()) {
			node<int>* c=n->getChild();
			do {
				printf("\"%p\" -> \"%p\";\n",n,c);
				_dumpChildren(c);
				c=c->getNext();
			} while(c!=n->getChild());
		}
	}
};


void test() {
	DotFibonacciHeap h;
	/*
    h.insert(2);
	h.insert(3);
	h.insert(1);
	h.insert(4);
	h.removeMinimum();
	h.removeMinimum();
	h.insert(5);
	h.insert(7);
	h.removeMinimum();
	h.insert(2);
	node<int>* nine=h.insert(90);
	h.removeMinimum();
	h.removeMinimum();
	h.removeMinimum();
	for(int i=0;i<20;i+=2)h.insert(30-i);
	for(int i=0;i<4;i++)h.removeMinimum();
	for(int i=0;i<20;i+=2)h.insert(30-i);
	h.insert(23);
	for(int i=0;i<7;i++)h.removeMinimum();
	h.decreaseKey(nine,1);
	h.decreaseKey(h.find(28),2);
	h.decreaseKey(h.find(23),3);
    */
    h.insert(2);
    h.insert(3);
    h.insert(1);
    h.insert(4);
    h.insert(5);
    h.insert(7);
	h.dump();
}

int main() {
	test();
}