import csv
import matplotlib.pyplot as plt

im = plt.imread('kinematic_simulation_copy/case_d_scene.png')
implot = plt.imshow(im)


filename = 'kinematic_simulation_copy/logs/data_d_x.csv'
scale = 13.5135135

t = []
x = []
y = []
state = []

with open(filename,'r') as csvfileQuick:
        plots = csv.reader(csvfileQuick, delimiter=',')
        for row in plots:
            t.append(int(row[0]))
            x.append(float(row[1]))
            y.append(float(row[2]))
            state.append(str(row[3]))



for i in t:
    if state[i] == 'N': colour = 'red'
    if state[i] == 'S': colour = 'purple'
    if state[i] == 'G1': colour = 'green'
    if state[i] == 'G2': colour = 'yellow'
    
    plt.scatter([x[i]*scale+432], [-y[i]*scale], c=colour, s=10)

# plt.xlabel('Time steps')
# plt.ylabel('Frames')
# plt.title('Frames until completion')
# plt.legend()

plt.show()
