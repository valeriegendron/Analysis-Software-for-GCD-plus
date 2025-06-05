import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('Agg')
mpl.rcParams['font.size'] = 12

# Parameters
dump_names = ["s050", "s100"]  # name of the dumps used to calculate SFR
dump_numbers = [50, 100]  # corresponding numbers to dump names
dt = 0.01  # time interval between each dump, in Gyr
nbins = [25, 25]  # number of bins in each direction
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
xlim, ylim = 5, 5  # x and y limits of plot in kpc

if plan == 'xy': columns = (0, 1, 6, 25); xlabel, ylabel = 'x [kpc]', 'y [kpc]'
elif plan == 'xz': columns = (0, 2, 6, 25); xlabel, ylabel = 'x [kpc]', 'z [kpc]'
elif plan == 'yz': columns = (1, 2, 6, 25); xlabel, ylabel = 'y [kpc]', 'z [kpc]'

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(autoscale_on=False, xlim=(-xlim, xlim), ylim=(-ylim, ylim))
ax.set_aspect('equal')

# Read files
ID_old = np.loadtxt("ascii_output/" + dump_names[0], usecols=25, unpack=True)
x, y, m, ID = np.loadtxt("ascii_output/" + dump_names[1], usecols=columns, unpack=True)

# Compute the time between the two dumps
time = (dump_numbers[1] - dump_numbers[0])*dt*10**9  # in years

# Plot reference galaxy in grey
ax.scatter(x, y, s=5, color='grey')

# Cutting data - only keeping new stars that are within the axi limits
x_cut, y_cut, m_cut = [], [], []
for particle in range(len(x)):
    if (abs(x[particle]) < xlim) and (abs(y[particle]) < ylim):  # within the axi limits
        if ID[particle] not in ID_old:  # new star particle
            m_cut.append(m[particle]), x_cut.append(x[particle]), y_cut.append(y[particle])

# Binning
heatmap, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut, weights=m_cut, bins=nbins)  # x and y axis switched in prevention for pcolormesh

# Plot
im = plt.pcolormesh(xedges, yedges, heatmap/time, cmap=mpl.colormaps["plasma"], norm=mpl.colors.LogNorm())

# Colorbar + labels
cbar = fig.colorbar(im)
cbar.set_label("SFR [M$_\odot$/yr]", rotation=270, verticalalignment='baseline')
ax.set(xlabel=xlabel, ylabel=ylabel)
ax.set_title("t = " + str(dump_numbers[1]*dt) + " Gyr")

# Save map
plt.savefig("sfr_map_" + dump_names[0] + "_" + dump_names[1] + ".png", dpi=500)
