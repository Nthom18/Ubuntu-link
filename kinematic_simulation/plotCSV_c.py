'''
Plotting csv files for case c).

Author: Nicoline Louise Thomsen
'''

import csv
import matplotlib.pyplot as plt

t = []
frame = []
collisions = []

def plotCSV_c(filename):
    
    with open('logs/' + filename + '.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            t.append(int(row[0]))
            frame.append(float(row[1]))
            collisions.append(float(row[2]))


    plt.plot(t, frame, label = 'Frames to complete')

    for i, c in enumerate(collisions):
        if c > 0:
            plt.scatter(i, c, color = 'red', label = 'Collisions')

    print('Avg_5: ', sum(frame)/len(t))

    # plt.plot(t, collisions, label = 'Collisions')
    plt.xlabel('Test number')
    plt.ylabel('Frames')
    plt.title('Frames until completion')
    plt.legend()
    
    plt.show()


if __name__ == '__main__':
    plotCSV_c('data_c')