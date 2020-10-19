// Compile this code from terminal:
// g++ main.cpp `pkg-config --cflags --libs opencv4`

#include <iostream>
#include <string>

#include <opencv2/opencv.hpp>

#include "globalDefines.h"

using namespace cv;

int main()
{
    
    for(int i = 1; i < NUM_IMAGES + 1; i++)
    {
        /***Read images **********************************/
        std::string img = "../images/ORings/ORing";
        if(i < 10)
            img += "0";
        img += std::to_string(i) + ".jpg";        

        Mat srcImg = imread(img);
        if (!srcImg.data) 
        {
            std::cout << "Error opening image" << std::endl;
            return 1;
        }

        /*** Resize image *******************************/
        Size size(IMAGE_DIMENSION, IMAGE_DIMENSION);
        Mat image;
        resize(srcImg, image, size);

        /*** Binary image *******************************/
        Mat binImg;
        threshold(image, binImg, 150, 255, THRESH_BINARY);

        /*** Dilate and erode image *********************/
        Mat erodeImg = ~binImg.clone();
        dilate(erodeImg, erodeImg, getStructuringElement(MORPH_RECT, Size(3, 3)));
        
        for(int j = 0; j < 5; j++)
            erode(erodeImg, erodeImg, getStructuringElement(MORPH_RECT, Size(3, 3)));


        /*** Show image *********************************/
        imshow("Image " + std::to_string(i), erodeImg);
        waitKey(0);
    }

    return 0;
}