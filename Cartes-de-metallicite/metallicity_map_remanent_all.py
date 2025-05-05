import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

mpl.use('Agg')
mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.9  # size of scatter markers

# FOR BOUND PARTICLES ONLY

# Input data
runs = ["TIDES8_h_p2_mm", "ISOL_A"]  # Must be in order: Run with tides first, isolated run second
nbins = [200, 200]  # number of bins in each direction
dump_names = ["s500", "s500"]  # format sxxx, where the 'x' are numbers. Must be in string. For TIDES and ISOL respectively
dump_numbers = [500, 500]  # for TIDES and ISOL respectively
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
xlim, ylim = 10, 10  # x and y limits of plot in kpc
light_theme = True  # True for light theme, False for dark theme
mean = True  # if True, compute mean metallicity in each bin. If False, total metallicity in each bin.
cbarlabels = ["[O/H]", "[Fe/H]", "[O/Fe]"]

if not light_theme: plt.style.use('dark_background')

columns_r = (6, 7, 10, 11, 14, 15)
if plan == 'xy': columns = (0, 1); xlabel, ylabel = 'x [kpc]', 'y [kpc]'
elif plan == 'xz': columns = (0, 2); xlabel, ylabel = 'x [kpc]', 'z [kpc]'
elif plan == 'yz': columns = (1, 2); xlabel, ylabel = 'y [kpc]', 'z [kpc]'

# Sun
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

# Setting figure
fig, axs = plt.subplots(3, 2, sharex=True, sharey=True, constrained_layout=True, figsize=(8, 11), dpi=500)
pic_name = "metallicity_map_stars_all_" + plan + '_' + str(xlim) + 'kpc'
paths = [runs[0] + "/diskev/ascii_output/bound_data/", runs[1] + "/diskev/ascii_output/"]  # TIDES, ISOL

if mean:
    for label in range(len(cbarlabels)):
        cbarlabels[label] += "$_\mathrm{mean}$"
else:
    for label in range(len(cbarlabels)):
        cbarlabels[label] += "$_\mathrm{total}$"

vmins, vmaxs = [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]  # will contain vmin and vmax values for [Fe/H], [O/H] and [O/Fe]
for i in range(len(runs)):
    # Read files
    x, y = np.loadtxt(paths[i] + "/detilted/" + dump_names[i] + "r", usecols=columns, unpack=True)
    m_tot, He, O, Ne, Fe, Z = np.loadtxt(paths[i] + dump_names[i], usecols=columns_r, unpack=True)

    # Computing metallicities
    H = m_tot - He - Z  # operation on arrays
    Fe_H, O_H, O_Fe, Ne_O = [], [], [], []
    for j in range(len(Fe)):
        Fe_H.append(np.log10(Fe[j] / H[j]) - np.log10(Fe_sun / H_sun))  # [Fe/H]
        O_H.append(np.log10(O[j] / H[j]) - np.log10(O_sun / H_sun))  # [O/H]
        O_Fe.append(np.log10(O[j] / Fe[j]) - np.log10(O_sun / Fe_sun))  # [O/Fe]

    # Cutting data
    x_cut, y_cut = [], []
    Fe_H_cut, O_H_cut, O_Fe_cut = [], [], []
    for k in range(len(x)):
        if (abs(x[k]) < xlim) and (abs(y[k]) < ylim):
            x_cut.append(x[k]), y_cut.append(y[k])
            Fe_H_cut.append(Fe_H[k]), O_H_cut.append(O_H[k]), O_Fe_cut.append(O_Fe[k])
    Z_data = np.column_stack([O_H_cut, Fe_H_cut, O_Fe_cut])

    # Plot
    #vmins, vmaxs = [np.nan, np.nan, np.nan], [np.nan, np.nan, np.nan]  # will contain vmin and vmax values for [Fe/H], [O/H] and [O/Fe]
    for z in range(3):
        # Histogramme
        heatmap_count, yedges, xedges = np.histogram2d(y=x_cut, x=y_cut,
                                                       bins=nbins)  # x and y axis switched in prevention for pcolormesh
        heatmap_sum, _, _ = np.histogram2d(y=x_cut, x=y_cut, weights=Z_data[:, z],
                                           bins=nbins)  # x and y axis switched in prevention for pcolormesh

        # Mean or total metallicity
        if mean:
            with np.errstate(divide='ignore', invalid='ignore'):  # suppress possible divide-by-zero warnings
                heatmap = heatmap_sum / heatmap_count  # mean metallicity
            option = "_mean"
        else:
            heatmap = heatmap_sum; option = "_sum"  # total metallicity

        # Getting vmin and vmax values
        if i == 0:  # so that runs with tides and isolated have the same colorbar
            vmins[z], vmaxs[z] = np.nanmin(heatmap), np.nanmax(heatmap)
        #im = axs[i].scatter(x_cut, y_cut, c=Z_plot, cmap=mpl.colormaps["plasma"], vmin=vmin, vmax=vmax, s=0.1)
        im = axs[z, i].pcolormesh(xedges, yedges, heatmap, cmap=mpl.colormaps["plasma"],
                                  norm=mpl.colors.Normalize(vmin=vmins[z], vmax=vmaxs[z]))
        axs[z, i].set_aspect("equal")

        # Colorbar
        if i == 1:  # colorbar to the right
            cbar = fig.colorbar(im, ax=axs[z, 1])
            cbar.set_label(cbarlabels[z], rotation=270, verticalalignment='baseline')

    axs[0, i].set_title(runs[i])  # title only once over top subfigures

    pic_name = pic_name + "_" + runs[i]

# Set labels
for ax in axs.flat: ax.set(xlabel=xlabel, ylabel=ylabel)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat: ax.label_outer()

# Save figure
if not light_theme: pic_name += '_dark'
plt.savefig(pic_name + "_" + str(dump_numbers) + option + ".png")
