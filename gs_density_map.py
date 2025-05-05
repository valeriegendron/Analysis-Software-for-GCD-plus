import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm


nbins = [200, 200]  # number of bins in each direction
#vmin, vmax = 2E-3, 4E-2  # min and max value of SFR in colorbar for all runs
plan = "xy"  # plane to be graphed. Can be "xy", "xz" or "yz"
dump_number = "500"  # in string format
xcut, ycut = 10, 10  # max extent of first and second axi, in kpc
stars = True  # if True, map star density. If False, map gas density

cbarlabel = 'Density [M$_\odot /$pc$^2$]'
picName = "density_map_"

# Set figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Read data
if plan == "xy": columns = (0, 1); x_label = "x [kpc]"; y_label = "y [kpc]"
elif plan == "xz": columns = (0, 2); x_label = "x [kpc]"; y_label = "z [kpc]"
elif plan == "yz": columns = (1, 2); x_label = "y [kpc]"; y_label = "z [kpc]"

if stars: file_name = "s"
else: file_name = "g"

path = "ascii_output/bound_data/detilted/" + file_name + dump_number + "r"
x, y = np.loadtxt(path, usecols=columns, unpack=True)

# Cutting data
x_cut, y_cut = [], []
for i in range(len(x)):
    if (abs(x[i]) < xcut) and (abs(y[i]) < ycut):
        x_cut.append(x[i]), y_cut.append(y[i])

# Histogramme
heatmap, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut, bins=nbins)  # x and y axis switched in prevention for pcolormesh

# Plot
im = plt.pcolormesh(xedges, yedges, heatmap, cmap=mpl.colormaps["plasma"], norm=mpl.colors.LogNorm())

# Colorbar + labels
cbar_ax = fig.add_axes([0.90, 0.15, 0.01, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label(cbarlabel, rotation=270, verticalalignment='baseline')
ax.set(xlabel=x_label, ylabel=y_label)
ax.set_aspect("equal")

# Save map
picName = picName + file_name + "_" + plan + "_" + dump_number + "_" + str(xcut) + "kpc_" + str(nbins[0]) + "bins"
plt.savefig(picName + '.png', dpi=500)
