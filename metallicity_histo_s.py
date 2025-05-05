import numpy as np
import matplotlib.pyplot as plt

# Parameters
nbins_Fe_H, nbins_O_H, nbins_O_Fe = [40, 40, 10, 20], [40, 40, 20, 20], [50, 50, 50, 20]
#w_Fe_H, w_O_H, w_O_Fe = [0.05, 0.05, 0.05, 0.05], [0.05, 0.05, 0.05, 0.05], [0.02, 0.02, 0.02, 0.02]  # width of bars in bar plot
binwidths = [0.08699214, 0.08699214, 0.08699214, 0.08699214]  # if we want our comparison to better reflect the data
colors = np.array(["darkgrey", "darkviolet", "deepskyblue", "gold"])
t = [1.0, 1.0, 1.0, 1.0]
labels = ["Old and bound", "New and bound", "Old and ICL", "New and ICL"]
dump_number = 500
dump_name = "s500"
binwidth_option = True  # if True, bin data from binwidth. If False, bin data from nbins.
pic_name = "metallicity_histo_stars_" + dump_name
if binwidth_option:
    pic_name = pic_name + "_binwidth"

# Sun
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses

# Setting figure
fig, axs = plt.subplots(2, 2)

# Read file
m_tot, He, O, Ne, Fe, Z = np.loadtxt("ascii_output/" + dump_name, usecols=(6, 7, 10, 11, 14, 15), unpack=True)

