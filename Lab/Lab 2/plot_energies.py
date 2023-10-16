"""
Created on 16.10.2023
"""

import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile

# Input file
file = "simulation/log400K.lammps"

# Plot energies E_tot and H
log = lammps_logfile.File(file)
enthalpy = log.get("Enthalpy")
toteng = log.get("TotEng")
step = np.arange(0, len(toteng)*100, 100)
T = int(file.split(".")[0][-4:-1])

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
