import math
import numpy as np
import matplotlib.pyplot as plt

#airfoil data
airfoil = np.stack(
    list(filter(
        lambda x : len(x) > 1, 
        [
            list(filter(len, x.split(" "))) for x in open("C:/Users/domin/OneDrive/Stalinis kompiuteris/windtunel/airfoil.dat", "r").read().split("\n")
        ]
    ))
).astype(float)

#sensor values
data = np.stack([
    x.split(", ") for x in open("C:/Users/domin/OneDrive/Stalinis kompiuteris/windtunel/data.txt", "r").read().split(",\n")
]).astype(float)

#sensor location
sensors = np.stack([
    x.split("\t") for x in open("C:/Users/domin/OneDrive/Stalinis kompiuteris/windtunel/sensors.txt", "r").read().split("\n")
]).astype(float)

areas = airfoil[1:] - airfoil[:-1]
normals = [[x[1] / (x[0]**2 + x[1]**2) ** 0.5, -x[0]/ (x[0]**2 + x[1]**2) ** 0.5] for x in areas]

#function for finding which sensor correpsonds to the correct datapoint
def interpolate(point, sensors):
    for x in range(1, len(sensors)):
        if (sensors[x, 1] < 0 and point[1] > 0) or (sensors[x, 1] > 0 and point[1] < 0):
            continue
        if sensors[x - 1, 0]* 0.01 <= point[0] and sensors[x, 0] * 0.01 >= point[0]:
            return x
    return -1
#aoa values
lt = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12.5, 
 13, 13.5, 14, 14.5, 14.2, 13.8, 13.6, 13.4, 13.2, 13, 12.8, 12.6, 12.4, 
 12.2, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 7.5, 6.5] #aoa
DRAG = []
LIFT = []

#drag curve generation
for y in range(0, len(lt)):
    force = np.stack([0.0,  0.0])
    for x in range(len(airfoil) - 1):
        index = interpolate(airfoil[x], sensors)
        if index == -1: continue
        force -= np.array(normals[x]) * data[y, index] * (areas[x, 0] ** 2 + areas[x, 1] ** 2) ** 0.5
    LIFT.append(force[1] / 247) #247 is q here
    DRAG.append(force[0] / 247)
plt.plot(lt, LIFT)
plt.show()
