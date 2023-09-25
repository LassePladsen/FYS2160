"""
Created on 25.09.2023
"""

from sys import argv

import lammps_logfile as lmplog
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

if __name__ == "__main__":
    # Constants
    rho = 0.001
    k = 1.380649e-23  # m^2 kg s^-2 K^-1

    log = lmplog.File(argv[1])

    # Extract values
    T = log.get("Temp")[1:]
    U = log.get("TotEng")[1:]
    P = log.get("Press")[1:]

    # Regression
    reg = linregress(T, U)
    y = reg.slope * T + reg.intercept

    # Plot
    figsize = (6, 4)
    plt.figure(figsize=figsize)
    plt.plot(T, U, "o", label="Data")
    plt.plot(T, y, label="Regression")
    plt.legend()
    plt.xlabel("T*")
    plt.ylabel("U*")
    plt.savefig("U(T).png")

    def mean_std(array):
        return np.mean(array), np.std(array)


    # Calculate values
    Cv = reg.slope
    dCv = reg.stderr

    f = Cv * 2
    df = f * dCv / Cv

    Z_arr = P / (rho * T)
    Z, dZ = mean_std(Z_arr)

    # Plot Z:
    reg_Z = linregress(T, Z_arr)
    y_Z = reg_Z.slope * T + reg_Z.intercept
    plt.figure(figsize=figsize)
    plt.plot(T, Z_arr, "o", label="Data", ms=2)
    plt.plot(T, y_Z, label="Regression", ms=2)
    plt.legend()
    plt.xlabel("T*")
    plt.ylabel(r"$Z=P^*/(\rho^* T^*)$")
    plt.savefig("Z(T).png")

    # Save prints to output file
    with open("analyze.txt", "w") as file:
        file.write(f"C_v = ({Cv:.4e} ± {dCv:.4e})\n")
        file.write(f"f = ({f} ± {df})\n")
        file.write(f"Z_mean = ({Z:.4e} ± {dZ:.4e})\n")
