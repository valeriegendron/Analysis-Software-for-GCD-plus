import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Input
run = "TIDES8_h_p2_mm"
dumps_str = ["000", "023", "027", "034", "040", "045", "057", "063", "074", "080", "100", "120", "140", "200",
                "240", "300", "400", "500"]
times = [0.00, 0.23, 0.27, 0.34, 0.40, 0.45, 0.57, 0.63, 0.74, 0.80, 1.00, 1.20, 1.40, 2.00, 2.40, 3.00, 4.00, 5.00]
fepochs_limits = [0.0, 0.2, 1.4]  # in Gyr
path = "/diskev/ascii_output/bound_data/"
colors = ["#242363", "#ec3c34", "#fab052"]

# Read data
old_stars_plot, starburst_plot, others_plot, total_stars_plot = [], [], [], []
for i in range(len(dumps_str)):
    m, V_tan = np.loadtxt(run + path + "detilted/s" + dumps_str[i] + "r_v", usecols=(6, 8), unpack=True)
    age, ID = np.loadtxt(run + path + "s" + dumps_str[i], usecols=(18, 25), unpack=True)
    ID_0 = np.loadtxt(run + path + "s000", usecols=25)
    counter_count, counter_mass = 0, 0

    m_old_stars, m_starburst, m_others = [], [], []
    V_old_stars, V_starburst, V_others = [], [], []
    for line in range(len(ID)):
        if ID[line] in ID_0:  # old star
            m_old_stars.append(m[line]), V_old_stars.append(V_tan[line])
        else:  # stars formed in the simulation
            if fepochs_limits[0] <= (times[i] - age[line] / (10 ** 9)) < fepochs_limits[1]:  # old stars
                m_old_stars.append(m[line]), V_old_stars.append(V_tan[line])
            elif fepochs_limits[1] <= (times[i] - age[line] / (10 ** 9)) < fepochs_limits[2]:  # starburst stars
                m_starburst.append(m[line]), V_starburst.append(V_tan[line])
            else:  # all other stars
                m_others.append(m[line]), V_others.append(V_tan[line])

    # Lists of indexes of counter rotating stars
    old_star_counter, starburst_counter, others_counter =\
        tuple([index for (index, item) in enumerate(V_old_stars) if item < 0]),\
        tuple([index for (index, item) in enumerate(V_starburst) if item < 0]),\
        tuple([index for (index, item) in enumerate(V_others) if item < 0])

    m_old_stars_counter, m_starburst_counter, m_others_counter = [m_old_stars[k] for k in old_star_counter],\
                                                                 [m_starburst[k] for k in starburst_counter],\
                                                                 [m_others[k] for k in others_counter]

    # Add mass count to lists for plot
    old_stars_plot.append(sum(m_old_stars_counter))
    starburst_plot.append(sum(m_starburst_counter))
    others_plot.append(sum(m_others_counter))
    total_stars_plot.append(sum(m_old_stars_counter)+sum(m_starburst_counter)+sum(m_others_counter))


# Plot
ax.scatter(times, old_stars_plot, color=colors[0], label=str(fepochs_limits[0]) + ' - ' + str(fepochs_limits[1]))
ax.scatter(times, starburst_plot, color=colors[1], label=str(fepochs_limits[1]) + ' - ' + str(fepochs_limits[2]))
ax.scatter(times, others_plot, color=colors[2], label=str(fepochs_limits[2]) + ' - 5.0')
ax.scatter(times, total_stars_plot, color="grey")

ax.set_xlabel("Time [Gyr]"), ax.set_ylabel("Stellar mass [M$_\odot$]")
lgnd = ax.legend(title='Formation epoch [Gyr]', loc='upper left')

# Save figure
plt.savefig("remnant_counter_velocity/velocity_counter_dist-" + run)
