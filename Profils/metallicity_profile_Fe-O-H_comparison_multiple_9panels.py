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
runs1 = [["ISOL_I", "ISOL_G", "ISOL_A", "ISOL_J", "ISOL9_h_p3_mm", "ISOL_H", "ISOL8_h"], ["TIDES9_h_p3_mm", "TIDES8_h_p3_mm", "TIDES_H"]]
dump_numbers1 = [["452", "399", "313", "251", "172", "098", "154"], ["500", "500", "500"]]
labels1 = [["I15 (4.52 Gyr)", "I04 (3.99 Gyr)", "I11 (3.13 Gyr)", "I10 (2.51 Gyr)", "I06 ( 1.72 Gyr)", "I05 (0.98 Gyr)", "I07 (1.54 Gyr)"], ["T08", "T19", "T07"]]

runs2 = [["ISOL_A", "ISOL_J", "ISOL_E", "ISOL9_h_p3_mm", "ISOL_F", "ISOL_H", "ISOL8_h", "ISOL_D"], ["TIDES8_h_p2_mm", "TIDES8_h_r"]]
dump_numbers2 = [["500", "500", "484", "354", "264", "265", "272", "122"], ["500", "500"]]
labels2 = [["I11 (5.00 Gyr)", "I10 (5.00 Gyr)", "I16 (4.84 Gyr)", "I06 (3.54 Gyr)", "I12 (2.64 Gyr)", "I05 (2.65 Gyr)", "I07 (2.72 Gyr)", "I13 (1.22 Gyr)"], ["T18", "T14"]]

runs3 = [["ISOL_D", "ISOL_D", "ISOL_D"], ["TIDES8_h_p_mm", "TIDES8_h_p_m", "TIDES8_h_r2"]]
dump_numbers3 = [["297", "321", "440"], ["500", "500", "500"]]
labels3 = [["I13 (2.97 Gyr)", "I13 (3.21 Gyr)", "I13 (4.40 Gyr)"], ["T17", "T16", "T15"]]

runs_all = [runs1, runs2, runs3]
dump_numbers_all = [dump_numbers1, dump_numbers2, dump_numbers3]
labels_all = [labels1, labels2, labels3]
nbins = 40  # for isolated runs and run with tides
#colors = [["#05cad2"], ["#8c0404"]]
#colors = [["k", "#2a2a2a", "#3f3f3f", "#545454", "#6a6a6a", "#7f7f7f", "#a9a9a9", "#bebebe"], ["darkmagenta"]]

#colors = [["k", "k", "k", "k", "k", "k", "k", "k"], ["darkmagenta", "dodgerblue", "forestgreen"]]
colors = [["maroon", "orangered", "orange", "gold", "olivedrab", "deeppink", "indigo", "chocolate"],
          ["darkmagenta", "dodgerblue", "forestgreen"]]
#markerstyles = ["x", "."]

#linestyles = [["--", (0,(1,10)), (0,(3,10,1,10)), (0,(3,5,1,5,1,5)), (0,(5,10)), (0,(1,1)), (0,(3,1,1,1)), (0,(3,10,1,10,1,10))], ["-", "-", "-"]]
linestyles = [["--"]*8, ["-"]*3]

paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]
paths2 = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]
ylabels = ["[O/H]", "[Fe/H]", "[O/Fe]"]
mean = True  # if True, compute mean metallicity in each bin. If False, total metallicity in each bin.

# Setting figure
fig, axes = plt.subplots(3, 3, sharex='col', constrained_layout=True, figsize=(15, 11))

# Sun
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

if mean:
    for label in range(len(ylabels)):
        ylabels[label] += "$_\mathrm{mean}$"
else:
    for label in range(len(ylabels)):
        ylabels[label] += "$_\mathrm{total}$"

# LOOP ON RUNS
for column in range(len(runs_all)):
    for kind in range(len(runs_all[column])):
        for i in range(len(runs_all[column][kind])):
            #colors = iter(cm.gist_rainbow(np.linspace(0, 1, 7)))  # a color for each element plotted

            # Read data
            R = np.loadtxt(runs_all[column][kind][i] + paths[kind] + dump_numbers_all[column][kind][i] + "r_v", usecols=11)
            m, He, O, Fe, Z = np.loadtxt(runs_all[column][kind][i] + paths2[kind] + dump_numbers_all[column][kind][i], usecols=(6, 7, 10, 14, 15), unpack=True)  # m, He, O, Fe, Z

            # Computing metallicities
            H = m - He - Z  # operation on arrays
            Fe_H, O_H, O_Fe = [], [], []
            for j in range(len(Fe)):
                Fe_H.append(np.log10(Fe[j] / H[j]) - np.log10(Fe_sun / H_sun))  # [Fe/H]
                O_H.append(np.log10(O[j] / H[j]) - np.log10(O_sun / H_sun))  # [O/H]
                O_Fe.append(np.log10(O[j] / Fe[j]) - np.log10(O_sun / Fe_sun))  # [O/Fe]
            data_Z = np.column_stack((O_H, Fe_H, O_Fe))

            # Bin radius
            #count, R_bins = np.histogram(R, bins=nbins[i])
            count, R_bins = np.histogram(R, histedges_equalN(R, nbins))

            # Computing mean/total metallicity for each radius bin
            data_Z_bins, R_plot = np.zeros((len(R_bins)-1, 3)), []
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
            for Z in range(data_Z_bins.shape[1]):  # a plot for each ratio ([Fe/H], [O/H], [O/Fe])
                #c = next(colors)
                axes[Z, column].plot(R_plot, data_Z_bins[:, Z], color=colors[kind][i], label=labels_all[column][kind][i], linewidth=1.00, linestyle=linestyles[kind][i])
                #axes[Z].set_yscale("log")
                axes[Z, column].set_xscale("log")
                axes[Z, column].tick_params(axis='x', labelsize=15), axes[Z, column].tick_params(axis='y', labelsize=15)

                #handles.append(mpatches.Patch(color=c))
                if (i == 0) and (column == 0):  # only writing each element once
                    axes[Z, column].set_ylabel(ylabels[Z], fontsize=15)

    axes[2, column].set_xlabel("Radius [kpc]", fontsize=15)
    axes[0, column].legend()

# axes[2].set_xlabel("Radius [kpc]", fontsize=15)
# axes[0].legend()

# Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axes.flat:
#     ax.label_outer()
# axes[1, 3].axis("off")

# Save figure
if mean: option = "mean_"
else: option = "total_"
plt.savefig("remnant_metallicity_profiles_part2/metallicity_profiles_Fe-O-H_multiple_9panels")
