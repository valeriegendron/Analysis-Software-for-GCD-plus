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
light_theme = True  # True for light theme, False for dark theme
option = 0  # 0: Z of all stars, 1: Z of category 1 of stars, 2: Z cat 2, 3: Z cat 3, 4: Z cat 4
Z_option = "[Fe/H]"  # can be "[Fe/H]", "[O/H]" or "[O/Fe]"
compare_option = True  # if True, the metallicity of any star category will have the same vmin and vmax as if we took
# all the stars of the dump, categories confounded. If False, the metallicity of star category 1 will have the vmin
# and vmax found in the list of metallicity of star category 1; the metallicity of star category 2 will have the vmin
# and vmax found in the list of metallicity of star category 2; and so on.

if not light_theme:
    plt.style.use('dark_background')

if plan == 'xy':
    columns = (0, 1, 6, 7, 10, 11, 14, 15)
    xlabel, ylabel = 'x [kpc]', 'y [kpc]'
elif plan == 'xz':
    columns = (0, 2, 6, 7, 10, 11, 14, 15)
    xlabel, ylabel = 'x [kpc]', 'z [kpc]'
elif plan == 'yz':
    columns = (1, 2, 6, 7, 10, 11, 14, 15)
    xlabel, ylabel = 'y [kpc]', 'z [kpc]'

# Sun
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

# Setting figure
fig, ax = plt.subplots(1, 1, figsize=(8, 8))
pic_name = "metallicity_map_stars_" + plan + '_' + str(dump_number) + '_' + str(xlim) + 'kpc'
colors = np.array(["", "darkgrey", "darkviolet", "deepskyblue", "gold"])
t = np.array([0, 0.5, 1.0, 1.0, 1.0])
zorders = np.array([0, 1, 2, 3, 4])

# Read file
x, y, m_tot, He, O, Ne, Fe, Z = np.loadtxt("ascii_output/data_centered/" + dump_name, usecols=columns, unpack=True)

cat, dumps, line = np.loadtxt("stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
cat = [int(i) for i in cat]  # to make sure we have an array of integers
line = [int(i) for i in line]
#cat = np.array(cat)

# To separate the metallicities in the 4 categories of stars, we need to use the file "stars_separated_in_4"
# We only use the information related to the dump number chosen
index_min = np.searchsorted(dumps, dump_number - 0.5)
index_max = np.searchsorted(dumps, dump_number + 0.5)

x_cat, y_cat, m_tot_cat, He_cat, O_cat, Ne_cat, Fe_cat, Z_cat = np.take(x, line[index_min:index_max]),\
                                                                np.take(y, line[index_min:index_max]),\
                                                                np.take(m_tot, line[index_min:index_max]),\
                                                                np.take(He, line[index_min:index_max]),\
                                                                np.take(O, line[index_min:index_max]),\
                                                                np.take(Ne, line[index_min:index_max]),\
                                                                np.take(Fe, line[index_min:index_max]),\
                                                                np.take(Z, line[index_min:index_max])
cat_plot = cat[index_min:index_max]
# Count how much elements are in each of the four categories
cat_1, cat_2, cat_3, cat_4 = cat_plot.count(1), cat_plot.count(2), cat_plot.count(3), cat_plot.count(4)

# Computing metallicities
H_cat = m_tot_cat - He_cat - Z_cat  # operation on arrays
Fe_H_cat, O_H_cat, O_Fe_cat, Ne_O_cat = [], [], [], []
for i in range(len(Fe_cat)):
    Fe_H_cat.append(np.log10(Fe_cat[i]/H_cat[i]) - np.log10(Fe_sun/H_sun))  # [Fe/H]
    O_H_cat.append(np.log10(O_cat[i]/H_cat[i]) - np.log10(O_sun/H_sun))  # [O/H]
    O_Fe_cat.append(np.log10(O_cat[i]/Fe_cat[i]) - np.log10(O_sun/Fe_sun))  # [O/Fe]

# Separate the datasets in the 4 star categories
# Since we read info for a single dump, we'll only have cat_1, cat_2, cat_3, cat_4 (i.e. they won't repeat)
first_indexes = [0, cat_1, cat_1+cat_2, cat_1+cat_2+cat_3]
last_indexes = [cat_1, cat_1+cat_2, cat_1+cat_2+cat_3, cat_1+cat_2+cat_3+cat_4]
if cat_4 == 0:
    first_indexes[3], last_indexes[3] = 0, 0  # we'll have an empty list

# Which metallicity to plot
if Z_option == "[Fe/H]":
    cbarlabel = "[Fe/H]"
    Z_cat = Fe_H_cat
    pic_name += "_FeH"
elif Z_option == "[O/H]":
    cbarlabel = "[O/H]"
    Z_cat = O_H_cat
    pic_name += "_OH"
elif Z_option == "[O/Fe]":
    cbarlabel = "[O/Fe]"
    Z_cat = O_Fe_cat
    pic_name += "_OFe"

# Compare option
if compare_option: vmin = min(Z_cat); vmax = max(Z_cat); pic_name += "_compare"
else: vmin = min(Z_cat[first_indexes[option-1]:last_indexes[option-1]]); vmax = max(Z_cat[first_indexes[option-1]:last_indexes[option-1]])

# Plot
if option == 0:
    plt.scatter(x_cat, y_cat, c=Z_cat, cmap=mpl.colormaps['plasma'], alpha=t[cat_plot])
elif option == 1:
    zorder = np.array([4, 1, 2, 3])
    pic_name += '_cat1'
    for i in range(0, 4):
        if i == option - 1:
            color = Z_cat[first_indexes[i]:last_indexes[i]]
            im = plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                             c=color, cmap=mpl.colormaps['plasma'], vmin=vmin, vmax=vmax, zorder=zorders[i])
            cbar = plt.colorbar(im)
        else:
            color = "silver"
            plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                        c=color, zorder=zorders[i])
if option == 2:
    zorder = np.array([1, 4, 2, 3])
    pic_name += '_cat2'
    for i in range(0, 4):
        if i == option - 1:
            color = Z_cat[first_indexes[i]:last_indexes[i]]
            im = plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                             c=color, cmap=mpl.colormaps['plasma'], vmin=vmin, vmax=vmax, zorder=zorders[i])
            cbar = plt.colorbar(im)
        else:
            color = "silver"
            plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                        c=color, zorder=zorders[i])
if option == 3:
    zorder = np.array([1, 2, 4, 3])
    pic_name += '_cat3'
    for i in range(0, 4):
        if i == option - 1:
            color = Z_cat[first_indexes[i]:last_indexes[i]]
            im = plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                             c=color, cmap=mpl.colormaps['plasma'], vmin=vmin, vmax=vmax, zorder=zorders[i])
            cbar = plt.colorbar(im)

        else:
            color = "silver"
            plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                        c=color, zorder=zorders[i])
if option == 4:
    zorder = np.array([1, 2, 3, 4])
    pic_name += '_cat4'
    for i in range(0, 4):
        if i == option - 1:
            color = Z_cat[first_indexes[i]:last_indexes[i]]
            im = plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                             c=color, cmap=mpl.colormaps['plasma'], vmin=vmin, vmax=vmax, zorder=zorders[i])
            cbar = plt.colorbar(im)
        else:
            color = "silver"
            plt.scatter(x_cat[first_indexes[i]:last_indexes[i]], y_cat[first_indexes[i]:last_indexes[i]],
                        c=color, zorder=zorders[i])

cbar.set_label(cbarlabel, rotation=270, verticalalignment='baseline')

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
