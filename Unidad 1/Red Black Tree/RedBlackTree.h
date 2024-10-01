#ifndef REDBLACKTREE_H
#define REDBLACKTREE_H

#include <iostream>
#include <fstream>

enum Color {RED, BLACK};

struct Node {
    int data;
    Color color;
    Node* left;
    Node* right;
    Node* parent;

    explicit Node(int value) : data(value), color(RED), left(nullptr), right(nullptr), parent(nullptr) {}
};

class RedBlackTree {
    public:
        Node* root;
        void RotateLeft(Node* nodeX) {
            if (nodeX == nullptr || nodeX->right == nullptr) {
                return;
            }

            Node* nodeY = nodeX->right;
            nodeX->right = nodeY->left;
            
            if (nodeY->left != nullptr) {
                nodeY->left->parent = nodeX;
            }

            nodeY->parent = nodeX->parent;

            if (nodeX->parent == nullptr) {
                root = nodeY;
            }
            else if (nodeX == nodeX->parent->left) {
                nodeX->parent->left = nodeY;
            }
            else {
                nodeX->parent->right = nodeY;
            }
            nodeY->left = nodeX;
            nodeX->parent = nodeY;
        }

        void RotateRight(Node* nodeY) {
            if (nodeY == nullptr || nodeY->left == nullptr) {
                return;
            }

            Node* nodeX = nodeY->left;
            nodeY->left = nodeX->right;
            
            if (nodeX->right != nullptr) {
                nodeX->right->parent = nodeY;
            }

            nodeX->parent = nodeY->parent;

            if (nodeY->parent == nullptr) {
                root = nodeX;
            }
            else if (nodeY == nodeY->parent->left) {
                nodeY->parent->left = nodeX;
            }
            else {
                nodeY->parent->right = nodeX;
            }
            nodeX->right = nodeY;
            nodeY->parent = nodeX;
        }

        void InsertFix(Node* nodeZ) {
            while (nodeZ != root && nodeZ->parent->color == RED) {
                if (nodeZ->parent == nodeZ->parent->parent->left) {
                    Node* nodeY = nodeZ->parent->parent->right;
                    if (nodeY != nullptr && nodeY->color == RED) {
                        nodeZ->parent->color = BLACK;
                        nodeY->color = BLACK;
                        nodeZ->parent->parent->color = RED;
                        nodeZ = nodeZ->parent->parent;
                    }
                    else {
                        if (nodeZ == nodeZ->right->parent) {
                            nodeZ = nodeZ->parent;
                            RotateLeft(nodeZ);
                        }
                        nodeZ->parent->color = BLACK;
                        nodeZ->parent->parent->color = RED;
                        RotateRight(nodeZ->parent->parent);
                    }
                }
                else {
                    Node* nodeY = nodeZ->parent->parent->left;
                    if (nodeY != nullptr && nodeY->color == RED) {
                        nodeZ->parent->color = BLACK;
                        nodeY->color = BLACK;
                        nodeZ->parent->parent->color = RED;
                        nodeZ = nodeZ->parent->parent;
                    }
                    else {
                        if (nodeZ == nodeZ->parent) {
                            nodeZ = nodeZ->parent;
                            RotateRight(nodeZ);
                        }
                        nodeZ->parent->color = BLACK;
                        nodeZ->parent->parent->color = RED;
                        RotateLeft(nodeZ->parent->parent);
                    }
                }
            }
            root->color = BLACK;
        }

        void Transplant(Node* nodeU, Node* nodeV) {
            if (nodeU->parent == nullptr) {
                root = nodeV;
            }
            else if (nodeU == nodeU->parent->left) {
                nodeU->parent->left = nodeV;
            }
            else {
                nodeU->parent->right = nodeV;
            }

            if (nodeV != nullptr) {
                nodeV->parent = nodeU->parent;
            }
        }
        
        void DeleteNode(Node* nodeZ) {
            if (nodeZ == nullptr) {
                return;
            }

            Node* nodeY = nodeZ;
            Node* nodeX = nullptr;
            Color y_color_original = nodeY->color;

            if (nodeZ->left == nullptr) {
                nodeX = nodeZ->right;
                Transplant(nodeZ, nodeZ->right);
            }
            else if (nodeZ->right == nullptr) {
                nodeX = nodeZ->left;
                Transplant(nodeZ, nodeZ->left);
            }
            else {
                nodeY = Minimun(nodeZ->right);
                y_color_original = nodeY->color;
                nodeX = nodeY->right;

                if (nodeY->parent == nodeZ) {
                    if (nodeX != nullptr) {
                        nodeX->parent = nodeY;
                    }
                }
                else {
                    if (nodeX != nullptr) {
                        nodeX->parent = nodeY->parent;
                    }
                    
                    Transplant(nodeY, nodeY->right);
                    
                    if (nodeY->right != nullptr) {
                        nodeY->right->parent = nodeY;
                    }

                    nodeY->right = nodeZ->right;

                    if (nodeY->right != nullptr) {
                        nodeY->right->parent = nodeY;
                    }
                }

                Transplant(nodeZ, nodeY);
                nodeY->left = nodeZ->left;

                if (nodeY->left != nullptr) {
                    nodeY->left->parent = nodeY;
                }

                nodeY->color = nodeZ->color;
            }
            
            if (y_color_original == BLACK && nodeX != nullptr) {
                DeleteFix(nodeX);
            }

            delete nodeZ;
        }
        
