import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
from get_time import get_time

picName = "sfr_profile_global.png"
dt, noutput = get_time("ini/input.dat")  # time interval between dumps in Gyr, number of output files -1

total_smass = []  # will contain the total star mass for each time step
for fileName in sorted(os.listdir("ascii_output")):  # to run through all dumps
    if len(fileName) == 4:  # output file
        if fileName.startswith("s"):  # star file
            if fileName.endswith("000"):  # dump 000, skipping
                total_smass.append(0)  # no star formation at t=0
            else:
                print("Reading file " + fileName)
                smass_list, age_list = np.loadtxt("ascii_output/" + fileName, usecols=(6, 18), unpack=True)
                new_stars = []  # will contain masses of new star particles
                for particle in range(len(age_list)):
                    if age_list[particle] < dt*(10**9):
                        new_stars.append(smass_list[particle])
                total_smass.append(sum(new_stars))

# Computing sfr
sfr = []  # will contain sfr in M_sun/yr at each time step
for i in range(len(total_smass)):
    sfr.append(total_smass[i]/(dt*10**9))  # in M_sun/yr units

# Plotting
time = []
for k in range(int(noutput)+1):
    time.append(round(dt*k, 2))
#del time[0]  # remove time 0 from list

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time, sfr, color='blue')
ax.set_xlabel("Time [Gyr]")
ax.set_ylabel("SFR [M$_\odot$/yr]")
fig.tight_layout()

print('Saving')
plt.savefig(picName, dpi=500)

# Writing in separate file
data = np.column_stack([time, sfr])
np.savetxt('sfr_global_data', data)
