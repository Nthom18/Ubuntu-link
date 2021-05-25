import multiprocessing
import time

from main import main
from logger import Logger
from plotCSV_d import plotCSV_d

nr_of_tests = 50
frame_duration = 800

log = Logger('d', 'combined')


def test_d():

    collisions = 0

    for i in range(nr_of_tests):

        print("Test: ", i)
        collisions += main(frame_duration, 'd', i)    # Run simulation

    print('Collisions: ', collisions)
    log.combine_files('data_d', nr_of_tests, frame_duration)

if __name__ == '__main__':
    test_d()
    

        