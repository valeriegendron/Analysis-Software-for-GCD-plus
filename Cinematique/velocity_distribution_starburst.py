import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# FOR BOUND PARTICLES ONLY
plt.rcParams['font.size'] = 15

# Input
tides_option = True  # if True, reading files of a run with tides. If False, reading files of isolated run.
run = "TIDES8_h_p2_mm"
fepochs_limits = [0.0, 0.2, 1.4]  # in Gyr
dump_numbers = ["080", "100", "120", "140", "200", "500"]
times = [0.80, 1.00, 1.20, 1.40, 2.00, 5.00]  # times corresponding to dump numbers (should be automated instead!)
nbins = [60, 60, 60, 60, 60, 60]
colors = ["#242363", "#ec3c34", "#fab052"]  # Old stars, starburst, others
zorder = [1, 3, 2]  # Old stars, starburst, others
paths = ["/diskev/ascii_output/", "/diskev/ascii_output/bound_data/"]  # isol, tides

# Setting figure
fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, constrained_layout=True, figsize=(11, 7))
axes = [axs[0, 0], axs[0, 1], axs[0, 2], axs[1, 0], axs[1, 1], axs[1, 2]]

for i in range(len(dump_numbers)):
    # Read data
    if tides_option: index = 1
    else: index = 0

    m, V_tan = np.loadtxt(run + paths[index] + "detilted/s" + dump_numbers[i] + "r_v", usecols=(6, 8), unpack=True)

    # Separate stars in categories
    age, ID = np.loadtxt(run + paths[index] + "s" + dump_numbers[i], usecols=(18, 25), unpack=True)
    ID_0 = np.loadtxt(run + paths[index] + "s000", usecols=25)

    V_old_stars, V_starburst, V_others = [], [], []
    m_old_stars, m_starburst, m_others = [], [], []
    for line in range(len(ID)):
        if ID[line] in ID_0:  # old star
            V_old_stars.append(V_tan[line]), m_old_stars.append(m[line])
        else:  # stars formed in the simulation
            if fepochs_limits[0] <= (times[i] - age[line] / (10 ** 9)) < fepochs_limits[1]:  # old stars
                V_old_stars.append(V_tan[line]), m_old_stars.append(m[line])
            elif fepochs_limits[1] <= (times[i] - age[line] / (10 ** 9)) <= fepochs_limits[2]:  # starburst stars
                V_starburst.append(V_tan[line]), m_starburst.append(m[line])
            else:  # all other stars
                V_others.append(V_tan[line]), m_others.append(m[line])

    # Make histogram
    plt.sca(axes[i])
    sns.histplot(x=V_tan, weights=m, kde=False, color='#c5c5c5', element="step", fill=True, line_kws={"linestyle":"dashed"})
    sns.histplot(x=V_old_stars, weights=m_old_stars, bins=nbins[i], kde=False, color=colors[0], element="step", fill=False,
                 zorder=zorder[0], label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
    if len(V_starburst) != 0:
        sns.histplot(x=V_starburst, weights=m_starburst, bins=nbins[i], kde=False, color=colors[1], element="step", fill=False,
                     zorder=zorder[1], label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
    if len(V_others) != 0:
        sns.histplot(x=V_others, weights=m_others, bins=nbins[i], kde=False, color=colors[2], element="step", fill=False,
                     zorder=zorder[2], label=str(fepochs_limits[2]) + ' - 5.0')
    axes[i].set_title("t = " + str(times[i]) + " Gyr")

# Set labels
for ax in axs.flat:
    ax.set(xlabel="V [km/s]", ylabel="Stellar mass [M$_\odot$]")
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

lgnd = axs[1, 2].legend(title='Formation epoch [Gyr]', loc='upper left', fontsize=12)
# for handle in lgnd.legend_handles:
#     handle.set_sizes([6.0])

# Save figure
plt.savefig(run + "/diskev/velocity_dist_starburst_" + str(nbins) + "bins")
