import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

# Input
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_numbers = ["500", "500"]
colors = ["#05cad2", "#8c0404"]
t = [0.6, 0.8]
zorders = [2, 1]
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(runs)):
    # Read data
    V_tan, R = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=(8, 11), unpack=True)

    # Scatter plot
    ax.scatter(R, V_tan, s=0.2, color=colors[i], alpha=t[i], zorder=zorders[i], label=runs[i])

ax.set_xlabel("Radius [kpc]")
ax.set_ylabel("V [km/s]")
ax.legend()
plt.axhline(y=0.0, color='k', linestyle='-')
plt.xlim(0, 40)
fig.tight_layout()

# Save figure
plt.savefig("velocity_profile_scatter_" + runs[0] + "_" + runs[1] + "_" + dump_numbers[0])
