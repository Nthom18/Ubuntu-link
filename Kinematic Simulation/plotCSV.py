import csv
import matplotlib.pyplot as plt
import numpy as np

x = []
y = []

# QUICKSELECT_____________________________________

t = np.arange(0, 2500, 1)

with open('logs/data.csv','r') as csvfileQuick:
    plots = csv.reader(csvfileQuick, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(float(row[1]))

plt.plot(x, y, label = 'Distance to target')


plt.xlabel('Time steps')
plt.ylabel('Distance')
plt.title('Example of plotted data')
plt.legend()
plt.show()
