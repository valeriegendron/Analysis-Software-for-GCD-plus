# This code assumes a simulation of 5 Gyr and a dt = 0.01 Gyr.
# If for example we had a simulation of 3 Gyr, we would need to write "if 300 % n_dt !=0", instead of 500
# If for example dt = 0.02 Gyr and we wanted bins 3 times that size (0.06 Gyr), we would need to set n_dt = 6

import numpy as np
import matplotlib.pyplot as plt
import sys


# Settings
n_dt = [20, 20]  # number of dt we want the bins width to be
runs = [["ISOL_G", "TIDES_G"], ["ISOL_H", "TIDES_H"], ["ISOL9_h_p3_mm", "TIDES9_h_p3_mm"],
        ["ISOL10_h_p3_mm", "TIDES10_h_p3_mm"]]
sburst = [[0.2, 1.8], [0.2, 0.4, 0.6, 1.6], [0.2, 1.4], [0.2, 1.6]]
#runs = ["ISOL8_h", "TIDES8_h_a", "TIDES8_h_a2"]
fill_bool = [True, False]
linewidths = [1.5, 2.0]
alphas = [0.4, 1.0]
alphas_squares = [0.2, 0.07]
hatches = ['', 'x']
#colors = ["#5d06e9", "tab:orange", "tab:red"]
#colors = ["#05cad2", "#8c0404"]
colors = ["#6f6f6f", "#d1242f"]
#colors = ["#6f6f6f", "#d1242f", "#fa7b0e"]
#colors = ["#6f6f6f", "#d1242f", "#fa7b0e", "#8c048b"]
#zorders = [3, 2, 1]
zorders = [3, 4]
zorders_sburst = [1, 2]
file_name = "sfr_global_ID_data"
picName = "sfr_global_hist"
x_label = "Time [Gyr]"
y_label = "SFR [M$_\odot$/yr]"

# Figure setting
fig, axs = plt.subplots(2, 3, sharey='row', constrained_layout=True, figsize=(11, 7))
axes = [axs[0, 0], axs[0, 1], axs[0, 2], axs[1, 0], axs[1, 1]]

for pair in range(len(runs)):
    for run in range(len(runs[pair])):
        time, sfr = np.loadtxt(runs[pair][run] +"/diskev/" + file_name, usecols=(0, 1), unpack=True)

        i = 0
        if 500 % n_dt[run] != 0:
            print("Choose another n_dt so that all bins may be equal.")
            sys.exit()
        elif n_dt != 1:
            sfr_n, time_n = [], []
            time_n.append(time[0])
            while i < (len(sfr)-1):
                sfr_i = sum(sfr[i:(i+n_dt[run])])/n_dt[run]
                time_i = time[i+n_dt[run]]
                sfr_n.append(sfr_i), time_n.append(time_i)
                i += n_dt[run]

        # time_middle = []
        # for j in range(len(time_n)-1):
        #     time_middle.append((time_n[j+1]-time[j])/2)

        # plt.scatter(time_middle, sfr_n, color=colors[run], label=runs[run], zorder=zorders[run], s=10)
        # plt.plot(time_middle, sfr_n, color=colors[run], label=runs[run], zorder=zorders[run])
        axes[pair].stairs(sfr_n, time_n, fill=fill_bool[run], linewidth=linewidths[run], alpha=alphas[run], color=colors[run],
                  label=runs[pair][run], zorder=zorders[run])
        if run == 1:  # run with tides
            picName += ("_" + runs[pair][run])
            axes[pair].legend(loc='upper right')

for i in range(len(sburst)):
    for j in range(len(sburst[i])):
        axes[i].axvline(x=(sburst[i])[j], linestyle='dotted', color='k')  # dotted lines delimiting the starburst(s)
    for j in range(int(len(sburst[i])/2)):  # ONLY WORKS WHEN THERE'S NO MORE THAN 2 STARBURSTS
        axes[i].axvspan(xmin=(sburst[i])[2*j], xmax=(sburst[i])[2*j+1], color=colors[1], zorder=zorders_sburst[j], alpha=alphas_squares[j], hatch=hatches[j])
# plt.axvline(x=0.9, linestyle='dotted', color='k'), plt.axvline(x=1.8, linestyle='dotted', color='k')
# plt.axvspan(xmin=0.9, xmax=1.8, color=colors[1], zorder=1, alpha=0.2)
# plt.axvline(x=1.9, linestyle='dotted', color='k'), plt.axvline(x=4.5, linestyle='dotted', color='k')
# plt.axvspan(xmin=1.9, xmax=4.5, color=colors[1], zorder=2, alpha=0.2)

# # Set labels
# for ax in axs.flat:
#     ax.set(xlabel=x_label, ylabel=y_label)
# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()
# Set labels
axes[0].set_xticklabels([])
for ax in range(1, len(axes)):
    axes[ax].set_xlabel(x_label)
axs[0, 0].set_ylabel(y_label), axs[1, 0].set_ylabel(y_label)
axs[1, 1].axis("off"), axs[1, 2].axis("off")
# axs[0, 1].set_xlabel(x_label), axs[0, 2].set_xlabel(x_label)

# Save file
plt.savefig(picName + ".png", dpi=500)
