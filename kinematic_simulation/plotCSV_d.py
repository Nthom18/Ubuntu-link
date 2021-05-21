'''
Plotting csv files.
This script only works for a flock of five drones!
'''


import csv
import matplotlib.pyplot as plt

t = []
dst0 = []
dst1 = []
dst2 = []
dst3 = []
dst4 = []

with open('logs/data.csv','r') as csvfileQuick:
    plots = csv.reader(csvfileQuick, delimiter=',')
    for row in plots:
        t.append(int(row[0]))
        dst0.append(float(row[1]))
        dst1.append(float(row[2]))
        dst2.append(float(row[3]))
        dst3.append(float(row[4]))
        dst4.append(float(row[5]))


# plt.subplot(1,2,1)
plt.plot(t, dst0, label = 'Drone_0')
plt.plot(t, dst1, label = 'Drone_1')
plt.plot(t, dst2, label = 'Drone_2')
plt.plot(t, dst3, label = 'Drone_3')
plt.plot(t, dst4, label = 'Drone_4')
plt.xlabel('Time steps')
plt.ylabel('Distance')
plt.title('Distance to target')
plt.legend()

# plt.subplot(1,2,2)
# plt.plot(t, collisions, 'r', label = 'Colliesions over time')
# plt.xlabel('Time steps')
# plt.ylabel('Cumulative collisions')
# plt.title('Example of plotted data')
# plt.legend()


plt.show()
