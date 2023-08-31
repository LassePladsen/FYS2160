"""
Created on 31.08.2023
"""

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("termokopper_data.txt")
time = data[:, 0] / 60
temp1 = data[:, 1]
temp2 = data[:, 2]

plt.plot(time, temp1, time, temp2)
plt.legend(["Bodum thermos", "Temperfect thermos"])
plt.xlabel("Time [min]")
plt.ylabel("Water temperature $T_w$ [°C]")
plt.grid()
plt.savefig("figures/termokopper_plot.png")
