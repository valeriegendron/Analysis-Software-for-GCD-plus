import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

# Input
dump_number = "500"
colors = ["#05cad2", "#8c0404"]
tides_option = True  # if True, applied to a run with tides. If False, applied to an isolated run (changes the path).
if tides_option: path = "ascii_output/bound_data/detilted/s"; color=colors[1]
else: path = "ascii_output/detilted/s"; color=colors[0]

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Read data
V_tan, R = np.loadtxt(path + dump_number + "r_v", usecols=(8, 11), unpack=True)

# Scatter plot
ax.scatter(R, V_tan, s=0.2, color=color, alpha=0.8)
ax.set_xlabel("Radius [kpc]")
ax.set_ylabel("V [km/s]")
plt.axhline(y=0.0, color='k', linestyle='-')
fig.tight_layout()

# Save figure
plt.savefig("velocity_profile_scatter_" + dump_number)
