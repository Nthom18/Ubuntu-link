#ifndef TREE_H
#define TREE_H

#include <iostream>
#include <vector>

#include "Node.h"

class Tree {
public:
    Tree(){}
    Tree(int BoardHeight, int BoardWidth, int KnightStartXPosition,
         int KnightStartYPosition, int KnightEndXPosition, int KnightEndYPosition);
    ~Tree();

    int minSteps = 0;

private:
    
    Node root;
    Node finalNode;
    std::vector<std::vector<bool>> boardVisits;

    int boardXEdge = 0;
    int boardYEdge = 0;

    void iterateTree(std::vector<Node*> nodeList);

    void exploreMoves(Node* node);

    void makeNode(Node* parent, int xStep, int yStep);

    void initBoardVisits();

    void printBoardVisits();

    void printAllNodes(Node* node);

    void iterateDestructor(std::vector<Node*> nodes);
};
#endif
