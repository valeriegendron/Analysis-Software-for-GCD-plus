import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

# FOR BOUND PARTICLES ONLY

runs = ["ISOL_A", "TIDES8_h_p2_mm"]  # Must be in order: Isolated run first, run with tides second
nbins = [200, 200]  # number of bins in each direction
plan = "xy"  # plane to be graphed. Can be "xy", "xz" or "yz"
dump_numbers = ["500", "500"]  # in string format, TIDES and ISOL
xcut, ycut = 10, 10  # max extent of first and second axi, in kpc
stars = True  # if True, map star density. If False, map gas density

cbarlabel = 'Density [M$_\odot /$pc$^2$]'
picName = "density_map_"

# Set figure
fig, axs = plt.subplots(1, 2, sharey=True, sharex=True, constrained_layout=True)

# Read data
if plan == "xy": columns = (0, 1, 6); x_label = "x [kpc]"; y_label = "y [kpc]"
elif plan == "xz": columns = (0, 2, 6); x_label = "x [kpc]"; y_label = "z [kpc]"
elif plan == "yz": columns = (1, 2, 6); x_label = "y [kpc]"; y_label = "z [kpc]"

if stars: file_name = "s"
else: file_name = "g"

picName += file_name

path_tides = runs[1] + "/diskev/ascii_output/bound_data/detilted/" + file_name + dump_numbers[1] + "r"
path_isol = runs[0] + "/diskev/ascii_output/detilted/" + file_name + dump_numbers[0] + "r"
paths = [path_isol, path_tides]

for run in [1, 0]:
    x, y, m = np.loadtxt(paths[run], usecols=columns, unpack=True)

    # Cutting data
    x_cut, y_cut, m_cut = [], [], []
    for i in range(len(x)):
        if (abs(x[i]) < xcut) and (abs(y[i]) < ycut):
            x_cut.append(x[i]), y_cut.append(y[i]), m_cut.append(m[i])

    # Histogramme
    heatmap, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut, bins=nbins, weights=m_cut)  # x and y axis switched in prevention for pcolormesh

    bin_area = (yedges[1]-yedges[0])*(xedges[1]-xedges[0])*(10**6)  # in pc^2
    # Getting vmin and vmax
    density = heatmap/bin_area
    if run == 1:  # run with tides
        vmin, vmax = np.min(density[np.nonzero(density)]), np.amax(heatmap/bin_area)  # vmin cannot be 0

    # Plot
    im = axs[run].pcolormesh(xedges, yedges, heatmap/bin_area, cmap=mpl.colormaps["plasma"],
                             norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
    axs[run].set_aspect("equal")
    axs[run].set_title(runs[run])

# Colorbar
#cbar_ax = fig.add_axes([0.90, 0.15, 0.01, 0.7])
#cax = fig.add_axes([axs[1].get_position().x1+0.01, axs[1].get_position().y0, 0.02, axs[1].get_position().height])
cbar = fig.colorbar(im, ax=axs[1], fraction=0.05, pad=0.04)
cbar.set_label(cbarlabel, rotation=270, verticalalignment='baseline')

# Set labels
for ax in axs.flat:
    ax.set(xlabel=x_label, ylabel=y_label)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

# Save map
picName = picName + "_" + runs[0] + "_" + dump_numbers[0] + "_" + runs[1] + "_" + str(xcut) + "kpc_" + str(nbins[0]) + "bins"
plt.savefig("remnant_density_maps/" + picName + '.png', dpi=500)
