import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import TwoSlopeNorm
import matplotlib.cm as cm

mpl.use('Agg')
mpl.rcParams['font.size'] = 12
plt.style.use('dark_background')

# Parameters
runs = ["Af_v2", "I"]  # name of the runs to compare, run with collisions first followed by isolated run
dump_names = [["s000032r", "s000054r"], ["s000025r", "s000039r"]]  # name of the dumps used to calculate SFR (must be detilted first)
# dump_numbers = [[32, 54], [25, 39]]  # corresponding numbers to dump names
time_diff = 0.12  # time difference between both dumps selected, in Gyr
time = 0.30  # time of the second dump of the run with collisions, in Gyr
nbins = [75, 75]  # number of bins in each direction
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
xlim, ylim = 20, 20  # x and y limits of plot in kpc
cbar_label = "$\Delta$SFR [M$_\odot$ yr$^{-1}$ kpc$^{-2}$]"

if plan == 'xy': columns = (0, 1, 6, 25); xlabel, ylabel = 'x [kpc]', 'y [kpc]'
elif plan == 'xz': columns = (0, 2, 6, 25); xlabel, ylabel = 'x [kpc]', 'z [kpc]'
elif plan == 'yz': columns = (1, 2, 6, 25); xlabel, ylabel = 'y [kpc]', 'z [kpc]'

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(autoscale_on=False, xlim=(-xlim, xlim), ylim=(-ylim, ylim))
ax.set_aspect('equal')

for i in range(len(runs)):
    # Read files
    ID_old = np.loadtxt(runs[i] + "/diskev/ascii_output/" + dump_names[i][0], usecols=25, unpack=True)
    x, y, m, ID = np.loadtxt(runs[i] + "/diskev/ascii_output/" + dump_names[i][1], usecols=columns, unpack=True)

    # Cutting data - only keeping new stars that are within the axi limits
    x_cut_old, y_cut_old, m_cut_old = [], [], []  # all stars in the limits
    x_cut, y_cut, m_cut = [], [], []  # new stars in the limits
    for particle in range(len(x)):
        if (abs(x[particle]) < xlim) and (abs(y[particle]) < ylim):  # within the axi limits
            m_cut_old.append(m[particle]), x_cut_old.append(x[particle]), y_cut_old.append(y[particle])
            if ID[particle] not in ID_old:  # new star particle
                m_cut.append(m[particle]), x_cut.append(x[particle]), y_cut.append(y[particle])

    if i == 0:  # run with collisions
        # Plot reference galaxy in grey
        ax.scatter(x, y, s=5, color='grey')

        # Binning
        heatmap, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut, weights=m_cut, bins=nbins)  # x and y axis switched in prevention for pcolormesh
        heatmap_old, yedges_old, xedges_old = np.histogram2d(y=x_cut_old, x=y_cut_old, bins=[yedges, xedges])

    if i == 1:  # isolated run
        heatmap_isol, yedges_isol, xedges_isol = np.histogram2d(y=x_cut, x=y_cut, weights=m_cut, bins=[yedges, xedges])
        heatmap_isol_old, yedges_isol_old, xedges_isol_old = np.histogram2d(y=x_cut_old, x=y_cut_old, bins=[yedges, xedges])

# When there are no particles in a bin, we put a nan instead of 0
heatmap[heatmap_old == 0] = np.nan
heatmap_isol[heatmap_isol_old == 0] = np.nan

# Compute SFR difference
heatmap_diff = heatmap - heatmap_isol

# Divide star mass by surface area
area = []
for i in range(len(xedges)-1):
    area.append((xedges[i+1]-xedges[i])*(yedges[i+1]-yedges[i]))

area_array = np.array(area)  # convert list to numpy array
heatmap_diff = heatmap_diff/area_array


# Plot
norm = TwoSlopeNorm(vmin=np.nanmin(heatmap_diff/time_diff), vcenter=0, vmax=np.nanmax(heatmap_diff/time_diff))  # center white to 0
im = plt.pcolormesh(xedges, yedges, heatmap_diff/time_diff, cmap="seismic", norm=norm)
#im = plt.pcolormesh(xedges, yedges, heatmap_diff/time_diff, cmap="seismic", vmax=np.nanmax(heatmap_diff/time_diff), vmin=-1*np.nanmax(heatmap_diff/time_diff))


# Colorbar + labels
cbar = fig.colorbar(im)
cbar.set_label(cbar_label, rotation=270, verticalalignment='baseline')
ax.set(xlabel=xlabel, ylabel=ylabel)
ax.set_title("t = " + str(time) + " Gyr")

# Save map
plt.savefig("sfr_map_diff_" + runs[0] + "-" + runs[1] + "_" + dump_names[0][0] + "_" + dump_names[0][1] + ".png", dpi=500)
