#include <cmath>
#include <iostream>
#include <vector>

#include <opencv2/opencv.hpp>

#include "globalDefines.h"

using namespace cv;


Mat Bug0(Mat map, Point start, Point goal);

void calGoalDirection();

Point calCurrentDirection();

Point rotatePoint(Point point);

