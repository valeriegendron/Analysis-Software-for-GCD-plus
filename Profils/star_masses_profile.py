import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY

# Input
tides_option = True  # True for run with tides. False for isolated run.
r_lim, lim = True, 5  # limit of radius considered, in kpc
dump_number = "500"
nbins = [100, 100]  # for isolated run and run with tides, respectively
colors = ["#05cad2", "#8c0404"]
paths = ["ascii_output/detilted/s", "ascii_output/bound_data/detilted/s"]

if tides_option: index = 1
else: index = 0

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Read data
m, R = np.loadtxt(paths[index] + dump_number + "r_v", usecols=(6, 11), unpack=True)
total_mass = np.sum(m)

# Cutting data
if r_lim:
    index_to_delete = []
    for i in range(len(R)):
        if R[i] > lim:  # over the limit
            index_to_delete.append(i)
    R_cut = np.delete(R, index_to_delete, 0)
    R = R_cut

# Bin radius
count, R_bins = np.histogram(R, bins=nbins[index])

# Computing total stellar mass per radius bin
m_bins, R_plot = [], []
for j in range(len(count)):
    m_bins.append(count[j]*m[0])
    R_plot.append((R_bins[j] + R_bins[j+1])/2)  # get the middle value of each bin (for scatter plot)

# Computing effective radius (assuming it to be the radius inside which 1/2 of the total stellar mass is)
accumulated_mass = []
mass = 0
for k in range(len(count)):
    mass += count[k]*m[0]  # adding the mass of each radius bin
    accumulated_mass.append(mass)
    if mass >= total_mass/2:
        break
# Take last two elements of accumulated_mass and see which one is closest to total_mass/2
if (total_mass/2 - accumulated_mass[-2]) < (accumulated_mass[-1] - total_mass/2):
    # index of accumulated_mass[-2] = k-1; index of accumulated_mass[-1] = k
    r_eff = R_bins[k]  # k-1+1
else:
    r_eff = R_bins[k+1]  # k+1

# Plot histogram
ax.hist(R_bins[:-1], R_bins, weights=m_bins, log=True, color=colors[index], histtype='step')
ymin, ymax = ax.get_ylim()
ax.vlines(r_eff, ymin=0, ymax=ymax, linestyle='dotted', color='#494444')
#ax.scatter(R_plot, m_bins, color=colors[index], s=2)

ax.set_xlabel("Radius [kpc]")
ax.set_ylabel("Stellar mass [M$_\odot$]")
ax.set_ylim(bottom=1e4)
#ax.set_xticklabels([str(r_eff)], minor=True)
fig.tight_layout()

# Save figure
if r_lim:
    plt.savefig("star_mass_profile_" + str(nbins) + "bins_" + dump_number + "_" + str(lim) + "kpc")
else:
    plt.savefig("star_mass_profile_" + str(nbins) + "bins_" + dump_number)
print("r_eff = " + str(r_eff) + ' kpc')