cat, dumps, line = np.loadtxt("stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
cat = [int(i) for i in cat]  # to make sure we have an array of integers
line = [int(i) for i in line]
#cat = np.array(cat)

# To separate the metallicities in the 4 categories of stars, we need to use the file "stars_separated_in_4"
# We only use the information related to the dump number chosen
index_min = np.searchsorted(dumps, dump_number - 0.5)
index_max = np.searchsorted(dumps, dump_number + 0.5)

m_tot_cat, He_cat, O_cat, Ne_cat, Fe_cat, Z_cat = np.take(m_tot, line[index_min:index_max]),\
                                                  np.take(He, line[index_min:index_max]),\
                                                  np.take(O, line[index_min:index_max]),\
                                                  np.take(Ne, line[index_min:index_max]),\
                                                  np.take(Fe, line[index_min:index_max]),\
                                                  np.take(Z, line[index_min:index_max]),
cat_plot = cat[index_min:index_max]
# Count how much elements are in each of the four categories
cat_1, cat_2, cat_3, cat_4 = cat_plot.count(1), cat_plot.count(2), cat_plot.count(3), cat_plot.count(4)

# Computing metallicities
H_cat = m_tot_cat - He_cat - Z_cat  # operation on arrays
Fe_H_cat, O_H_cat, O_Fe_cat, Ne_O_cat = [], [], [], []
for i in range(len(Fe_cat)):
    Fe_H_cat.append(np.log10(Fe_cat[i]/H_cat[i]) - np.log10(Fe_sun/H_sun))  # [Fe/H]
    O_H_cat.append(np.log10(O_cat[i]/H_cat[i]) - np.log10(O_sun/H_sun))  # [O/H]
    O_Fe_cat.append(np.log10(O_cat[i]/Fe_cat[i]) - np.log10(O_sun/Fe_sun))  # [O/Fe]
    # Ne_O_cat.append(np.log10(Ne_cat[i]/O_cat[i]) - np.log10(Ne_sun/O_sun))

# Separate the datasets in the 4 star categories
# Since we read info for a single dump, we'll only have cat_1, cat_2, cat_3, cat_4 (i.e. they won't repeat)
first_indexes = [0, cat_1, cat_1+cat_2, cat_1+cat_2+cat_3]
last_indexes = [cat_1, cat_1+cat_2, cat_1+cat_2+cat_3, cat_1+cat_2+cat_3+cat_4]
if cat_4 == 0:
    first_indexes[3], last_indexes[3] = 0, 0  # we'll have an empty list

# Plotting histograms
# [Fe/H]
hist1_list, bins1_list, bins1_list_minus1 = [], [], []
for i in range(len(first_indexes)):  # plotting a distribution for each category
    data1 = Fe_H_cat[first_indexes[i]:last_indexes[i]]
    if (binwidth_option and len(data1) != 0):
        hist1, bins1 = np.histogram(data1, np.arange(min(data1), max(data1)+binwidths[i], binwidths[i]))
        # if len(data1) == 0: bin_min = 0; bin_max = 0
        # else: bin_min = min(data1); bin_max = max(data1)+binwidth
        # hist1, bins1 = np.histogram(data1, bins=np.arange(bin_min, bin_max, binwidth))
    else:
        hist1, bins1 = np.histogram(data1, bins=nbins_Fe_H[i])
    # axs[0, 0].hist(bins1[:-1], bins1, weights=hist1, log=True, color=colors[i], alpha=t[i], width=w_Fe_H[i],
    #                histtype='step', label=labels[i])
    if len(data1) != 0:  # only plot histogram if there is something to plot
        axs[0, 0].hist(bins1[:-1], bins1, weights=hist1*m_tot[0], log=True, color=colors[i], alpha=t[i], histtype='step')
    # try:
    #     histo(Fe_H_cat[first_indexes[i]:last_indexes[i]], bins='scott', ax=axs[0, 0], histtype='stepfilled',
    #           alpha=t[i], density=True, label=labels[i])
    # except ValueError:
    #     pass
axs[0, 0].grid()

# [O/H]
for i in range(len(first_indexes)):  # plotting a distribution for each category
    data2 = O_H_cat[first_indexes[i]:last_indexes[i]]
    if (binwidth_option and len(data2) != 0):
        hist2, bins2 = np.histogram(data2, bins=np.arange(min(data2), max(data2) + binwidths[i], binwidths[i]))
    else:
        hist2, bins2 = np.histogram(data2, bins=nbins_O_H[i])
    # axs[0, 1].hist(bins2[:-1], bins2, weights=hist2, log=True, color=colors[i], alpha=t[i], width=w_O_H[i],
    #                histtype='step', label=labels[i])
    if len(data2) != 0:  # only plot histogram if there is something to plot
        axs[0, 1].hist(bins2[:-1], bins2, weights=hist2*m_tot[0], log=True, color=colors[i], alpha=t[i], histtype='step')
    # try:
    #     histo(O_H_cat[first_indexes[i]:last_indexes[i]], bins='knutt', ax=axs[0, 1], histtype='stepfilled',
    #           alpha=t[i], log=True, color=colors[i], label=labels[i])
    # except ValueError:
    #     pass
axs[0, 1].grid()

# [O/Fe]
for i in range(len(first_indexes)):  # plotting a distribution for each category
    data3 = O_Fe_cat[first_indexes[i]:last_indexes[i]]
    if (binwidth_option and len(data3) != 0):
        hist3, bins3 = np.histogram(data3, bins=np.arange(min(data3), max(data3) + binwidths[i], binwidths[i]))
    else:
        hist3, bins3 = np.histogram(data3, bins=nbins_O_Fe[i])
    # axs[1, 0].hist(bins3[:-1], bins3, weights=hist3, log=True, color=colors[i], alpha=t[i], width=w_O_Fe[i],
    #                histtype='step', label=labels[i])
    if len(data3) != 0:  # only plot histogram if there is something to plot
        axs[1, 0].hist(bins3[:-1], bins3, weights=hist3*m_tot[0], log=True, color=colors[i], alpha=t[i], histtype='step',
                       label=labels[i])
    # try:
    #     histo(O_Fe_cat[first_indexes[i]:last_indexes[i]], bins='knutt', ax=axs[1, 1], histtype='stepfilled',
    #           alpha=t[i], log=True, color=colors[i], label=labels[i])
    # except ValueError:
    #     pass
axs[1, 0].grid()
axs[1, 1].axis('off')
fig.legend(bbox_to_anchor=(0.91, 0.40))

# Labels
# axs[0, 0].set_ylabel("Number of particles [-]")
# axs[1, 0].set_ylabel("Number of particles [-]")
axs[0, 0].set_ylabel("Mass [M$_\odot$]")
axs[1, 0].set_ylabel("Mass [M$_\odot$]")
axs[0, 0].set_xlabel("[Fe/H]")
axs[0, 1].set_xlabel("[O/H]")
axs[1, 0].set_xlabel("[O/Fe]")
fig.tight_layout()

plt.savefig(pic_name + ".png", dpi=500)
