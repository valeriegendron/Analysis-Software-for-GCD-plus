import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_names = ["s500", "s500"]  # for isolated run and run with tides respectively
dump_numbers = [321, 500]
fepochs_limits = [0.0, 0.2, 1.4]  # in Gyr
paths = ["/diskev/ascii_output/", "/diskev/ascii_output/bound_data/"]
file_name = 'toomre_3components_'

# Setting figure
fig, axs = plt.subplots(3, 2, constrained_layout=True, dpi=500, figsize=(8, 11))

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
            if fepochs_limits[0] <= (dump_numbers[i]*0.01 - age[line]/(10**9)) < fepochs_limits[1]:  # old stars
                V_old_stars.append(V[line]), sqUW_old_stars.append(sqUW[line])
            elif fepochs_limits[1] <= (dump_numbers[i]*0.01 - age[line]/(10**9)) <= fepochs_limits[2]:  # starburst stars
                V_starburst.append(V[line]), sqUW_starburst.append(sqUW[line])
            else:  # all other stars
                V_others.append(V[line]), sqUW_others.append(sqUW[line])

    # Computing mean and standard deviation
    print(runs[i])
    print("V_old_stars mean: " + str(np.mean(V_old_stars)) + " km/s; " + "Std: " + str(np.std(V_old_stars)))
    print("sqUW_old_stars mean: " + str(np.mean(sqUW_old_stars)) + " km/s; " + "Std: " + str(np.std(sqUW_old_stars)))

    print("V_starburst mean: " + str(np.mean(V_starburst)) + " km/s; " + "Std: " + str(np.std(V_starburst)))
    print("sqUW_starburst mean: " + str(np.mean(sqUW_starburst)) + " km/s; " + "Std: " + str(np.std(sqUW_starburst)))

    print("V_others mean: " + str(np.mean(V_others)) + " km/s; " + "Std: " + str(np.std(V_others)))
    print("sqUW_others mean: " + str(np.mean(sqUW_others)) + " km/s; " + "Std: " + str(np.std(sqUW_others)))

    # Plot
    axs[0, i].set_facecolor('k'), axs[1, i].set_facecolor('k'), axs[2, i].set_facecolor('k')
    axs[0, i].scatter(V_old_stars, sqUW_old_stars, s=0.4, alpha=0.6, color='mediumslateblue',
                      label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
    axs[1, i].scatter(V_starburst, sqUW_starburst, s=0.4, alpha=0.8, color='gold',
                      label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
    axs[2, i].scatter(V_others, sqUW_others, s=0.4, alpha=0.4, color='deeppink',
                      label=str(fepochs_limits[2]) + ' - 5.0')
    x_max0, y_max0 = np.abs(axs[0, i].get_xlim()).max(), np.abs(axs[0, i].get_ylim()).max()
    x_max1, y_max1 = np.abs(axs[1, i].get_xlim()).max(), np.abs(axs[1, i].get_ylim()).max()
    x_max2, y_max2 = np.abs(axs[2, i].get_xlim()).max(), np.abs(axs[2, i].get_ylim()).max()
    axs[0, i].set_xlim(xmin=-x_max0, xmax=x_max0), axs[1, i].set_xlim(xmin=-x_max1, xmax=x_max1), axs[2, i].set_xlim(xmin=-x_max2, xmax=x_max2)
    axs[0, i].set_ylim(ymin=0, ymax=y_max0), axs[1, i].set_ylim(ymin=0, ymax=y_max1), axs[2, i].set_ylim(ymin=0, ymax=y_max2)
    axs[0, i].set_title(runs[i])
    axs[2, i].set_xlabel("V [km/s]")

    file_name = file_name + runs[i] + "_"

# so that both subplots have the same limits
axs[0, 0].set_xlim(xmin=-x_max0, xmax=x_max0), axs[1, 0].set_xlim(xmin=-x_max1, xmax=x_max1), axs[2, 0].set_xlim(xmin=-x_max2, xmax=x_max2)
axs[0, 0].set_ylim(ymin=0, ymax=y_max0), axs[1, 0].set_ylim(ymin=0, ymax=y_max1), axs[2, 0].set_ylim(ymin=0, ymax=y_max2)
axs[0, 0].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[1, 0].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[2, 0].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[0, 1].yaxis.set_ticklabels([]), axs[1, 1].yaxis.set_ticklabels([]), axs[2, 1].yaxis.set_ticklabels([])
# lgnd = axs[0, 0].legend(title='Formation epoch [Gyr]', loc='upper left')
# for handle in lgnd.legend_handles:
#     handle.set_sizes([6.0])

# Save figure
plt.savefig(file_name + str(dump_names))
