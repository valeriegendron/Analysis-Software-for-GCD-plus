import numpy as np
from get_time import get_time

run = 'TIDES2_h'
path = run + "/diskev/sortie_data"
path_cm = run + "/diskev/ascii_output/data_centered/cm_stars_data"
picName = 'orbit'

# Read data
t, x, y, z, vx, vy, vz = np.loadtxt(path, usecols=(0, 1, 2, 3, 4, 5, 6), unpack=True)

# The number of elements in 't' is much higher than the number of dumps.
# We need to only use the time in 't' corresponding to the dumps.
dt, noutput = get_time(run + "/diskev/ini/input.dat")  # time interval between dumps in Gyr, number of output files -1
time = []
for k in range(int(noutput)+1):
    time.append(round(dt*k, 4))

# Arrange 't' for comparison with 'time'
for i in range(len(t)):
    if t[i] < 1E-2:  # so of order 10^-3
        t[i] = round(t[i], 5)
    elif t[i] < 1E-1:  # so of order 10^-2
        t[i] = round(t[i], 4)
    elif t[i] < 1E+0:  # so of order 10^-1
        t[i] = round(t[i], 3)
    elif t[i] < 1E+1:  # so of order 10^0
        t[i] = round(t[i], 2)

print("Sorting data...")
xt, yt, zt, vxt, vyt, vzt = [], [], [], [], [], []  # will contain only data corresponding to dumps
for i in range(len(time)):
    for j in range(len(t)):
        if t[j] == time[i]:
            xt.append(x[j]), yt.append(y[j]), zt.append(z[j]), vxt.append(vx[j]), vyt.append(vy[j]), vzt.append(vz[j])
            break

# Recenter data of more massive galaxy using 'cm_stars_data' file
print("Recentering...")
x_cm, y_cm, z_cm, vx_cm, vy_cm, vz_cm = np.loadtxt(path_cm, usecols=(0, 1, 2, 3, 4, 5), unpack=True)
for i in range(len(xt)):
    xt[i] = xt[i] - x_cm[i]
    yt[i] = yt[i] - y_cm[i]
    zt[i] = zt[i] - z_cm[i]
    vxt[i] = vxt[i] - vx_cm[i]
    vyt[i] = vyt[i] - vy_cm[i]
    vzt[i] = vzt[i] - vz_cm[i]

# Write in new file
data = np.column_stack([time[:len(xt)], xt, yt, zt, vxt, vyt, vzt])
np.savetxt(run + "/diskev/sortie_data_centered", data, fmt='%13.5E' * 7)
