import matplotlib.pyplot as plt
import numpy as np

# Parameters
Ctb = 1  # Heat capacity ratio top to bottom
N = 8000  # Number of heat packets
nstep = 15 * N  # Number of steps in simulation
tau = N  # Time scale (characteristic time)

# Initialize temperature-time arrays
Tt = np.zeros(nstep, float)
Tb = np.zeros(nstep, float)
Tt[0] = 1  # Initial temperature top
Tb[0] = -1  # Initial temperature bottom
Tr = -1  # Room temperature

for i in range(1, nstep):
    # Random number between 2 and -2
    r = 4 * np.random.rand(1, 1) - 2
    # Temperature difference top to bottom
    DT = Tt[i - 1] - Tb[i - 1]
    if r < DT:
        # Move heat quanta from top to bottom
        Tt[i] = Tt[i - 1] - 1 / N
        Tb[i] = Tb[i - 1] + Ctb / N
    else:
        # Move heat quanta from bottom to top
        Tt[i] = Tt[i - 1] + 1 / N
        Tb[i] = Tb[i - 1] - Ctb / N

# Plot
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(np.arange(0, nstep)/N, Tt, color='r')
plt.plot(np.arange(0, nstep)/N, Tb, color='k')
plt.xlabel('steps/N')
plt.ylabel(r'$2(T-<T_0>)/\Delta T_0$')
plt.legend(['Temperature top', 'Temperature bottom'])


D = np.loadtxt('metalblocks_lecture.txt', usecols = [0, 1, 2], unpack = True)
# Guessing the characteristic time
tau = 100
# Dimensionless time
t = D[0,:] / tau
T1 = D[1,:]
T2 = D[2,:]
T10 = np.mean(T1[70:91])
T20 = np.mean(T2[70:91])
DT0 = T20 - T10
Tmean0 = (T20 + T10) / 2

# Plot rescaled temperature versus rescaled time
plt.subplot(2, 1, 2)
plt.plot(t, 2 * (T1 - Tmean0) / DT0, color = 'k')
plt.plot(t, 2 * (T2 - Tmean0) / DT0, color = 'r')
plt.axis([0, 15, -1.0, 1.01])
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$2(T-<T_0>)/\Delta T_0$')
plt.legend(['Temperature top','Temperature bottom'])
plt.savefig("figures/diffusion_simulation.png")
