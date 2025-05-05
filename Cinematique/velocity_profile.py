import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 15

# FOR BOUND PARTICLES ONLY

# Function to get non-uniform bins with same number of particles within (copied from farenorth on Stack Overflow)
def histedges_equalN(x, nbin):
    npt = len(x)
    return np.interp(np.linspace(0, npt, nbin + 1),
                     np.arange(npt),
                     np.sort(x))


# Input
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_numbers = ["500", "500"]
nbins = [180, 180]  # for isolated run and run with tides, respectively
colors = ["#05cad2", "#8c0404"]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# ADD LOOP ON RUNS
for i in range(len(runs)):
    # Read data
    V_tan, R = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=(8, 11), unpack=True)

    # Bin radius
    #count, R_bins = np.histogram(R, bins=nbins[i])
    count, R_bins = np.histogram(R, histedges_equalN(R, nbins[i]))

    # Computing mean tangential velocity for each radius bin
    V_tan_bins, R_plot = [], []
    for j in range(len(count)):
        V_tan_temp = []  # to compute the mean of each bin
        R_plot.append((R_bins[j] + R_bins[j+1])/2)  # get the middle value of each bin
        for k in range(len(V_tan)):
            if R_bins[j] <= R[k] < R_bins[j+1]:  # particle in radius bin
                V_tan_temp.append(V_tan[k])
        if len(V_tan_temp) != 0: V_tan_bins.append(np.mean(V_tan_temp))
        else: V_tan_bins.append(np.nan)

    # Plot histogram
    #ax.hist(R_bins[:-1], R_bins, weights=V_tan_bins, log=False, color=colors[i], histtype='step', label=runs[i])
    ax.scatter(R_plot, V_tan_bins, color=colors[i], label=runs[i], s=2)

ax.set_xlabel("Radius [kpc]")
ax.set_ylabel("$\overline{V}$ [km/s]")
ax.legend()
fig.tight_layout()

# Save figure
plt.savefig("velocity_profiles_" + runs[0] + "_" + dump_numbers[0] + "_" + runs[1] + "_" + str(nbins) + "bins")
