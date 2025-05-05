import numpy as np
import matplotlib.pyplot as plt


run = 'TIDES2_h'
path = run + "/diskev/sortie_data_centered"
plane = 'yz'  # plane to be plotted, can be 'xy', 'xz' or 'yz'
picName = 'orbit_' + plane
cbarlabel = 'Time [Gyr]'

plt.style.use('dark_background')
# Read data
t, x, y, z, vx, vy, vz = np.loadtxt(path, usecols=(0, 1, 2, 3, 4, 5, 6), unpack=True)

# Get data corresponding to chosen plane
if plane == 'xy' or plane == 'yx':
    a1, a2, v1, v2 = x, y, vx, vy
    label1, label2 = "x [kpc]", "y [kpc]"
elif plane == 'xz' or plane == 'zx':
    a1, a2, v1, v2 = x, z, vx, vz
    label1, label2 = "x [kpc]", "z [kpc]"
elif plane == 'yz' or plane == 'zy':
    a1, a2, v1, v2 = y, z, vy, vz
    label1, label2 = "y [kpc]", "z [kpc]"

# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(a1, a2, c=t, zorder=1, s=2)
cbar = plt.colorbar()
cbar.set_label(cbarlabel, rotation=270, verticalalignment='baseline')

i = len(a1) - 1  # last index
ax.arrow(a1[i], a2[i], v1[i]/(np.sqrt(v1[i]**2+v2[i]**2)), v2[i]/(np.sqrt(v1[i]**2+v2[i]**2)), width=1, zorder=2)  # final velocity vector
ax.plot([0], [0], marker='+', color='g', markersize=16)
ax.set_xlabel(label1)
ax.set_ylabel(label2)
fig.tight_layout()

# Save
plt.savefig(picName + '_' + run, dpi=500)
