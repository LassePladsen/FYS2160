from lammps_logfile import File

log = File("log.lammps")
print(log.get_keywords())

t = log.get("Time")
temp = log.get("Temp")
press = log.get("Press")

import matplotlib.pyplot as plt 

plt.plot(t, temp*press)
plt.xlabel("Time (ps)")
plt.ylabel("Temperature (K)")
# plt.ylim([215, 225])
plt.savefig("time_temp_press.png")

from lammps_logfile import running_mean

# temp_avg = running_mean(temp, 100)
#
# plt.plot(t, temp_avg)
# plt.xlabel("Time (ps)")
# plt.ylabel("Temperature (K)")
# # plt.ylim([215, 225])
# plt.savefig("time_temp_press_avg.png")

