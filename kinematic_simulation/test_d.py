import multiprocessing
import time

from main import main

nr_of_tests = 2
frame_duration = 800


if __name__ == '__main__':

    for i in range(nr_of_tests):

        print("Test: ", i)
        main(frame_duration, 'd', i)


    


