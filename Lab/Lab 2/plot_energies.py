"""
Created on 16.10.2023
"""

import numpy as np
import matplotlib.pyplot as plt

# Input file
file = "300K_simulation_log.txt"

# Plot energies E_tot and H
data = np.genfromtxt(file, skip_header=True)
toteng = data[:, 2]
enthalpy = data[:, 3]
step = np.arange(0, len(toteng)*100, 100)
T = int(file.split("_")[0].rstrip("K"))

fig, axs = plt.subplots(1, 2)
fig.suptitle(f"Simulation energy plots at {T=}K")

axs[0].plot(step, toteng)
axs[0].set_xlabel("Step")
axs[0].set_ylabel("Energy $E$")
axs[0].set_title("Energy")

axs[1].plot(step, enthalpy)
axs[1].set_xlabel("Step")
axs[1].set_ylabel("Enthalpy $H$")
axs[1].set_title("Enthalpy")

plt.tight_layout()
plt.savefig(f"energy_plots_{T}K.png")
