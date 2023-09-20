import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
traj = read("dump.lammpstrj", format="lammps-dump-text", index=":")
n = len(traj) # Number of timesteps
nleft = np.zeros(n)
vxmean = np.zeros(n)
# Find size of simulation box
firstframe = traj[0]
cellshape = firstframe.get_cell()
halfsize = cellshape[0][0]*0.5
# Count number of particles on left side for each timestep
it = 0
for frame in traj:
    x = frame.get_positions() # positions of atoms
    xi = x[:,0] # x-coordinates of atoms
    nleft[it] = np.sum(xi<halfsize)
    v = frame.get_velocities() # velocities of atoms
    vx = v[:,0] # x-component of velocities
    vxmean[it] = np.mean(vx)
    it = it + 1
fig, axs = plt.subplots(2)
fig.suptitle('functions of position and velocity')
axs[0].plot(nleft)
axs[0].set_xlabel("Time")
axs[0].set_ylabel("x")

axs[1].plot(vxmean)
axs[1].set_xlabel("Time")
axs[1].set_ylabel("v_x")

plt.tight_layout()
plt.show()
