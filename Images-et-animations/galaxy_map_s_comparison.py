import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines
import sys

mpl.use('Agg')
plt.rcParams['font.size'] = 10
#mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.9  # size of scatter markers

# Input data
runs = ["TIDES8_h_a", "TIDES8_h_r2", "TIDES8_h_p3_mm", "TIDES10_h_p3_mm"]
titles = ["T10", "T15", "T19", "T20"]
legend_labels = ["Old and bound", "New and bound", "Old and ICL", "New and ICL"]
dump_name = "s500"  # format sxxx, where the 'x' are numbers. Must be in string.
dump_number = 500
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
xlim, ylim = 200, 200  # x and y limits of plot in kpc

if plan == 'xy':
    columns = (0, 1)
    xlabel, ylabel = 'x [kpc]', 'y [kpc]'
elif plan == 'xz':
    columns = (0, 2)
    xlabel, ylabel = 'x [kpc]', 'z [kpc]'
elif plan == 'yz':
    columns = (1, 2)
    xlabel, ylabel = 'y [kpc]', 'z [kpc]'

# Setting figure
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, constrained_layout=True, figsize=(8, 8))
axs = [axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]]
pic_name = "galaxy_map_stars_" + plan
colors = np.array(["", "darkgrey", "darkviolet", "deepskyblue", "gold"])

for run in range(len(runs)):
    # Read file
    cat, dumps, line = np.loadtxt(runs[run] + "/diskev/stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
    cat = [int(i) for i in cat]  # to make sure we have an array of integers
    line = [int(i) for i in line]
    cat = np.array(cat)

    # x_cat1, x_cat2, x_cat3, x_cat4 = [], [], [], []
    # y_cat1, y_cat2, y_cat3, y_cat4 = [], [], [], []
    # x_cat, y_cat = [], []
    x, y = np.loadtxt(runs[run] + "/diskev/ascii_output/" + dump_name + "r", usecols=columns, unpack=True)  # detilted file but with all stars

    index_min = np.searchsorted(dumps, dump_number - 0.5)
    index_max = np.searchsorted(dumps, dump_number + 0.5)-1

    # x_cat = x[int(line[index_min]):int(line[index_max])]
    # y_cat = y[int(line[index_min]):int(line[index_max])]
    x_cat = np.take(x, line[index_min:index_max])
    y_cat = np.take(y, line[index_min:index_max])
    cat_plot = cat[index_min:index_max]

    # Plot
    axs[run].set_facecolor('k')
    axs[run].scatter(x_cat, y_cat, c=colors[cat_plot])
    # axs[0, i].scatter(x_cat1, y_cat1, s=0.2, c="darkgrey", label="Old and bound")
    # axs[0, i].scatter(x_cat2, y_cat2, s=0.2, c="darkviolet", label="New and bound")
    # axs[0, i].scatter(x_cat3, y_cat3, s=0.2, c="deepskyblue", label="Old and ICL")
    # axs[0, i].scatter(x_cat4, y_cat4, s=0.2, c="gold", label="New and ICL")

    axs[run].set_xlim(-xlim, xlim)
    axs[run].set_ylim(-ylim, ylim)
    axs[run].set_aspect("equal")
    axs[run].set_title(titles[run])

    pic_name += "_" + runs[run]

# Legend
handles = [mlines.Line2D([], [], marker=".", mec=color, mfc=color, ls='', markersize=10) for color in colors[1:]]
axes[0, 0].legend(handles, legend_labels, loc="lower left")

# Set labels
for ax in axes.flat:
    ax.set(xlabel=xlabel, ylabel=ylabel)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axes.flat:
    ax.label_outer()

# Save figure
plt.savefig(pic_name + ".png")
