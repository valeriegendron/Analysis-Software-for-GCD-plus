import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

mpl.use('Agg')
mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.9  # size of scatter markers

# Input data
dump_name = "s500"  # format sxxx, where the 'x' are numbers. Must be in string.
dump_number = 500
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
xlim, ylim = 200, 200  # x and y limits of plot in kpc
light_theme = False  # True for light theme, False for dark theme

if not light_theme:
    plt.style.use('dark_background')

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
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
pic_name = "galaxy_map_stars_" + plan + '_' + str(dump_number) + '_' + str(xlim) + 'kpc'
colors = np.array(["", "darkgrey", "darkviolet", "deepskyblue", "gold"])

isol = input("Is the run isolated? (y/n) ")
if isol == 'y':
    x_isol, y_isol = np.loadtxt("ascii_output/data_centered/" + dump_name, usecols=columns, unpack=True)
    ax.scatter(x_isol, y_isol, color="deeppink")

    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.set_aspect("equal")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Save figure
    fig.tight_layout()
    pic_name += "_isol"
    if not light_theme:
        pic_name += '_dark'
    plt.savefig(pic_name + ".png")
    sys.exit()

# Read file
cat, dumps, line = np.loadtxt("stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
cat = [int(i) for i in cat]  # to make sure we have an array of integers
line = [int(i) for i in line]
cat = np.array(cat)

print("Reading and plotting dump " + dump_name + "...")
# x_cat1, x_cat2, x_cat3, x_cat4 = [], [], [], []
# y_cat1, y_cat2, y_cat3, y_cat4 = [], [], [], []
# x_cat, y_cat = [], []
x, y = np.loadtxt("ascii_output/data_centered/" + dump_name, usecols=columns, unpack=True)

index_min = np.searchsorted(dumps, dump_number - 0.5)
index_max = np.searchsorted(dumps, dump_number + 0.5)-1

# x_cat = x[int(line[index_min]):int(line[index_max])]
# y_cat = y[int(line[index_min]):int(line[index_max])]
x_cat = np.take(x, line[index_min:index_max])
y_cat = np.take(y, line[index_min:index_max])
cat_plot = cat[index_min:index_max]

# Plot
ax.scatter(x_cat, y_cat, c=colors[cat_plot])
# axs[0, i].scatter(x_cat1, y_cat1, s=0.2, c="darkgrey", label="Old and bound")
# axs[0, i].scatter(x_cat2, y_cat2, s=0.2, c="darkviolet", label="New and bound")
# axs[0, i].scatter(x_cat3, y_cat3, s=0.2, c="deepskyblue", label="Old and ICL")
# axs[0, i].scatter(x_cat4, y_cat4, s=0.2, c="gold", label="New and ICL")

ax.set_xlim(-xlim, xlim)
ax.set_ylim(-ylim, ylim)
ax.set_aspect("equal")

ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)

# Save figure
fig.tight_layout()
if not light_theme:
    pic_name += '_dark'
plt.savefig(pic_name + ".png")
