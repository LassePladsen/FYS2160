import matplotlib.pyplot as plt
import numpy as np

# SIMULATION PARAMETERS
Ctb = 5  # Heat capacity ratio top to bottom
C_loss = 1/18  # Heat loss coefficient
N = 100_000  # Number of heat packets
nstep = 50 * N  # Number of steps in simulation
T_bm = 0.4  # melting temperature for bottom part
L_b = 0.6 * N   # latent heat for bottom, simulating phase-change

# PLOT TEMPERFECT EXPERIMENT
data = np.genfromtxt("termokopper_data.txt")
time = data[:, 0] / 60
temp1 = data[:, 1]
temp2 = data[:, 2]

fig = plt.figure(figsize=(5, 5))
plt.subplot(2, 1, 1)
plt.plot(time, temp2, label="Temperfect thermos", color="k")
plt.legend()
plt.title("Experiment")
plt.xlabel("Time [min]")
plt.ylabel("Water temperature $T_w$ [°C]")

# Data grid ticks
xmin = 0
xmax = 116
plt.xticks(np.arange(xmin, xmax, 10))
plt.xticks(np.arange(xmin, xmax, 5), minor=True)
ymin = 20
ymax = 91
plt.yticks(np.arange(ymin, ymax, 10))
plt.yticks(np.arange(ymin, ymax, 5), minor=True)
plt.grid(which="both")


# DIFFUSION SIMULATION
# Initialize temperature-time arrays
Tt = np.zeros(nstep, float)
Tb = np.zeros(nstep, float)
Tt[0] = 1  # Initial temperature top
Tb[0] = -1  # Initial temperature bottom
Tr = -1  # Room temperature

L_i = 0  # variable to keep track of bottom's latent heat
melting = False  # variables to keep track of phase-changes of the bottom
liquid = False
crystallizing = False
solid = True

def heat_to_bottom(i):
    """Move heat quanta from top to bottom in the below loop"""
    Tt[i] = Tt[i - 1] - 1 / N
    Tb[i] = Tb[i - 1] + Ctb / N

def heat_to_top(i):
    """Move heat quanta from bottom to top for the below loop"""
    Tt[i] = Tt[i - 1] + 1 / N
    Tb[i] = Tb[i - 1] - Ctb / N

def heat_loss_top(i):
    """Randomized heat loss to air in the same fashion as the above diffusion, for the top block."""
    rt = np.random.uniform(0, 2)  # Random number between 0 and 2
    DTt = Tt[i] - Tr  # Temperature difference top to room
    if rt < DTt:
        # Subtract one heat quanta multiplied by heat loss coefficient
        Tt[i] -= C_loss / N

def heat_loss_bot(i):
    """Randomized heat loss to air in the same fashion as the above diffusion, for the bottom block."""
    rb = np.random.uniform(0, 2)  # Random number between 0 and 2
    DTb = Tb[i] - Tr  # Temperature difference bot to room
    if rb < DTb:
        # Subtract one heat quanta multiplied by heat loss coefficient
        Tb[i] -= C_loss / N


for i in range(1, nstep):
    r = 4 * np.random.rand(1, 1) - 2  # Random number between 2 and -2
    DT = Tt[i - 1] - Tb[i - 1]  # Temperature difference top to bottom
    if melting:
        crystallizing = False
        solid = False
        if L_i < L_b:  # continue melting
            L_i += 1
            Tt[i] = Tt[i - 1] - 1 / N  # suck heat quanta from top to melt the bottom
            Tb[i] = Tb[i-1]  # dont change bottom temp during phase-change

        else:  # stop melting
            melting = False
            liquid = True
            L_i = 0
            if r < DT:
                # Move heat quanta from top to bottom
                heat_to_bottom(i)
            else:

                # Move heat quanta from bottom to top
                heat_to_top(i)

    elif crystallizing:
        melting = False
        liquid = False
        if L_i < L_b:  # continue crystallizing
            L_i += 1
            Tt[i] = Tt[i - 1] + 1 / N  # release heat from bottom to top during crystallization
            Tb[i] = Tb[i-1]  # dont change bottom temp during phase-change

        else:  # stop crystallizing
            crystallizing = False
            solid = True
            L_i = 0
            if r < DT:
                # Move heat quanta from top to bottom
                heat_to_bottom(i)
            else:

                # Move heat quanta from bottom to top
                heat_to_top(i)

    else:  # no phase-change
        if r < DT:
            # Move heat quanta from top to bottom
            heat_to_bottom(i)
            if Tb[i] >= T_bm > Tb[i - 1] and solid:  # start melting
                melting = True

        else:
            # Move heat quanta from bottom to top
            heat_to_top(i)
            if Tb[i] < T_bm <= Tb[i - 1] and liquid:  # start crystallization
                crystallizing = True

    heat_loss_top(i)
    heat_loss_bot(i)


# Simulation grid ticks
xmin = 0
xmax = nstep/N + 0.1
x_ticks_maj = np.arange(xmin, xmax, 5)
x_ticks_min = np.arange(xmin, xmax, 2.5)
ymin = -1
ymax = 1.01
y_ticks_maj = np.arange(ymin, ymax, 0.5)
y_ticks_min = np.arange(ymin, ymax, 0.25)

# Plot simulation
plt.subplot(2, 1, 2)
plt.title("Simulation")
plt.plot(np.arange(0, nstep) / N, Tb, color="r", label="Temperature bot")
plt.plot(np.arange(0, nstep) / N, Tt, color="k", label="Temperature top")
plt.xlabel('steps/N')
plt.ylabel(r'$2(T-<T_0>)/\Delta T_0$')
plt.axis([xmin-2, xmax, ymin, ymax])
plt.legend()
plt.xticks(x_ticks_maj)
plt.xticks(x_ticks_min, minor=True)
plt.yticks(y_ticks_maj)
plt.yticks(y_ticks_min, minor=True)
plt.grid(which="both")

plt.tight_layout()
plt.savefig("figures/temperfect_simulation.png")
# plt.show()
