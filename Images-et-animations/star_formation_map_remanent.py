import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec


# FOR BOUND PARTICLES ONLY

# Input data
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
nbins = [40, 40]  # for isolated run and run with tides, respectively
w = 0.1
dump_names = ["s500", "s500"]
dump_numbers = [500, 500]
xlim, ylim = 10, 10  # limits of both axi (in kpc)
rlim = 4  # limit of radius considered for histogram
colors = ["#05cad2", "#8c0404"]  # for histogram (isol, tides)
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
    ID = np.loadtxt(runs[i] + paths[i] + dump_names[i], usecols=25)
    ID_0 = np.loadtxt(runs[i] + paths[i] + "s000", usecols=25)
    x, y, m = np.loadtxt(runs[i] + paths[i] + "/detilted/" + dump_names[i] + "r", usecols=(0, 1, 6), unpack=True)  # detilted file
    R = np.loadtxt(runs[i] + paths[i] + "/detilted/" + dump_names[i] + "r_v", usecols=11)

    old_stars_x, old_stars_y, new_stars_x, new_stars_y = [], [], [], []
    new_stars_m, new_stars_R = [], []
    for line in range(len(ID)):
        if ID[line] in ID_0:  # old star
            old_stars_x.append(x[line]), old_stars_y.append(y[line])
        else:  # new star
            new_stars_x.append(x[line]), new_stars_y.append(y[line])
            new_stars_m.append(m[line]), new_stars_R.append(R[line])

    # Plot
    # Maps
    axs[i].scatter(old_stars_x, old_stars_y, color="darkgrey", alpha=0.6, s=0.5, label="Old stars")
    axs[i].scatter(new_stars_x, new_stars_y, color="deeppink", alpha=0.8, s=0.5, label="New stars")
    axs[i].set_xlim([-xlim, xlim])
    axs[i].set_ylim([-ylim, ylim])

    axs[i].set_xlabel("x [kpc]")
    axs[i].set_aspect("equal")
    axs[i].set_title(runs[i])

    # Histogram
    new_stars_R_cut, new_stars_m_cut = [], []
    for data in range(len(new_stars_R)):
        if new_stars_R[data] <= rlim:
            new_stars_R_cut.append(new_stars_R[data]), new_stars_m_cut.append(new_stars_m[data])
    histo = sns.histplot(ax=axs[2], x=new_stars_R_cut, weights=new_stars_m_cut,
                         bins=len(np.arange(min(new_stars_R_cut), max(new_stars_R_cut) + w, w)),
                         kde=True, color=colors[i], element="step", fill=False, label=runs[i])
    #axs[2].set_xscale("log")

axs[0].set_ylabel("y [kpc]")
axs[2].set_ylabel("Stellar mass [M$_\odot$]")
axs[2].set_xlabel("Radius [kpc]")
lgnd = axs[0].legend()
axs[2].legend(scatterpoints=1)
axs[2].set_xlim([0, 4])
axs[1].yaxis.set_ticklabels([])
for handle in lgnd.legend_handles:
    handle.set_sizes([6.0])
# Save figure
plt.savefig("star_formation_map_" + runs[0] + "_" + runs[1] + "_" + str(nbins) + "bins_" + str(dump_numbers))
