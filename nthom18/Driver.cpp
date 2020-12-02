#include "Driver.h"

#include <iostream>

int MinimumSteps(int BoardHeight, int BoardWidth, int KnightStartXPosition,
int KnightStartYPosition, int KnightEndXPosition, int KnightEndYPosition)
{
    if( failsafe( BoardHeight, BoardWidth, KnightStartXPosition,
                  KnightStartYPosition, KnightEndXPosition, KnightEndYPosition) )
    {
        Tree Board(BoardHeight, BoardWidth, KnightStartXPosition, KnightStartYPosition, KnightEndXPosition, KnightEndYPosition);
        return Board.minSteps;
    }
    return -1;
}

bool failsafe(int BoardHeight, int BoardWidth, int KnightStartXPosition,
int KnightStartYPosition, int KnightEndXPosition, int KnightEndYPosition)
{
    // "Assertions"
    if( KnightStartXPosition == KnightEndXPosition & KnightStartYPosition == KnightEndYPosition )
    {
        std::cout << '\n' << "Start and end has to be different!" << std::endl;
        return false;        
    }
    if( BoardHeight != BoardWidth )
    {
        std::cout << '\n' << "Board is not square!" << std::endl;
        return false;        
    }
    if( BoardHeight > 5000 )
    {
        std::cout << '\n' << "Board is too big!" << std::endl;
        return false;;
    }
    if( BoardHeight < 5 )
    {
        std::cout << '\n' << "Board is too small!" << std::endl;
        return false;;
    }
    if( KnightStartXPosition < 0 | KnightStartXPosition > BoardWidth - 1 )
    {
        std::cout << '\n' << "Start x is out of bounds!" << std::endl;
        return false;;
    }
    if( KnightStartYPosition < 0 | KnightStartYPosition > BoardHeight - 1 )
    {
        std::cout << '\n' << "Start y is out of bounds!" << std::endl;
        return false;;
    }
    if( KnightEndXPosition < 0 | KnightEndXPosition > BoardWidth - 1 )
    {
        std::cout << '\n' << "End x is out of bounds!" << std::endl;
        return false;;
    }
    if( KnightEndYPosition < 0 | KnightEndYPosition > BoardHeight - 1 )
    {
        std::cout << '\n' << "End y is out of bounds!" << std::endl;
        return false;;
    }
    return true;
}