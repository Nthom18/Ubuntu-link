'''
Plotting csv files for case d).

Author: Nicoline Louise Thomsen
'''

import csv
import matplotlib.pyplot as plt

t = []
dst0 = []
dst1 = []
dst2 = []
dst3 = []
dst4 = []

def plotCSV_d(filename):
    
    with open('logs/' + filename + '.csv','r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            t.append(int(row[0]))
            dst0.append(float(row[1]))
            dst1.append(float(row[2]))
            dst2.append(float(row[3]))
            dst3.append(float(row[4]))
            dst4.append(float(row[5]))

    plt.plot(t, dst0, label = 'Drone_0')
    plt.plot(t, dst1, label = 'Drone_1')
    plt.plot(t, dst2, label = 'Drone_2')
    plt.plot(t, dst3, label = 'Drone_3')
    plt.plot(t, dst4, label = 'Drone_4')
    plt.xlabel('Time steps')
    plt.ylabel('Distance')
    plt.title('Distance to target')
    plt.legend()
    
    plt.show()
    


if __name__ == '__main__':
    plotCSV_d('data_d_combined')
    # 9 15 23