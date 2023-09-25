# coding=utf-8

"""
Created on 25.09.2023
"""

import lammps_logfile as lmplog
from scipy.stats import linregress

# Constants
rho = 0.001

with open("analyze.txt", "w") as outfile:
    for file in ["log.rod", "log.spring"]:
        log = lmplog.File(file)

        # Extract values
        T = log.get("Temp")[1:]
        U = log.get("TotEng")[1:]

        # Regression
        reg = linregress(T, U)
        y = reg.slope * T + reg.intercept

        # Calculate values
        Cv = reg.slope
        dCv = reg.stderr
        f = Cv * 2
        df = f * dCv / Cv

        outfile.write(f"{file}:\n")
        outfile.write(f"C_v = ({Cv:.4f} ± {dCv:.4f})\n")
        outfile.write(f"f = ({f:.4f} ± {df:.4f})\n\n")


