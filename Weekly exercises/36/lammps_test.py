import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile
from ovito.io import import_file

plt.rc('text', usetex=True)                                                     # Setting LaTex fonts and style
plt.rc('font', family='serif', size=16)                                         # as well as the desired text size




'''
Reading Lammps dump file using the ovito enviroment:

If the ovito enviroment is not installed, install using
 - Mac OS / Linux : pip install ovito
 - Windows : ??

 For  further information, see: 'https://ovito.org/manual_testing/python/modules/ovito_io'
'''
'''
pipeline = import_file('dump.lammpstrj')
_t = []
_N_atoms = []
_Lx = []
_Ly = []
_x = []
_y = []
_vx = []
_vy = []


for frame in range(pipeline.source.num_frames):
   data = pipeline.compute(frame)
   _Lx.append(data.cell[0,0])
   _Ly.append(data.cell[1,1])
   _t.append(data.attributes['Timestep'])
   _N_atoms.append(data.particles.count)
   pos = data.particles.positions
   _x.append(pos[:,0])
   _y.append(pos[:,1])
   vel = data.particles.velocities
   _vx.append(vel[:,0])
   _vy.append(vel[:,1])

t = np.array(_t)
N_atoms = np.array(_N_atoms)
Lx = np.array(_Lx)
Ly = np.array(_Ly)
x = np.array(_x)
y = np.array(_y)
vx = np.array(_vx)
vy = np.array(_vy)

nleft = np.zeros(len(t))
for i in range(len(t)):
    nleft[i] = np.sum(np.where(x[i,:] < Lx[i]/2))

#print(f'Mean number of particles to the left in the box: {np.mean(nleft):.3f}  {np.std(nleft):.3f}')

fig1 = plt.figure()
ax1 = plt.axes()
ax1.plot(t, nleft)
ax1.set_xlabel('time $t$')
ax1.set_title('Number of particles on the left side of the box')
fig1.tight_layout()

rho = N_atoms/(Lx * Ly)
vxsq = np.mean(vx**2, axis=1)
vysq = np.mean(vy**2, axis=1)
K  = (vxsq + vysq)/2

fig2 = plt.figure()
ax2 = plt.axes()
ax2.plot(t, vxsq, label=r'$\overline{v_x^2}$')
ax2.plot(t, vysq, label=r'$\overline{v_y^2}$')
ax2.plot(t, K, label=r'$\overline{K/m}$')
ax2.set_xlabel('time $t$')
ax2.set_title('Mean square of velocity components and kinetic energy')
fig2.legend()
fig2.tight_layout()

Pkin = rho * K

fig3 = plt.figure()
ax3 = plt.axes()
ax3.plot(t, Pkin)
ax3.set_xlabel('time $t$')
ax3.set_title('Kinetic pressure')
fig3.tight_layout()
'''




'''
Reading a log.lammps file using lammps_logfile and extracting vital information

If the lammps_logfile enviroment is not installed, install using
 - Mac OS / Linux : pip install lammps-logfile
 - Windows : ??

 For further information, see: 'https://github.com/henriasv/lammps-logfile'
'''

log = lammps_logfile.File('log.lammps')
t = log.get('Time')
T = log.get('Temp')
Ek = log.get('KinEng')
Ep = log.get('PotEng')
P = log.get('Press')

fig4 = plt.figure()
ax4 = plt.axes()
ax4.plot(t, Ek + Ep)
ax4.set_xlabel('time $t$')
ax4.set_title('Total energy')
fig4.tight_layout()

fig5 = plt.figure()
ax5 = plt.axes()
ax5.plot(t, T)
ax5.set_xlabel('time $t$')
ax5.set_title('Temperature')
fig5.tight_layout()
plt.show()
