import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

plt.rcParams['font.size'] = 15

times = [0.00, 0.21, 0.40, 0.47, 0.56, 0.64, 0.80, 1.75, 5.00]  # in Gyr
dump_numbers = ["000", "021", "040", "047", "056", "064", "080", "175", "500"]  # format "xxx"
nbins = [200, 200]  # number of bins in each direction
plan = "xy"  # plane to be graphed. Can be "xy", "xz" or "yz"
xcut, ycut = 10, 10  # max extent of first and second axi, in kpc
stars = True  # if True, map star density. If False, map gas density
tides = True  # if True, run with tides. If False, isolated run
bound_stars = False  # if True, only plotting bound stars. If False, plotting every star.

cbarlabel = 'Density [M$_\odot /$pc$^2$]'
picName = "density_map_9panels_"

# Set figure
fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, constrained_layout=True, figsize=(11, 11))
axs = [axes[0, 0], axes[0, 1], axes[0, 2], axes[1, 0], axes[1, 1], axes[1, 2], axes[2, 0], axes[2, 1], axes[2, 2]]

# Read data
if plan == "xy": columns = (0, 1, 6); x_label = "x [kpc]"; y_label = "y [kpc]"
elif plan == "xz": columns = (0, 2, 6); x_label = "x [kpc]"; y_label = "z [kpc]"
elif plan == "yz": columns = (1, 2, 6); x_label = "y [kpc]"; y_label = "z [kpc]"

if stars: file_name = "s"
else: file_name = "g"

picName += file_name

if tides:
    if bound_stars:
        path = "ascii_output/bound_data/detilted/" + file_name  # Run with tides
        picName += "_bound"
    else:
        path = "ascii_output/" + file_name
        picName += "_all"
else: path = "ascii_output/detilted/" + file_name  # Isolated run

# Loop on all times specified
for time in range(len(times)):
    x, y, m = np.loadtxt(path + dump_numbers[time] + "r", usecols=columns, unpack=True)

    # Cutting data
    x_cut, y_cut, m_cut = [], [], []
    for i in range(len(x)):
        if (abs(x[i]) < xcut) and (abs(y[i]) < ycut):
            x_cut.append(x[i]), y_cut.append(y[i]), m_cut.append(m[i])

    # Histogramme
    heatmap, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut, bins=nbins, weights=m_cut)  # x and y axis switched in prevention for pcolormesh

    bin_area = (yedges[1]-yedges[0])*(xedges[1]-xedges[0])*(10**6)  # converted in pc^2
    # Getting vmin and vmax
    density = heatmap/bin_area
    if time == 0:  # first time of list. So that all maps get the same vmin and vmax
        vmin, vmax = np.min(density[np.nonzero(density)]), np.amax(heatmap/bin_area)  # vmin cannot be 0

    # Plot
    im = axs[time].pcolormesh(xedges, yedges, heatmap/bin_area, cmap=mpl.colormaps["plasma"],
                             norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax))

    #axs[time].set_title("t = " + str(times[time]) + " Gyr")
    axs[time].set_title("t = {0:.2f} Gyr".format(times[time]))
    axs[time].set_xlim(-xcut, xcut), axs[time].set_ylim(-ycut, ycut)
    axs[time].set_aspect("equal")

    picName = picName + "_" + dump_numbers[time]

# Colorbar
#cbar_ax = fig.add_axes([0.91, 0.15, 0.01, 0.7])
cbar = fig.colorbar(im, ax=[axs[2], axs[8]], shrink=0.87, aspect=30)  # colorbar to the right of figure
cbar.set_label(cbarlabel, rotation=270, verticalalignment='baseline')

# Set labels
for ax in axes.flat:
    ax.set(xlabel=x_label, ylabel=y_label)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axes.flat:
    ax.label_outer()

# Save map
picName = picName + "_" + plan + "_" + str(xcut) + "kpc_" + str(nbins[0]) + "bins"
plt.savefig(picName + '.png', dpi=500)
