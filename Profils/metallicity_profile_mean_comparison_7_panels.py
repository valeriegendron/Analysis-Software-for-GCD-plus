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
labels = ["C", "N", "O", "Ne", "Mg", "Si", "Fe"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]
paths2 = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]
mean = True  # if True, compute mean metallicity in each bin. If False, total metallicity in each bin.

# Setting figure
fig, axes = plt.subplots(2, 4, sharex=True, sharey=True, constrained_layout=True, figsize=(14, 8))
axs = [axes[0, 0], axes[0, 1], axes[0, 2], axes[0, 3], axes[1, 0], axes[1, 1], axes[1, 2]]

# ADD LOOP ON RUNS
#handles = []
for i in range(len(runs)):
    #colors = iter(cm.gist_rainbow(np.linspace(0, 1, 7)))  # a color for each element plotted

    # Read data
    R = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=11)
    data_Z = np.loadtxt(runs[i] + paths2[i] + dump_numbers[i], usecols=(8, 9, 10, 11, 12, 13, 14))  # C, N, O, Ne, Mg, Si, Fe

    # Bin radius
    #count, R_bins = np.histogram(R, bins=nbins[i])
    count, R_bins = np.histogram(R, histedges_equalN(R, nbins[i]))

    # Computing mean/total metallicity for each radius bin
    data_Z_bins, R_plot = np.zeros((len(R_bins)-1, 7)), []
    for j in range(len(count)):
        Z_temp_old = np.empty((data_Z.shape[1]))  # to compute the mean/total of each bin
        R_plot.append((R_bins[j] + R_bins[j+1])/2)  # get the middle value of each bin
        for k in range(data_Z.shape[0]):
            if R_bins[j] <= R[k] < R_bins[j+1]:  # particle in radius bin
                Z_temp_new = np.row_stack([Z_temp_old, data_Z[k, :]])  # add whole row
                Z_temp_old = Z_temp_new  # update for next iteration

        Z_temp = np.delete(Z_temp_new, 0, 0)  # deleting first row, is empty
        for Z in range(Z_temp.shape[1]):
            if Z_temp.shape[0] != 0:  # compute mean/total of each column if the radius bin is not empty
                if mean: data_Z_bins[j, Z] = np.mean(Z_temp[:, Z])  # mean metallicity of bin
                else: data_Z_bins[j, Z] = np.sum(Z_temp[:, Z])  # total metallicity of bin
            else:
                data_Z_bins[j, Z] = np.nan


    # Plot scatter plots
    for Z in range(data_Z_bins.shape[1]):  # a plot for each element (C, N, O, Ne, Mg, Si, Fe)
        #c = next(colors)
        axs[Z].plot(R_plot, data_Z_bins[:, Z], color=colors[i], label=labels[Z], linewidth=1.00, linestyle=linestyles[i])
        axs[Z].set_yscale("log")
        axs[Z].set_xscale("log")
        axs[Z].tick_params(axis='x', labelsize=15), axs[Z].tick_params(axis='y', labelsize=15)

        #handles.append(mpatches.Patch(color=c))
        if i == 0:  # only writing each element once
            axs[Z].text(0.9, 0.9, labels[Z], horizontalalignment='right', fontsize=20, transform=axs[Z].transAxes)
            axs[Z].set_xlabel("Radius [kpc]", fontsize=15), axs[Z].set_ylabel("Stellar mass [M$_\odot$]", fontsize=15)
            #axs[Z].legend(labels[Z], loc="upper left")


#handles = [mpatches.Patch(color=line.get_color()) for line in ax.legend_elements()[0]]
# leg1 = ax.legend(handles, labels, bbox_to_anchor=(1.04, 1), loc="upper left", title="Elements")
# ax.add_artist(leg1)
#
#handles = [mlines.Line2D([], [], linestyle=line, color=colors[line]) for line in linestyles]
handles = [mlines.Line2D([], [], linestyle=linestyles[i], color=colors[i]) for i in range(len(linestyles))]
axes[1, 3].legend(handles, runs, loc="center", fontsize=15)

# # Set labels
# for ax in axes.flat:
#     ax.set(xlabel="Radius [kpc]", ylabel="Stellar mass [M$_\odot$]", fontsize=15)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axes.flat:
    ax.label_outer()
axes[1, 3].axis("off")
#ax.legend()
#fig.tight_layout()

# Save figure
if mean: option = "mean_"
else: option = "total_"
plt.savefig("metallicity_profiles_" + option + "7panels_" + runs[0] + "_" + runs[1] + "_" + str(nbins) + "bins_" + dump_numbers[0])
