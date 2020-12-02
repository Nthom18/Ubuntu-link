#include "Node.h"

Node::Node(int xx, int yy)
{
    x = xx;
    y = yy;
}

std::ostream &operator<<(std::ostream &os, const Node &n)
{
    os << "[" << n.x << ", " << n.y << "]";
    return os;
}

bool Node::operator==(const Node &op)
{
    if( x == op.x & y == op.y)
        return true;
    else
        return false;
}
