import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

run = "TIDES8_h_p2_mm"
dump_name, t = "s500", 5.00  # file name and corresponding time
fepochs_limits = [0.0, 0.2, 1.4]  # in Gyr
tides = True  # True if run with tides. False if isolated run.
if tides:
    path = "ascii_output/bound_data/"
else:
    path = "ascii_output/"
file_name = 'toomre_3components_'

# Setting figure
fig, axs = plt.subplots(3, 1, constrained_layout=True, dpi=500, figsize=(5, 11))

# Read data
V, sqUW = np.loadtxt(path + "detilted/" + dump_name + "r_v", usecols=(8, 10), unpack=True)

# Separate stars in categories
age, ID = np.loadtxt(path + dump_name, usecols=(18, 25), unpack=True)
ID_0 = np.loadtxt(path + "s000", usecols=25)

V_old_stars, V_starburst, V_others = [], [], []
sqUW_old_stars, sqUW_starburst, sqUW_others = [], [], []
for line in range(len(ID)):
    if ID[line] in ID_0:  # old star
        V_old_stars.append(V[line]), sqUW_old_stars.append(sqUW[line])
    else:  # stars formed in the simulation
        if fepochs_limits[0] <= (t - age[line]/(10**9)) < fepochs_limits[1]:  # old stars
            V_old_stars.append(V[line]), sqUW_old_stars.append(sqUW[line])
        elif fepochs_limits[1] <= (t - age[line]/(10**9)) <= fepochs_limits[2]:  # starburst stars
            V_starburst.append(V[line]), sqUW_starburst.append(sqUW[line])
        else:  # all other stars
            V_others.append(V[line]), sqUW_others.append(sqUW[line])

# Computing mean and standard deviation
print(run)
print("V_old_stars mean: " + str(np.mean(V_old_stars)) + " km/s; " + "Std: " + str(np.std(V_old_stars)))
print("sqUW_old_stars mean: " + str(np.mean(sqUW_old_stars)) + " km/s; " + "Std: " + str(np.std(sqUW_old_stars)))

print("V_starburst mean: " + str(np.mean(V_starburst)) + " km/s; " + "Std: " + str(np.std(V_starburst)))
print("sqUW_starburst mean: " + str(np.mean(sqUW_starburst)) + " km/s; " + "Std: " + str(np.std(sqUW_starburst)))

print("V_others mean: " + str(np.mean(V_others)) + " km/s; " + "Std: " + str(np.std(V_others)))
print("sqUW_others mean: " + str(np.mean(sqUW_others)) + " km/s; " + "Std: " + str(np.std(sqUW_others)))

# Plot
axs[0].set_facecolor('k'), axs[1].set_facecolor('k'), axs[2].set_facecolor('k')
axs[0].scatter(V_old_stars, sqUW_old_stars, s=0.4, alpha=0.6, color='mediumslateblue',
               label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
axs[1].scatter(V_starburst, sqUW_starburst, s=0.4, alpha=0.8, color='gold',
               label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
axs[2].scatter(V_others, sqUW_others, s=0.4, alpha=0.4, color='deeppink',
               label=str(fepochs_limits[2]) + ' - 5.0')
x_max0, y_max0 = np.abs(axs[0].get_xlim()).max(), np.abs(axs[0].get_ylim()).max()
x_max1, y_max1 = np.abs(axs[1].get_xlim()).max(), np.abs(axs[1].get_ylim()).max()
x_max2, y_max2 = np.abs(axs[2].get_xlim()).max(), np.abs(axs[2].get_ylim()).max()
axs[0].set_xlim(xmin=-x_max0, xmax=x_max0), axs[1].set_xlim(xmin=-x_max1, xmax=x_max1), axs[2].set_xlim(xmin=-x_max2, xmax=x_max2)
axs[0].set_ylim(ymin=0, ymax=y_max0), axs[1].set_ylim(ymin=0, ymax=y_max1), axs[2].set_ylim(ymin=0, ymax=y_max2)
axs[0].set_title(dump_name)
axs[2].set_xlabel("V [km/s]")

axs[0].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[1].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
axs[2].set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")
# lgnd = axs[0, 0].legend(title='Formation epoch [Gyr]', loc='upper left')
# for handle in lgnd.legend_handles:
#     handle.set_sizes([6.0])

# Save figure
plt.savefig(file_name + dump_name)
