/*
Due to rounding error (Points are ints), the goalDirection might not be accurate, 
but will at closer distances change to the correct direction.
*/

#include "Bug0.h"

// Path
Mat pathMap;
std::vector<Point> path;
// Vectors
Point goalDirection, currentDirection;
int goalDistance;
// Coordinates
Point startPos, goalPos, currentPos;


Mat Bug0(Mat map, Point start, Point goal)
{
    // Load values into global variables
    startPos = start;
    goalPos = goal;
    currentPos = start;
    pathMap = map;
    
    // Initiate path
    path.push_back(start);

    calGoalDirection();
    std::cout << "goal direction: " << goalDirection << "    distance: " << goalDistance << std::endl;

    // Find path to goal
    while(goalDistance > STEP_SIZE)
    {
        calGoalDirection();        
        currentDirection = calCurrentDirection();

        path.push_back(currentPos);

        // Mark current position
        circle(pathMap, currentPos, 3, Vec3b(255, 0, 0), -1);

    }

    // Draw path
    for(int i = 0; i < path.size() - 1; ++i)
    {   
        cv::line(pathMap, path[i], path[i + 1], Vec3b(255, 0, 0), 2);
    }

    return pathMap;
}

void calGoalDirection()
{
    goalDirection.x = goalPos.x - currentPos.x;
    goalDirection.y = goalPos.y - currentPos.y;

    goalDistance = sqrt(pow(goalDirection.x, 2) + pow(goalDirection.y, 2));
}

Point calCurrentDirection()
{
    static Point nextStep;
    static Point directionGoal, directionCurrent;
    static Vec3b pixelColor;
    
    // If no obstacle in the way, take step towards goal
    directionGoal = Point(goalDirection.x * STEP_SIZE / goalDistance, goalDirection.y * STEP_SIZE / goalDistance);
        
    nextStep = currentPos + directionGoal;
    pixelColor = pathMap.at<Vec3b>(nextStep);
    
    if(pixelColor[0] > BLACK && pixelColor[1] > BLACK && pixelColor[2] > BLACK)
    {            
            currentPos = nextStep;
            return directionGoal;
    }
    else
    {
        nextStep = currentPos - directionGoal;
    }
    

    // If no obstacle in the way, take step towards current direction
    directionCurrent = currentDirection;
    nextStep = currentPos + directionCurrent;
    pixelColor = pathMap.at<Vec3b>(nextStep);
    
    if(pixelColor[0] > BLACK && pixelColor[1] > BLACK && pixelColor[2] > BLACK)
    {            
            currentPos = nextStep;
            return directionCurrent;
    }
    else
    {
        nextStep = currentPos - directionGoal;
    }


    // Check for obstacle 30 (in globalDefines.h) degrees counter-clockwise
    while(true)
    {
        nextStep = rotatePoint(nextStep);
        pixelColor = pathMap.at<Vec3b>(nextStep);
        if(pixelColor[0] > BLACK && pixelColor[1] > BLACK && pixelColor[2] > BLACK)
        {  
            directionCurrent.x = nextStep.x - currentPos.x;
            directionCurrent.y = nextStep.y - currentPos.y;
            currentPos = nextStep;
            return directionCurrent;
        }
    }
}

Point rotatePoint(Point point)
{
    static const int angle = M_PI / 8;
    static Point rotatedPoint;

    rotatedPoint.x = point.x * cos(0.4) - point.y * sin(0.4);
    rotatedPoint.y = point.x * sin(0.4) + point.y * cos(0.4);
    
    return rotatedPoint;
}
