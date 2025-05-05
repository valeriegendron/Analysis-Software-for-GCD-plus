import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

run = 'TIDES2_h'
path = run + "/diskev/sortie_data_centered"
picName = 'orbit_distance_' + run

# Read data
t, x, y, z, vx, vy, vz = np.loadtxt(path, usecols=(0, 1, 2, 3, 4, 5, 6), unpack=True)

# Compute radius
r, v = [], []
for i in range(len(t)):
    r.append(np.sqrt(x[i]**2+y[i]**2+z[i]**2))
    v.append(np.sqrt(vx[i]**2+vy[i]**2+vz[i]**2))

# Find exact time of pericenter
peri = min(r)  # distance of pericenter
peri_t = t[r.index(peri)]  # corresponding time
v_max = v[r.index(peri)]
v_max_test = max(v)

print(str(peri) + " kpc")
print(str(v_max) + " km/s", str(v_max_test) + " km/s")
print(str(peri_t) + " Gyr")

# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t, x, color='blue', zorder=1, label='$\Delta x$')
ax.plot(t, y, color='red', zorder=1, label='$\Delta y$')
ax.plot(t, z, color='green', zorder=2, label='$\Delta z$')
ax.plot(t, r, color='k', zorder=3, label='$\Delta r$')
# ax.annotate('t = ' + str(peri_t) + ' Gyr, $\Delta r$ = ' + str(round(peri, 1)) + ' kpc', xy=(peri_t, peri),
#             xytext=(peri_t+1, peri), arrowprops=dict(facecolor='k', shrink=0.05))
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
ax.vlines(peri_t, ymin=ymin, ymax=peri, linestyle='dotted', color='darkgrey')
ax.hlines(peri, xmin=xmin, xmax=peri_t, linestyle='dotted', color='darkgrey')
ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator([peri_t]))
ax.yaxis.set_minor_locator(mpl.ticker.FixedLocator([round(peri, 1)]))
ax.set_xticklabels([str(peri_t)], minor=True)
ax.set_yticklabels([str(round(peri, 1))], minor=True)
# ax.set_xticks(list(ax.get_xticks()) + peri_t)
# ax.set_yticks(list(ax.get_yticks()) + round(peri, 1))
# plt.xticks(list(plt.xticks()[0]) + peri_t, minor=True)
# plt.yticks(list(plt.yticks()[0]) + round(peri, 1))
ax.set_xlim(xmin, xmax), ax.set_ylim(ymin, ymax)

ax.set_xlabel("Time [Gyr]")
ax.set_ylabel("Distance [kpc]")
plt.legend()
fig.tight_layout()

# Save
plt.savefig(picName, dpi=500)
