'''
Plotting csv files for case c), specefically the test for flock size.

Author: Nicoline Louise Thomsen
'''

import csv
import matplotlib.pyplot as plt

t = []
frame1 = []
frame2 = []
frame3 = []
frame4 = []

def plotCSV_c_sizetest(filename):
    
    with open('logs/' + filename + '_1.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            t.append(int(row[0]))
            frame1.append(float(row[1]))

    with open('logs/' + filename + '_3.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            frame2.append(float(row[1]))
    
    with open('logs/' + filename + '_5.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            frame3.append(float(row[1]))

    with open('logs/' + filename + '_7.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            frame4.append(float(row[1]))

    # Output averages
    print('Avg_1: ', sum(frame1)/len(t))
    print('Avg_3: ', sum(frame2)/len(t))
    print('Avg_5: ', sum(frame3)/len(t))
    print('Avg_7: ', sum(frame4)/len(t))

    # Plot

    plt.plot(t, frame1, label = 'flock size = 1')
    plt.plot(t, frame2, label = 'flock size = 3')
    plt.plot(t, frame3, label = 'flock size = 5')
    plt.plot(t, frame4, label = 'flock size = 7')


    # plt.plot(t, collisions, label = 'Collisions')
    plt.xlabel('Time steps')
    plt.ylabel('Frames')
    plt.title('Frames until completion for different flock sizes')
    plt.legend()
    
    plt.show()


if __name__ == '__main__':
    plotCSV_c_sizetest('data_c')