import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# FOR BOUND PARTICLES ONLY

# Input
run = "TIDES8_h_p2_mm"
tides_option = True  # if True, reading files of a run with tides. If False, reading files of isolated run.
dump_numbers = ["000", "100", "200", "300", "400", "500"]
times = ["0.0", "1.0", "2.0", "3.0", "4.0", "5.0"]  # times corresponding to dump numbers (should be automated instead!)
nbins = [60, 60, 60, 60, 60, 60]
colors_isol = ["#5c3a92", "#8a64d6", "#b1a5eb", "#729efd", "#3acadf", "#05cad2"]
colors_tides = ["#ffc100", "#ff9a00", "#ff7400", "#ff4d00", "#c70000", "#8c0404"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]  # isol, tides

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(dump_numbers)):
    # Read data
    if tides_option: index = 1; colors = colors_tides
    else: index = 0; colors = colors_isol

    m, V_tan = np.loadtxt(run + paths[index] + dump_numbers[i] + "r_v", usecols=(6, 8), unpack=True)

    # Make histogram
    sns.histplot(x=V_tan, weights=m, bins=nbins[i], kde=True, color=colors[i], element="step", fill=False, label=times[i] + " Gyr")

plt.ylabel("Stellar mass [M$_\odot$]")
plt.xlabel("V [km/s]")
plt.legend()

# Save figure
plt.savefig("velocity_dist_time_" + run + "_" + str(nbins) + "bins")
