import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.size'] = 15

# FOR BOUND PARTICLES ONLY

# Input
runs = [["ISOL8_h", "TIDES8_h_a"], ["ISOL8_h", "TIDES8_h_a2"], ["ISOL8_h", "TIDES8_h_r"], ["ISOL8_h", "TIDES8_h_r2"],
        ["ISOL8_h", "TIDES8_h_p_m"], ["ISOL8_h", "TIDES8_h_p_mm"], ["ISOL8_h", "TIDES8_h_p2_mm"],
        ["ISOL8_h", "TIDES8_h_p3_mm"], ["ISOL9_h_p3_mm", "TIDES9_h_p3_mm"], ["ISOL_G", "TIDES_G"],
        ["ISOL_H", "TIDES_H"], ["ISOL10_h_p3_mm", "TIDES10_h_p3_mm"]]
sburst = [[0.4, 1.4], [0.8, 1.6], [0.2, 1.2], [0.8, 1.8], [0.2, 1.4], [0.2, 1.2], [0.2, 1.4], [0.2, 1.4],
          [0.2, 1.4], [0.2, 1.8], [0.2, 0.4], [0.2, 1.6]]
names = [["I07", "T10"], ["I07", "T11"], ["I07", "T14"], ["I07", "T15"], ["I07", "T16"], ["I07", "T17"], ["I07", "T18"],
         ["I07", "T19"], ["I06", "T08"], ["I04", "T06"], ["I05", "T07"], ["I08", "T20"]]
dump_number = "500"
dt = 0.01  # in Gyr
nbins = [60, 60]  # for isolated run and run with tides, respectively
colors = ["#c5c5c5", "darkorchid"]
linewidths = [1.5, 2.0]
fill_bool = [True, False]
#paths = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]
path = "/diskev/ascii_output/s"

choice = input("Press (1) to get the age distrubtion of stars or press (2) to get the formation epoch distribution,"
               " for dump " + dump_number + ": ")
while choice != '1' and choice != '2':
    choice = input("Wrong key. to get the age distrubtion of stars or press (2) to get the formation"
                   " epoch distribution, for dump " + dump_number + ": ")
if choice == '1':
    x_label = "Age [Gyr]"
    pic_name = "star_age_12panels"
else:
    x_label = "Formation epoch [Gyr]"
    pic_name = "star_fepoch_12panels"
y_label = "Stellar mass [M$_\odot$]"

# Setting figure
fig, axes = plt.subplots(3, 4, sharex=True, constrained_layout=True, figsize=(15, 11))
axs = [axes[0, 0], axes[0, 1], axes[0, 2], axes[0, 3], axes[1, 0], axes[1, 1], axes[1, 2], axes[1, 3], axes[2, 0],
       axes[2, 1], axes[2, 2], axes[2, 3]]
for ax in range(len(axs)-2):  # excluding TIDES10_h_p3_mm
    axs[ax].sharey(axs[ax+1])

for pair in range(len(runs)):
    for run in range(len(runs[pair])):
        # Read data
        m, age = np.loadtxt(runs[pair][run] + path + dump_number, usecols=(6, 18), unpack=True)

        # Convert age units to Gyr
        age = age/(10**9)  # operation on array

        if choice == '1':
            sburst[pair][run] = int(dump_number)*dt - sburst[pair][run]
        if choice == '2':
            for j in range(len(age)):
                age[j] = int(dump_number)*dt - age[j]  # "age" becomes formation epoch
                # if age[j] < 0:
                #     age[j] = 0

        # Make histogram
        plt.sca(axs[pair])
        sns.histplot(x=age, weights=m, bins=nbins[run], kde=False, color=colors[run], element="step",
                     fill=fill_bool[run], linewidth=linewidths[run], label=names[pair][run])
        if run == 1:  # run with tides
            axs[pair].legend(loc='upper right')

# Starbursts stars
for i in range(len(sburst)):
    for j in range(len(sburst[i])):
        axs[i].axvline(x=(sburst[i])[j], linestyle='dotted', color='k')  # dotted lines delimiting the starburst(s)
    for j in range(int(len(sburst[i])/2)):  # ONLY WORKS WHEN THERE'S NO MORE THAN 2 STARBURSTS
        axs[i].axvspan(xmin=(sburst[i])[2*j], xmax=(sburst[i])[2*j+1], color=colors[1], alpha=0.2)

# Set labels
for i in range(3):
    axes[i, 1].set_yticklabels([]), axes[i, 2].set_yticklabels([])
    axes[i, 1].set_ylabel("empty", color='w'), axes[i, 2].set_ylabel("empty", color='w'), axes[i, 3].set_ylabel("empty", color='w')
    axes[i, 0].set_ylabel(y_label)

    if i < 2:
        axes[2, i].set_xlabel(x_label)
        axes[i, 3].set_yticklabels([])
axes[2, 2].set_xlabel(x_label), axes[2, 3].set_xlabel(x_label)
# for ax in range(1, len(axes)):
#     axes[ax].set_xlabel(x_label)
# axes[0, 0].set_ylabel(y_label), axes[1, 0].set_ylabel(y_label)
# for ax in axes.flat:
#     ax.set(xlabel=x_label, ylabel=y_label)
# Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axes.flat:
#     ax.label_outer()

# Save figure
plt.savefig(pic_name + "_" + str(nbins) + "bins_" + dump_number)
