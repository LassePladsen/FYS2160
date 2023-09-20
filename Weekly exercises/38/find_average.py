import numpy as np

data = np.genfromtxt("data.txt", skip_header=True)
T = 1.4
rho = 0.01

def Z(T, rho, P_mean):
    return P_mean/(rho*T)


P_mean = np.mean(data[:, -1])
print(f"{P_mean=:.3e}")
print(f"{Z(T, rho, P_mean)=:g}")