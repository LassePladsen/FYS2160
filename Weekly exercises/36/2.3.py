"""
Created on 07.09.2023
"""

import numpy as np
import matplotlib.pyplot as plt

def mult(N_opp, N):
    return np.math.factorial(N)/(np.math.factorial(N_opp) * np.math.factorial(N-N_opp))

print(mult(25,50))