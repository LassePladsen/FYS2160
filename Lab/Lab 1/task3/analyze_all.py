"""
Created on 25.09.2023
"""

import lammps_logfile as lmplog
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.stats import linregress

path = Path(".")

# List of outfiles
outfiles = list(path.rglob("log.task3_rho*"))
# Put second item (rho10) to the back for correct loop indexing
outfiles.append(outfiles.pop(1))

# List of density values
rho_vals = np.genfromtxt("task3_infiles/rho_vals.txt")

Z_vals = np.zeros(len(rho_vals))
Cv_vals = np.zeros_like(Z_vals)

# Analyze each one, then plot Cv(T) and Z(rho)
# First plot Cv(t)
figsize = (6, 5)
plt.figure(figsize=figsize)
i = 0
for file, rho in zip(outfiles, rho_vals):
    log = lmplog.File(file)

    # Extract values
    T = log.get("Temp")[1:]
    U = log.get("TotEng")[1:]
    P = log.get("Press")[1:]

    # Regression
    reg = linregress(T, U)
    y = reg.slope * T + reg.intercept

    # Plot U regression
    rho_index = file.name.split("_")[-1]
    plt.plot(T, y, label=f"{rho_index}={rho}", ms=2)

    # Save mean Z values
    Z_vals[i] = np.mean(P / (rho * T))

    # Save C_v (slope) values
    Cv_vals[i] = reg.slope

    i += 1

plt.legend(frameon=False)
plt.xlabel("T*")
plt.ylabel("U*")
plt.title("Linear regressions")
plt.savefig("U(T).png")

# Secondly, plot Z(rho)
plt.figure(figsize=figsize)
plt.plot(rho_vals, Z_vals, "o-")
plt.xlabel(r"$\rho^*$")
plt.ylabel("Z")
plt.savefig("Z(rho).png")

# Lastly plot C_V(rho)
plt.figure(figsize=figsize)
plt.plot(rho_vals, Cv_vals, "o-")
plt.xlabel(r"$\rho^*$")
plt.ylabel("$C_V$ [J/K]")
plt.savefig("C_V(rho).png")
