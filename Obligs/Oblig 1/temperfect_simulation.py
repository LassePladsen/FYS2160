import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
Ctb = 1/8  # Heat capacity ratio top to bottom
C_loss = 1/25  # Heat loss coefficient
N = 5_000  # Number of heat packets
nstep = 15 * N  # Number of steps in simulation
T_bm = 0.5  # melting temperature for bottom part
L_b = nstep / 10   # latent heat for bottom (amount of steps to simulate phase-change)

# PLOT TEMPERFECT EXPERIMENT
data = np.genfromtxt("termokopper_data.txt")
time = data[:, 0] / 60
temp1 = data[:, 1]
temp2 = data[:, 2]

fig = plt.figure(figsize=(5, 5))
plt.subplot(2, 1, 1)
plt.plot(time, temp1, time, temp2)
plt.legend(["Bodum thermos", "Temperfect thermos"])
plt.title("Experiment")
plt.xlabel("Time [min]")
plt.ylabel("Water temperature $T_w$ [°C]")

# Grid ticks
xmin = 0
xmax = 116
plt.xticks(range(xmin, xmax, 10))
plt.xticks(range(xmin, xmax, 5), minor=True)
ymin = 20
ymax = 91
plt.yticks(range(ymin, ymax, 10))
plt.yticks(range(ymin, ymax, 5), minor=True)
plt.grid(which="both")


# DIFFUSION SIMULATION
# Initialize temperature-time arrays
Tt = np.zeros(nstep, float)
Tb = np.zeros(nstep, float)
Tt[0] = 1  # Initial temperature top
Tb[0] = -1  # Initial temperature bottom
Tr = -1  # Room temperature

L_i = L_b  # current latent heat
for i in range(1, nstep):
    r = 4 * np.random.rand(1, 1) - 2  # Random number between 2 and -2
    DT = Tt[i - 1] - Tb[i - 1]  # Temperature difference top to bottom
    if r < DT:
        # Move heat quanta from top to bottom
        Tt[i] = Tt[i - 1] - 1 / N
        Tb[i] = Tb[i - 1] + Ctb / N

        if Tb[i - 1] < T_bm < Tb[i]:  # start bottom melting
            L_i = 0

        if (Tb[i - 1] > T_bm and Tb[i] > T_bm) and L_i < L_b:  # if bottom melting
            L_i += N
            Tt[i] -= Tb[i] - Tb[i - 1]  # suck heat from top to melt bottom
            Tb[i] = Tb[i - 1]  # dont raise temp during melting
    else:
        # Move heat quanta from bottom to top
        Tt[i] = Tt[i - 1] + 1 / N
        Tb[i] = Tb[i - 1] - Ctb / N

        if Tb[i - 1] > T_bm > Tb[i]:  # start bottom crystallization
            L_i = 0

        if (Tb[i - 1] < T_bm and Tb[i] < T_bm) and L_i < L_b:  # if bottom crystallizing
            L_i += N
            Tt[i] += Tb[i] - Tb[i - 1]  # suck heat from top to melt bottom
            Tb[i] = Tb[i - 1]

    # Randomized heat loss to air in the same fashion as the above diffusion:
    # heat loss top
    rt = 4 * np.random.rand(1, 1) - 2  # Random number between 2 and -2
    DTt = Tt[i] - Tr  # Temperature difference top to room
    if rt < DTt:
        # Subtract one heat quanta multiplied by heat loss coefficient
        Tt[i] -= C_loss / N

    # heat loss bottom
    rb = 4 * np.random.rand(1, 1) - 2
    DTb = Tb[i] - Tr  # Temperature difference bot to room
    if rb < DTb:
        Tb[i] -= C_loss / N

# Grid ticks
xmin = 0
xmax = nstep/N + 0.1
x_ticks_maj = np.arange(xmin, xmax, 2.5)
x_ticks_min = np.arange(xmin, xmax, 2.5/2)
ymin = -1
ymax = 1.01
y_ticks_maj = np.arange(ymin, ymax, 0.5)
y_ticks_min = np.arange(ymin, ymax, 0.25)

# Plot simulation
plt.subplot(2, 1, 2)
plt.title("Simulation")
plt.plot(np.arange(0, nstep) / N, Tt)
plt.plot(np.arange(0, nstep) / N, Tb)
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
plt.savefig("figures/temperfect_simulation.png")
