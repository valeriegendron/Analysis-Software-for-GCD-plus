import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec

plt.rcParams['font.size'] = 15

# FOR BOUND PARTICLES ONLY

def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))


def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]

# Input data
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
nbins = [40, 40]  # for isolated run and run with tides, respectively
fepochs_limits = [0.00, 0.20, 1.40]  # in Gyr
w = 0.1
dump_names = ["s500", "s500"]
dump_numbers = [500, 500]
xlim, ylim = 10, 10  # limits of both axi (in kpc)
rlim = 4  # limit of radius considered for histogram
#colors = ["#05cad2", "#8c0404"]  # for histogram (isol, tides)
colors = ["#242363", "#ec3c34"]  # for histogram (isol, tides)
paths = ["/diskev/ascii_output/", "/diskev/ascii_output/bound_data/"]
# paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]

# Set figure
gs = gridspec.GridSpec(2, 2)
fig = plt.figure(constrained_layout=True, figsize=(8, 8), dpi=500)
ax1 = fig.add_subplot(gs[0, 0])  # map ISOL
ax2 = fig.add_subplot(gs[0, 1])  # map TIDES
ax3 = fig.add_subplot(gs[1, :])  # histogram
axs = [ax1, ax2, ax3]

# Read data
for i in range(len(runs)):
    age, ID = np.loadtxt(runs[i] + paths[i] + dump_names[i], usecols=(18, 25), unpack=True)
    ID_0 = np.loadtxt(runs[i] + paths[i] + "s000", usecols=25)
    x, y, m = np.loadtxt(runs[i] + paths[i] + "detilted/" + dump_names[i] + "r", usecols=(0, 1, 6), unpack=True)  # detilted file
    R = np.loadtxt(runs[i] + paths[i] + "detilted/" + dump_names[i] + "r_v", usecols=11)

    x_old_stars, x_starburst, x_others = [], [], []
    y_old_stars, y_starburst, y_others = [], [], []
    m_starburst, R_starburst = [], []
    for line in range(len(ID)):
        if ID[line] in ID_0:  # old star
            x_old_stars.append(x[line]), y_old_stars.append(y[line])
        else:  # stars formed in the simulation
            if fepochs_limits[0] <= (dump_numbers[i]*0.01 - age[line] / (10 ** 9)) < fepochs_limits[1]:  # old stars
                x_old_stars.append(x[line]), y_old_stars.append(y[line])
            elif fepochs_limits[1] <= (dump_numbers[i]*0.01 - age[line] / (10 ** 9)) < fepochs_limits[2]:  # starburst stars
                x_starburst.append(x[line]), y_starburst.append(y[line]), m_starburst.append(m[line]), R_starburst.append(R[line])
            else:  # all other stars
                x_others.append(x[line]), y_others.append(y[line])

    # Plot
    # Maps
    axs[i].scatter(x_old_stars, y_old_stars, color="darkgrey", alpha=0.6, s=0.5, zorder=1,
                   label="FE: " + str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
    axs[i].scatter(x_starburst, y_starburst, color="#ec3c34", alpha=0.8, s=0.5, zorder=3,
                   label="FE: " + str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))  # (color was "deeppink")
    axs[i].scatter(x_others, y_others, color="#fab052", alpha=0.6, s=0.5, zorder=2,
                   label="FE: " + str(fepochs_limits[2]) + ' - 5.0')  # (color was "lightcoral" before)
    axs[i].set_xlim([-xlim, xlim])
    axs[i].set_ylim([-ylim, ylim])

    axs[i].set_xlabel("x [kpc]")
    axs[i].set_aspect("equal")
    axs[i].set_title(runs[i])

    # Histogram
    R_starburst_cut, m_starburst_cut = [], []
    for data in range(len(R_starburst)):
        if R_starburst[data] <= rlim:
            R_starburst_cut.append(R_starburst[data]), m_starburst_cut.append(m_starburst[data])
    if len(R_starburst_cut) != 0:
        histo = sns.histplot(ax=axs[2], x=R_starburst_cut, weights=m_starburst_cut,
                             bins=len(np.arange(min(R_starburst_cut), max(R_starburst_cut) + w, w)),
                             kde=False, color=colors[i], element="step", fill=False, label=runs[i])
    if i == 45:  # i==1, run with tides ("i==45" to not go through)
        kde_data = axs[2].lines[3].get_xydata()
        max_xy = kde_data[np.where(kde_data[:, 1] == max(kde_data[:, 1]))]
        print("Radius: " + str(max_xy[0, 0]) + " kpc", "Stellar mass: " + str(max_xy[0, 1]) + " M_sun")

        # find the two crossing points
        hmx = half_max_x(kde_data[:, 0], kde_data[:, 1])

        # print the answer
        fwhm = hmx[1] - hmx[0]
        print("FWHM: " + fwhm + " kpc")
        print("Central region: " + hmx[1] + " kpc")

    #axs[2].set_xscale("log")

axs[0].set_ylabel("y [kpc]")
axs[2].set_ylabel("Stellar mass [M$_\odot$]")
axs[2].set_xlabel("Radius [kpc]")
lgnd = axs[0].legend(fontsize=12)
axs[2].legend(scatterpoints=1)
axs[2].set_xlim([0, 4])
axs[1].yaxis.set_ticklabels([])
for handle in lgnd.legend_handles:
    handle.set_sizes([10.0])
# Save figure
plt.savefig("remnant_star_formation_maps/star_formation_starburst_map_" + runs[0] + "_" + str(dump_numbers[0]) + "_" + runs[1])
