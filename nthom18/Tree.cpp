#include "Tree.h"

#include <iostream>
#include <iomanip>

#define LONG_STEP 2
#define SHORT_STEP 1
#define MOVES 8

Tree::~Tree()
{
    // // Make vector of root only
    // std::vector<Node*> nodes = {&root};

    // // Compute tree until final node is found
    // iterateDestructor(nodes);
}

Tree::Tree(int BoardHeight, int BoardWidth, int KnightStartXPosition,
           int KnightStartYPosition, int KnightEndXPosition, int KnightEndYPosition)
{
    // Initialize board-sized matrix of zeros (empty board)
    boardXEdge = BoardWidth;
    boardYEdge = BoardHeight;
    initBoardVisits();
    
    // Create node for final position
    finalNode.x = KnightEndXPosition;
    finalNode.y = KnightEndYPosition;

    // Initialize root node
    root.x = KnightStartXPosition;
    root.y = KnightStartYPosition;
    boardVisits[root.x][root.y] = true;


    // Make vector of root only
    std::vector<Node*> nodes = {&root};

    // Compute tree until final node is found
    iterateTree(nodes);


    /********** DEBUG **********/

    // printAllNodes(&root);
    // printBoardVisits();

}

void Tree::iterateTree(std::vector<Node*> nodes)
{
    std::vector<Node*> nodeList;

    for( auto i : nodes )
    {
        exploreMoves(i);
        
        for (int j = 0; j < i->children.size(); j++)
            nodeList.push_back(i->children[j]);
    }

    if( minSteps == 0 )
        iterateTree(nodeList);
}

void Tree::exploreMoves(Node* node)
{
    bool finalNodeFound = false;

    // Move sequence
    static const int x_step[MOVES] = {-SHORT_STEP, SHORT_STEP, LONG_STEP, LONG_STEP, SHORT_STEP, -SHORT_STEP, -LONG_STEP, -LONG_STEP};
    static const int y_step[MOVES] = {-LONG_STEP, -LONG_STEP, -SHORT_STEP, SHORT_STEP, LONG_STEP, LONG_STEP, SHORT_STEP, -SHORT_STEP};

    // Test possible moves, make node if valid
    for(int i = 0; i < MOVES + 1; i++)
    {
        bool within_left_border = (0 <= node->x + x_step[i]);
        bool within_right_border = (node->x + x_step[i] < boardXEdge);
        bool within_upper_border = (0 <= node->y + y_step[i]);
        bool within_lower_border = (node->y + y_step[i] < boardYEdge);

        if( within_left_border & within_right_border & within_upper_border & within_lower_border )
        {
            int newx = node->x + x_step[i];
            int newy = node->y + y_step[i];

            // Check that position hasn't been visited before
            if ( !boardVisits[newx][newy] )
            {
                boardVisits[newx][newy] = true;
                node->children.push_back(new Node(newx, newy));
                
                // If goal has been reached
                if( *node->children.back() == finalNode )
                    finalNodeFound = true;
            }
        }
        // Update height of new nodes
        for( auto i : node->children )
            i->height = node->height + 1;
        
        // Set minSteps to a value that's non-zero, which is the base case for iterateTree()        
        if( finalNodeFound )
            minSteps = node->height + 1;
    }
}

void Tree::initBoardVisits()
{
    // Make empty board
    for( int j = 0; j < boardXEdge; j++ )
    {
        std::vector <bool> row;
        for( int i = 0; i < boardYEdge; i++ )
            row.push_back( false );
        boardVisits.push_back(row);
    }
}

void Tree::printBoardVisits()
{
    for (int i = 0; i < boardVisits.size(); i++) 
    { 
        for (int j = 0; j < boardVisits[i].size(); j++) 
            std::cout << boardVisits[i][j] << " "; 
        std::cout << std::endl; 
    } 
}

void Tree::printAllNodes(Node* node)
{
    for( auto i : node->children )
        std::cout << *i << " " << i->height << "  |  ";

    for( int i = 0; i < node->children.size(); i++ )
        printAllNodes(node->children[i]);
}

void Tree::iterateDestructor(std::vector<Node*> nodes)
{
    std::vector<Node*> nodeList;

    for( auto i : nodes )
    {
        for (int j = 0; j < i->children.size(); j++)
            nodeList.push_back(i->children[j]);
    }
    iterateDestructor(nodeList);
        
    for( auto k : nodeList )
        delete[] k;
}
