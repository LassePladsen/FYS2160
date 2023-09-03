import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
Ctb = 1.96  # Heat capacity ratio top to bottom
C_loss = 1/25  # Heat loss coefficient
N = 100_000  # Number of heat packets
nstep = 15 * N  # Number of steps in simulation

# Data plotting parameters
tau = 150  # Guessing the characteristic time

### SIMULATION
# Initialize temperature-time arrays
Tt = np.zeros(nstep, float)
Tb = np.zeros(nstep, float)
Tt[0] = 1  # Initial temperature top
Tb[0] = -1  # Initial temperature bottom
Tr = -1  # Room temperature

for i in range(1, nstep):
    r = 4 * np.random.rand(1, 1) - 2  # Random number between 2 and -2
    DT = Tt[i - 1] - Tb[i - 1]  # Temperature difference top to bottom
    if r < DT:
        # Move heat quanta from top to bottom
        Tt[i] = Tt[i - 1] - 1 / N
        Tb[i] = Tb[i - 1] + Ctb / N
    else:
        # Move heat quanta from bottom to top
        Tt[i] = Tt[i - 1] + 1 / N
        Tb[i] = Tb[i - 1] - Ctb / N

    # Randomized heat loss to air in the same fashion as the above diffusion
    rt = 4 * np.random.rand(1, 1) - 2  # Random number between 2 and -2
    rb = 4 * np.random.rand(1, 1) - 2
    DTt = Tt[i] - Tr  # Temperature difference top to room
    DTb = Tb[i] - Tr  # Temperature difference bot to room
    if rt < DTt:
        # Subtract one heat quanta multiplied by heat loss coefficient
        Tt[i] -= C_loss / N
    if rb < DTb:
        Tb[i] -= C_loss / N

### EXPERIMENTAL DATA
D = np.loadtxt('metalblocks_lecture.txt', usecols=[0, 1, 2], unpack=True)
t = D[0, :] / tau  # Dimensionless time
T1 = D[1, :]
T2 = D[2, :]
T10 = np.mean(T1[70:91])
T20 = np.mean(T2[70:91])
DT0 = T20 - T10
Tmean0 = (T20 + T10) / 2


# Plotting config
xmin = 0
xmax = 12.1
x_ticks_maj = np.arange(xmin, xmax, 1)
x_ticks_min = np.arange(xmin, xmax, 0.5)
ymin = -1
ymax = 1.01
y_ticks_maj = np.arange(ymin, ymax, 0.5)
y_ticks_min = np.arange(ymin, ymax, 0.25)

# Plot data, rescaled temperature versus rescaled time
fig = plt.figure(figsize=(5, 5))
fig.suptitle(rf"Ctb = {Ctb}, $\tau$ = {tau}")
plt.subplot(2, 1, 1)
plt.title("Experimental data")
plt.plot(t, 2 * (T1 - Tmean0) / DT0, color='k')
plt.plot(t, 2 * (T2 - Tmean0) / DT0, color='r')
plt.axis([xmin, xmax, ymin, ymax])
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$2(T-<T_0>)/\Delta T_0$')
plt.legend(['Temperature top', 'Temperature bottom'])
plt.xticks(x_ticks_maj)
plt.xticks(x_ticks_min, minor=True)
plt.yticks(y_ticks_maj)
plt.yticks(y_ticks_min, minor=True)
plt.grid(which="both")

# Plot simulation
plt.subplot(2, 1, 2)
plt.title("Simulation")
plt.plot(np.arange(0, nstep) / N, Tt, color='r')
plt.plot(np.arange(0, nstep) / N, Tb, color='k')
plt.xlabel('steps/N')
plt.ylabel(r'$2(T-<T_0>)/\Delta T_0$')
plt.axis([xmin, xmax, ymin, ymax])
plt.legend(['Temperature top', 'Temperature bottom'])
plt.xticks(x_ticks_maj)
plt.xticks(x_ticks_min, minor=True)
plt.yticks(y_ticks_maj)
plt.yticks(y_ticks_min, minor=True)
plt.grid(which="both")

plt.tight_layout()
plt.savefig("figures/diffusion_simulation_with_loss.png")
