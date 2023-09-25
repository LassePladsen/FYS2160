"""
Created on 25.09.2023
"""

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

path = Path(".")

# List of outfiles
outfiles = path.rglob("log.task3_rho*")

# List of rho_vals
rho_vals = np.genfromtxt("task3_infiles/rho_vals.txt")

# Analyze each one, plot Cv(T) and Z(T)
Z_vals = np.empty(len(rho_vals))
plt.figure(figsize=(6, 5))  # First plot Cv(t)
for file in outfiles:
