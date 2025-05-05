import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# FOR BOUND PARTICLES ONLY

plt.rcParams['font.size'] = 15

# Input
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_numbers = ["500", "500"]
nbins = [60, 60]  # for isolated run and run with tides, respectively
colors = ["#05cad2", "#8c0404"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(runs)):
    # Read data
    m, V_tan = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=(6, 8), unpack=True)

    # Make histogram
    sns.histplot(x=V_tan, weights=m, bins=nbins[i], kde=False, color=colors[i], element="step", fill=False, label=runs[i])

plt.ylabel("Stellar mass [M$_\odot$]")
plt.xlabel("V [km/s]")
plt.legend()

# Save figure
plt.savefig("velocity_dist_" + runs[0] + "_" + runs[1] + "_" + str(nbins) + "bins_" + dump_numbers[0])
