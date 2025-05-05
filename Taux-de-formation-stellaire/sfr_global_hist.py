# This code assumes a simulation of 5 Gyr and a dt = 0.01 Gyr.
# If for example we had a simulation of 3 Gyr, we would need to write "if 300 % n_dt !=0", instead of 500
# If for example dt = 0.02 Gyr and we wanted bins of 3 times that size (0.06 Gyr), we would need to set n_dt = 6

import numpy as np
import matplotlib.pyplot as plt
import sys


# Settings
n_dt = 3  # number of dt we want the bins width to be
file_name = "sfr_global_ID_data"
picName = "sfr_global_ID-" + str(n_dt) + "_dt_hist.png"

# Figure setting
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Time [Gyr]")
ax.set_ylabel("SFR [M$_\odot$/yr]")


time, sfr = np.loadtxt(file_name, usecols=(0, 1), unpack=True)

i = 0
if 500 % n_dt != 0:
    print("Choose another n_dt so that all bins may be equal.")
    sys.exit()
elif n_dt != 1:
    sfr_n, time_n = [], []
    time_n.append(time[0])
    while i < (len(sfr)-1):
        sfr_i = sum(sfr[i:(i+n_dt)])/n_dt
        time_i = time[i+n_dt]
        sfr_n.append(sfr_i), time_n.append(time_i)
        i += n_dt

plt.stairs(sfr_n, time_n, fill=False, color='red')
fig.tight_layout()

# Save file
plt.savefig(picName, dpi=500)
