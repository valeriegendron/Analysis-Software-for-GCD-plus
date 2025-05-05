import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# FOR BOUND PARTICLES ONLY


# Function to get non-uniform bins with same number of particles within (copied from farenorth on Stack Overflow)
def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))


# Input
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_numbers = ["500", "500"]
nbins = [40, 40]  # for isolated run and run with tides, respectively
#colors = [["#05cad2"], ["#8c0404"]]
colors = ["k", "darkmagenta"]
#markerstyles = ["x", "."]
linestyles = ["--", "-"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]
paths2 = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]
ylabels = ["[Fe/H]", "[O/H]", "[O/Fe]"]
mean = True  # if True, compute mean metallicity in each bin. If False, total metallicity in each bin.

# Setting figure
fig, axes = plt.subplots(3, 1, sharex=True, constrained_layout=True, figsize=(4, 11))

# Sun
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

if mean:
    for label in range(len(ylabels)):
        ylabels[label] += "$_\mathrm{mean}$"
else:
    for label in range(len(ylabels)):
        ylabels[label] += "$_\mathrm{total}$"

# LOOP ON RUNS
for i in range(len(runs)):
    #colors = iter(cm.gist_rainbow(np.linspace(0, 1, 7)))  # a color for each element plotted

    # Read data
    R = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=11)
    m, He, O, Fe, Z = np.loadtxt(runs[i] + paths2[i] + dump_numbers[i], usecols=(6, 7, 10, 14, 15), unpack=True)  # m, He, O, Fe, Z

    # Computing metallicities
    H = m - He - Z  # operation on arrays
    # Fe_H, O_H, O_Fe = [], [], []
    # for j in range(len(Fe)):
    #     Fe_H.append(np.log10(Fe[j] / H[j]) - np.log10(Fe_sun / H_sun))  # [Fe/H]
    #     O_H.append(np.log10(O[j] / H[j]) - np.log10(O_sun / H_sun))  # [O/H]
    #     O_Fe.append(np.log10(O[j] / Fe[j]) - np.log10(O_sun / Fe_sun))  # [O/Fe]
    # data_Z = np.column_stack((Fe_H, O_H, O_Fe))
    data_Z = np.column_stack((H, Fe, O))

    # Bin radius
    #count, R_bins = np.histogram(R, bins=nbins[i])
    count, R_bins = np.histogram(R, histedges_equalN(R, nbins[i]))

    # Computing mean/total metallicity for each radius bin
    data_Z_bins, R_plot = np.zeros((len(R_bins)-1, 3)), []   # data_Z_bins columns: [Fe/H], [O/H], [O/Fe]
    for j in range(len(count)):
        Z_temp_old = np.empty((data_Z.shape[1]))  # to compute the mean/total of each bin
        R_plot.append((R_bins[j] + R_bins[j+1])/2)  # get the middle value of each bin
        for k in range(data_Z.shape[0]):
            if R_bins[j] <= R[k] < R_bins[j+1]:  # particle in radius bin
                Z_temp_new = np.row_stack([Z_temp_old, data_Z[k, :]])  # add whole row
                Z_temp_old = Z_temp_new  # update for next iteration

        Z_temp = np.delete(Z_temp_new, 0, 0)  # deleting first row, is empty
        if Z_temp.shape[0] != 0:  # compute mean/total of each column if the radius bin is not empty
            if mean:
                # [Fe/H]
                data_Z_bins[j, 0] = np.log10(np.sum(Z_temp[:, 1])/np.sum(Z_temp[:, 0])) - np.log10(Fe_sun / H_sun)
                # [O/H]
                data_Z_bins[j, 1] = np.log10(np.sum(Z_temp[:, 2]) / np.sum(Z_temp[:, 0])) - np.log10(O_sun / H_sun)
                # [O/Fe]
                data_Z_bins[j, 2] = np.log10(np.sum(Z_temp[:, 2]) / np.sum(Z_temp[:, 1])) - np.log10(O_sun / Fe_sun)
            #else: data_Z_bins[j, Z] = np.sum(Z_temp[:, Z])  # total metallicity of bin
        else:
            data_Z_bins[j, Z] = np.nan


    # Plot scatter plots
    for Z in range(data_Z_bins.shape[1]):  # a plot for each ratio ([Fe/H], [O/H], [O/Fe])
        #c = next(colors)
        axes[Z].plot(R_plot, data_Z_bins[:, Z], color=colors[i], label=runs[i], linewidth=1.00, linestyle=linestyles[i])
        #axes[Z].set_yscale("log")
        axes[Z].set_xscale("log")
        axes[Z].tick_params(axis='x', labelsize=15), axes[Z].tick_params(axis='y', labelsize=15)

        #handles.append(mpatches.Patch(color=c))
        if i == 0:  # only writing each element once
            axes[Z].set_ylabel(ylabels[Z], fontsize=15)

axes[2].set_xlabel("Radius [kpc]", fontsize=15)
axes[0].legend()

# Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axes.flat:
#     ax.label_outer()
# axes[1, 3].axis("off")

# Save figure
if mean: option = "mean_"
else: option = "total_"
plt.savefig("metallicity_profiles_Fe-O-H_vB_" + option + runs[0] + "_" + runs[1] + "_" + str(nbins) + "bins_" + dump_numbers[0])
