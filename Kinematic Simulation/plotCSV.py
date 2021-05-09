import csv
import matplotlib.pyplot as plt
import numpy as np

t = []
dst = []
collisions = []

with open('logs/data.csv','r') as csvfileQuick:
    plots = csv.reader(csvfileQuick, delimiter=',')
    for row in plots:
        t.append(int(row[0]))
        dst.append(float(row[1]))
        collisions.append(int(row[2]))

        # t.append(int(row[0]))
        # dst.append(row[1:])

        # # for i in range(len(row[1])):
        # #     if i != 0 and i != len(row[1]) - 1:
        # #         dst.append(float(row[1][i]))


plt.subplot(1,2,1)
plt.plot(t, dst, label = 'Distance to target')
plt.xlabel('Time steps')
plt.ylabel('Distance')
plt.title('Example of plotted data')
plt.legend()

plt.subplot(1,2,2)
plt.plot(t, collisions, 'r', label = 'Colliesions over time')
plt.xlabel('Time steps')
plt.ylabel('Cumulative collisions')
plt.title('Example of plotted data')
plt.legend()

# np_dst_T = np.matrix(dst)

# print(len(dst), len(dst[0]))
# print(np_dst_T)
# print()
# print(np.transpose(dst))

# for column in np.transpose(dst):
    # plt.plot(t, column)
    # print(column)

# plt.xlabel('Time steps')
# plt.ylabel('Distance')
# plt.title('Example of plotted data')
# plt.legend()

plt.show()
