#ifndef Node_H
#define Node_H

#include <iostream>
#include <vector>

class Node {
public:
    Node(){}
    Node(int xx, int yy);
    ~Node(){}

    int x = 0;
    int y = 0;
    int height = 0;
    std::vector<Node*> children;

    friend std::ostream &operator<<(std::ostream &os, const Node &n);

    bool operator==(const Node &op);

private:

};
#endif