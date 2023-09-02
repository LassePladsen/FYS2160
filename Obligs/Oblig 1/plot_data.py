"""
Created on 31.08.2023
"""

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("termokopper_data.txt")
time = data[:, 0] / 60
temp1 = data[:, 1]
temp2 = data[:, 2]

plt.figure(figsize=(5, 4))
plt.plot(time, temp1, time, temp2)
plt.legend(["Bodum thermos", "Temperfect thermos"])
plt.xlabel("Time [min]")
plt.ylabel("Water temperature $T_w$ [°C]")

# Grid ticks
xmin = 0
xmax = 116
plt.xticks(range(xmin, xmax, 10))
plt.xticks(range(xmin, xmax, 5), minor=True)
ymin = 20
ymax = 91
plt.yticks(range(ymin, ymax, 10))
plt.yticks(range(ymin, ymax, 5), minor=True)
plt.grid(which="both")

plt.savefig("figures/termokopper_plot.png")
