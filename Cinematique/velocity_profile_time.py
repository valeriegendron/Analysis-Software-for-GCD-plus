import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY


# Function to get non-uniform bins with same number of particles within (copied from farenorth on Stack Overflow)
def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))


# Input
run = "ISOL_A"
tides_option = False  # if True, reading files of a run with tides. If False, reading files of isolated run.
dump_numbers = ["000", "100", "200", "300", "400", "500"]
times = ["0.0", "1.0", "2.0", "3.0", "4.0", "5.0"]  # times corresponding to dump numbers (should be automated instead!)
markers = ["o", "1", "<", "x", "s", "+"]
sizes = [5, 10, 5, 10, 5, 10]
nbins = [200, 200, 200, 200, 200, 200]
colors_isol = ["#5c3a92", "#8a64d6", "#b1a5eb", "#729efd", "#3acadf", "#05cad2"]
colors_tides = ["#ffc100", "#ff9a00", "#ff7400", "#ff4d00", "#c70000", "#8c0404"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]  # isol, tides

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(dump_numbers)):
    if tides_option: index = 1; colors = colors_tides
    else: index = 0; colors = colors_isol
    # Read data
    V_tan, R = np.loadtxt(run + paths[index] + dump_numbers[i] + "r_v", usecols=(8, 11), unpack=True)

    # Bin radius
    # count, R_bins = np.histogram(R, bins=nbins[i])
    count, R_bins = np.histogram(R, histedges_equalN(R, nbins[i]))

    # Computing mean tangential velocity for each radius bin
    V_tan_bins, R_plot = [], []
    for j in range(len(count)):
        V_tan_temp = []  # to compute the mean of each bin
        R_plot.append((R_bins[j] + R_bins[j + 1]) / 2)  # get the middle value of each bin
        for k in range(len(V_tan)):
            if R_bins[j] <= R[k] < R_bins[j + 1]:  # particle in radius bin
                V_tan_temp.append(V_tan[k])
        if len(V_tan_temp) != 0:
            V_tan_bins.append(np.mean(V_tan_temp))
        else:
            V_tan_bins.append(np.nan)

    # Plot histogram
    # ax.hist(R_bins[:-1], R_bins, weights=V_tan_bins, log=False, color=colors[i], histtype='step', label=times[i])
    ax.scatter(R_plot, V_tan_bins, color=colors[i], marker=markers[i], linewidth=1, label=times[i] + " Gyr", s=sizes[i])

ax.set_xlabel("Radius [kpc]")
ax.set_ylabel("$\overline{V}$ [km/s]")
ax.legend()
fig.tight_layout()

# Save figure
plt.savefig("velocity_profiles_time_" + run + "_" + str(nbins) + "bins", dpi=500)
