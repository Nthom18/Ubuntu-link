'''
Running case scenario of case d).

Author: Nicoline Louise Thomsen
'''

from main import main
from logger import Logger

flock_size = 5
nr_of_tests = 50
frame_duration = 800

log = Logger('d', 'combined', flock_size)


def test_d():

    collisions = 0

    for i in range(nr_of_tests):

        print("Test: ", i)
        collisions += main(frame_duration, 'd', i, flock_size)    # Run simulation

    print('\n', 'Collisions: ', collisions)
    log.combine_files('data_d', nr_of_tests, frame_duration)

if __name__ == '__main__':
    test_d()
