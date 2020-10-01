// Compile this code from terminal:
// g++ main.cpp Bug0.h Bug0.cpp `pkg-config --cflags --libs opencv4`

#include <iostream>
#include <string>

#include <opencv2/opencv.hpp>

#include "globalDefines.h"
#include "Bug0.h"

using namespace cv;



// Prototypes
Point placeDot(Mat image, std::string colorPick);

int main()
{
    /***Read image ***********************************/
    std::string img = "map1.jpg";
    Mat srcImage = imread(img);
    if (!srcImage.data) 
    {
        std::cout << "Error opening image" << std::endl;
        return 1;
    }

    /*** Resize image *******************************/
    Size size(IMAGE_DIMENSION, IMAGE_DIMENSION);
    Mat map;
    resize(srcImage, map, size);

    /*** Generate start and goal ********************/
    Point start = placeDot(map, "green");
    Point goal = placeDot(map, "red");

    // Debug
    std::cout << "Start:   " << start.x << " " << start.y << '\n';
    std::cout << "Goal:    " << goal.x << " " << goal.y << '\n';


    Mat pathMap = Bug0(map, start, goal);


    /*** Show image ********************************/
    // imshow("Map", map);
    imshow("Path", pathMap);
    waitKey(0);

    
    return 0;
}

Point dot()
{
    // initialize random seed:
    srand (time(NULL));

    Point point;
    point.x = rand() % IMAGE_DIMENSION + 1;
    point.y = rand() % IMAGE_DIMENSION + 1;

    return point;
}

Point placeDot(Mat image, std::string colorPick)
{
    Point point;
    Vec3b pixelColor, pointColor;
    
    if(colorPick == "blue")
        pointColor = Vec3b(255,0,0);

    if(colorPick == "green")
        pointColor = Vec3b(0,255,0);

    if(colorPick == "red")
        pointColor = Vec3b(0,0,255);

    while(true)
    {
        point = dot();
        pixelColor = image.at<Vec3b>(point);
        if(pixelColor[0] > BLACK && pixelColor[1] > BLACK && pixelColor[2] > BLACK)
        {            
            circle(image, point, 10, pointColor, -1);
            return point;
        }
    }
}
