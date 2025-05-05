import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_names = ["s500", "s500"]  # for isolated run and run with tides respectively
times = [5.00, 5.00]  # corresponding times, in Gyr
fepochs_limits = [0.0, 0.2, 1.3]  # in Gyr
paths = ["/diskev/ascii_output/", "/diskev/ascii_output/bound_data/"]
file_name = 'toomre_'

# Setting figure
fig, axs = plt.subplots(1, 2, constrained_layout=True, dpi=500)

for i in range(len(runs)):
    # Read data
    V, sqUW = np.loadtxt(runs[i] + paths[i] + "/detilted/" + dump_names[i] + "r_v", usecols=(8, 10), unpack=True)

    # Separate stars in categories
    age, ID = np.loadtxt(runs[i] + paths[i] + dump_names[i], usecols=(18, 25), unpack=True)
    ID_0 = np.loadtxt(runs[i] + paths[i] + "s000", usecols=25)

    V_old_stars, V_starburst, V_others = [], [], []
    sqUW_old_stars, sqUW_starburst, sqUW_others = [], [], []
    for line in range(len(ID)):
        if ID[line] in ID_0:  # old star
            V_old_stars.append(V[line]), sqUW_old_stars.append(sqUW[line])
        else:  # stars formed in the simulation
            if fepochs_limits[0] <= (times[i] - age[line]/(10**9)) < fepochs_limits[1]:  # old stars
                V_old_stars.append(V[line]), sqUW_old_stars.append(sqUW[line])
            elif fepochs_limits[1] <= (times[i] - age[line]/(10**9)) <= fepochs_limits[2]:  # starburst stars
                V_starburst.append(V[line]), sqUW_starburst.append(sqUW[line])
            else:  # all other stars
                V_others.append(V[line]), sqUW_others.append(sqUW[line])

    # Plot
    axs[i].set_facecolor('k')
    axs[i].scatter(V_old_stars, sqUW_old_stars, s=0.4, alpha=0.6, zorder=1, color='mediumslateblue',
                   label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
    axs[i].scatter(V_starburst, sqUW_starburst, s=0.4, alpha=0.8, zorder=3, color='gold',
                   label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
    axs[i].scatter(V_others, sqUW_others, s=0.4, alpha=0.4, zorder=2, color='deeppink',
                   label=str(fepochs_limits[2]) + ' - 5.0')
    x_max, y_max = np.abs(axs[i].get_xlim()).max(), np.abs(axs[i].get_ylim()).max()
    axs[i].set_xlim(xmin=-x_max, xmax=x_max)
    axs[i].set_ylim(ymin=0, ymax=y_max)
    axs[i].set_title(runs[i])
    axs[i].set_xlabel("V [km/s]")

    file_name = file_name + runs[i] + "_"

axs[0].set_xlim(xmin=-x_max, xmax=x_max)  # so that both subplots have the same limits
axs[0].set_ylim(ymin=0, ymax=y_max)
axs[0].set_ylim()
axs[0].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[1].yaxis.set_ticklabels([])
lgnd = axs[0].legend(title='Formation epoch [Gyr]', loc='upper left')
for handle in lgnd.legend_handles:
    handle.set_sizes([6.0])

# Save figure
plt.savefig(file_name + str(dump_names))
