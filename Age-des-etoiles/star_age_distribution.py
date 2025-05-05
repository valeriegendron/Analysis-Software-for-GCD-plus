import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
from get_time import get_time

nbins = 20
w = 0.01  # width of bars in bar plot

smass_list, age_list = [], []  # will contain all star particles' respective mass and age, for all dumps
for fileName in sorted(os.listdir("ascii_output")):  # to run through all dumps
    if len(fileName) == 4:  # output file
        if fileName.startswith("s"):  # star file
            if fileName.endswith("000"):  # dump 000
                smass_list.append(0)
                age_list.append(0)
            else:
                print("Reading file " + fileName)
                m, age = np.loadtxt("ascii_output/data_centered/" + fileName, usecols=(6, 18), unpack=True)
                # Add to lists
                for i in range(len(m)):
                    smass_list.append(m[i])
                    age_list.append(age[i]/(10**9))  # age in Gyr

del smass_list[0]
del age_list[0]
# Age distribution
hist, bins = np.histogram(age_list, bins=nbins)
for i in range(len(hist)):
    hist[i] = hist[i]*smass_list[0]  # all of smass' elements are the same

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.set_xlim(left=0.00, right=time)
ax.bar(bins[:-1], hist, color='blue', alpha=0.6, width=w)
ax.set_ylabel('Mass of stars [M$_\odot$]')
ax.set_xlabel('Age [Gyr]')
#ax.set_title('Age distribution of star particles of run ' + str(galaxy_name) + ' at ' + str(time) + ' Gyr')
ax.grid()
fig.tight_layout()
# plt.show()
plt.savefig("star_age_distribution.png")
