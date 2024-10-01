#include "./RedBlackTree.h"

void RedBlackTree::generateDOT(const std::string& fileName) {
    std::ofstream file;
    file.open(fileName);

    if (file.is_open()) {
        file << "digraph RedBlackTree {\n";
        file << "    node [shape=circle];\n";

        if (root != nullptr) {
            generateDotFile(root, file);
        }

        file << "}\n";
        file.close();
        std::cout << "File " << fileName << " generated successfully." << std::endl;
    } else {
        std::cerr << "Error opening file: " << fileName << std::endl;
    }
}

void RedBlackTree::Insert(int value) {
    Node* newNode = new Node(value);
    Node* nodeY = nullptr;
    Node* nodeX = root;

    while (nodeX != nullptr) {
        nodeY = nodeX;
        if (newNode->data < nodeX->data) {
            nodeX = nodeX->left;
        }
        else {
            nodeX = nodeX->right;
        }
    }

    newNode->parent = nodeY;

    if (nodeY == nullptr) {
        root = newNode;
    }
    else if (newNode->data < nodeY->data) {
        nodeY->left = newNode;
    }
    else {
        nodeY->right = newNode;
    }

    InsertFix(newNode);
}

void RedBlackTree::remove(int value) {
    Node* nodeZ = root;
    
    while (nodeZ != nullptr) {
        if (value < nodeZ->data) {
            nodeZ = nodeZ->left;
        }
        else if (value > nodeZ->data) {
            nodeZ = nodeZ->right;
        }
        else {
            DeleteNode(nodeZ);
            return;
        }
    }

    std::cout << "Nodo con valor " << value << " no encontrado en el arbol." << std::endl;
}

void RedBlackTree::PrintTree() {
    Print(root, 0);
}

Node* RedBlackTree::Search(int data, int& comparaciones) {
    comparaciones = 0;
    return SearchHelper(root, data, comparaciones);
}