        void DeleteFix(Node* nodeX) {
            while (nodeX != root && nodeX != nullptr && nodeX->color == BLACK) {
                if (nodeX == nodeX->parent->left) {
                    Node* nodeW = nodeX->parent->right;
                    if (nodeW->color == RED) {
                        nodeW->color = BLACK;
                        nodeX->parent->color = RED;
                        RotateLeft(nodeX->parent);
                        nodeW = nodeX->parent->right;
                    }

                    if ((nodeW->left == nullptr || nodeW->left->color == BLACK) && (nodeW->right == nullptr || nodeW->right->color == BLACK)) {
                        nodeW->color = RED;
                        nodeX = nodeX->parent;
                    }
                    else {
                        if (nodeW->right == nullptr || nodeW->right->color == BLACK) {
                            if (nodeW->left != nullptr) {
                                nodeW->left->color = BLACK;
                            }
                            nodeW->color = RED;
                            RotateRight(nodeW);
                            nodeW = nodeX->parent->right;
                        }

                        nodeW->color = nodeX->parent->color;
                        nodeX->parent->color = BLACK;

                        if (nodeW->right != nullptr) {
                            nodeW->right->color = BLACK;
                        }

                        RotateLeft(nodeX->parent);
                        nodeX = root;
                    }
                }
                else {
                    Node* nodeW = nodeX->parent->left;
                    if (nodeW->color == RED) {
                        nodeW->color = BLACK;
                        nodeX->parent->color = RED;
                        RotateRight(nodeX->parent);
                        nodeW = nodeX->parent->left;
                    }
                    
                    if ((nodeW->right == nullptr || nodeW->right->color == BLACK) && (nodeW->left == nullptr || nodeW->left->color == BLACK)) {
                        nodeW->color = RED;
                        nodeX = nodeX->parent;
                    }
                    else {
                        if (nodeW->left == nullptr || nodeW->left->color == BLACK) {
                            if (nodeW->right != nullptr) {
                                nodeW->right->color = BLACK;
                            }
                            nodeW->color = RED;
                            RotateLeft(nodeW);
                            nodeW = nodeX->parent->left;
                        }

                        nodeW->color = nodeX->parent->color;
                        nodeX->parent->color = BLACK;

                        if (nodeW->left != nullptr) {
                            nodeW->left->color = BLACK;
                        }

                        RotateRight(nodeX->parent);
                        nodeX = root;
                    }
                }
            }
            if (nodeX != nullptr) {
                nodeX->color = BLACK;
            }
        }
        
        Node* Minimun(Node* node) {
            while (node->left != nullptr) {
                node = node->left;
            }
            return node;
        }
        
        void Print(Node* root, int space) {
            constexpr int COUNT = 5;

            if (root == nullptr) {
                return;
            }
            
            space += COUNT;
            Print(root->right, space);
            std::cout << std::endl;
            
            for (int i = COUNT; i < space; i++) {
                std::cout << " ";
            }

            std::cout << root->data << "(" << ((root->color == RED) ? "RED" : "BLACK") << ")" << std::endl;
            Print(root->left, space);
        }

        Node* SearchHelper(Node* node, int data, int& comparaciones) {
            comparaciones++;

            if (node == nullptr) {
                //std::cout << "Clave " << data << " no encontrada despues de " << comparaciones << " comparaciones." << std::endl;
                return node;
            }
            else if (data == node->data) {
                //std::cout << "Clave " << data << " encontrada en el nodo " << node->data  << " despues de " << comparaciones << " comparaciones." << std::endl;
                return node;
            }

            if (data < node->data) {
                //std::cout << "Buscando a la izquierda del nodo " << node->data << std::endl;
                return SearchHelper(node->left, data, comparaciones);
            }
            
            //std::cout << "Buscando a la derecha del nodo " << node->data << std::endl;
            return SearchHelper(node->right, data, comparaciones);
        }

        void generateDotFile(Node* node, std::ofstream& file) {
            if (node == nullptr) return;

            file << "    \"" << node->data << "\" [label=\"" << node->data << "\", color="
                << (node->color == RED ? "red" : "black") << ", fontcolor="
                << (node->color == RED ? "red" : "black") << "];\n";

            if (node->left != nullptr) {
                file << "    \"" << node->data << "\" -> \"" << node->left->data << "\";\n";
                generateDotFile(node->left, file);
            }

            if (node->right != nullptr) {
                file << "    \"" << node->data << "\" -> \"" << node->right->data << "\";\n";
                generateDotFile(node->right, file);
            }
        }
    public:
        RedBlackTree() : root(nullptr) {}
        void generateDOT(const std::string& fileName);
        void Insert(int value);
        void remove(int value);
        void PrintTree();
        Node* Search(int data, int& comparaciones);
};

#endif