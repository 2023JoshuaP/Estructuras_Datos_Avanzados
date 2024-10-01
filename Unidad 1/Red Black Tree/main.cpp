#include <iostream>
#include "./RedBlackTree.cpp"

int main() {
    RedBlackTree RBTree;

    RBTree.Insert(10);
    RBTree.Insert(5);
    RBTree.Insert(15);
    RBTree.Insert(3);
    RBTree.Insert(7);
    RBTree.Insert(12);
    RBTree.Insert(18);
    RBTree.Insert(1);
    
    std::cout << "Estructura del Red Black Tree:" << std::endl;
    RBTree.PrintTree();

    RBTree.generateDOT("RedBlackTree.dot");
    
    /*
    RBTree.remove(5);

    std::cout << "Despues de eliminar el nodo 5:" << std::endl;
    RBTree.PrintTree();
    */

    std::cout << "Buscando nodo 15: " << (RBTree.Search(15) != RBTree.Search(0)) << std::endl;
    std::cout << "Buscando nodo 25: " << (RBTree.Search(25) != RBTree.Search(0)) << std::endl;
    return 0;
}