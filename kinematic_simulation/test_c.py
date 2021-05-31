'''
Running case scenario of case c).

Author: Nicoline Louise Thomsen
'''

from main import main

nr_of_tests = 10
flock_size = 7

def test_c():

    collisions = 0

    for i in range(nr_of_tests):
        
        print("Test: ", i)
        collisions += main(-1, 'c', i, flock_size)    # Run simulation

    print('\n', 'Collisions: ', collisions)

if __name__ == '__main__':
    test_c()
