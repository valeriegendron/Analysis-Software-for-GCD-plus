import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY
dump_name, t = "s500", 5.00  # file name and corresponding time
fepochs_limits = [0.0, 0.2, 1.4]  # in Gyr
tides = True  # True if run with tides. False if isolated run.
if tides:
    path = "ascii_output/bound_data/"
else:
    path = "ascii_output/"
file_name = 'toomre_'

# Setting figure
fig, axs = plt.subplots(1, 1, constrained_layout=True, dpi=500)

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

# Plot
axs.set_facecolor('k')
axs.scatter(V_old_stars, sqUW_old_stars, s=0.4, alpha=0.6, zorder=1, color='mediumslateblue',
               label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
axs.scatter(V_starburst, sqUW_starburst, s=0.4, alpha=0.8, zorder=3, color='gold',
               label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
axs.scatter(V_others, sqUW_others, s=0.4, alpha=0.4, zorder=2, color='deeppink',
               label=str(fepochs_limits[2]) + ' - 5.0')
x_max, y_max = np.abs(axs.get_xlim()).max(), np.abs(axs.get_ylim()).max()
axs.set_xlim(xmin=-x_max, xmax=x_max)
axs.set_ylim(ymin=0, ymax=y_max)
axs.set_title(dump_name)
axs.set_xlabel("V [km/s]")
axs.set_ylabel("$\sqrt{\mathrm{U}^2+\mathrm{W}^2}$ [km/s]")

lgnd = axs.legend(title='Formation epoch [Gyr]', loc='upper left')
for handle in lgnd.legend_handles:
    handle.set_sizes([6.0])

# Save figure
plt.savefig(file_name + dump_name)
