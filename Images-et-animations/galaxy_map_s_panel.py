import numpy as np
import matplotlib.pyplot as plt

list_dumps = ["s050", "s100", "s150", "s200", "s300", "s400"]  # dumps to read from
dumps_number = [50, 100, 150, 200, 300, 400]

# Setting figure
fig, axs = plt.subplots(2, 3, sharex='col', sharey='row')
pic_name = "galaxy_map_stars_pannel"
colors = np.array(["", "darkgrey", "darkviolet", "deepskyblue", "gold"])
xlim, ylim = 200, 200  # x and y limits of subplots, in kpc

# Read file
cat, dumps, line = np.loadtxt("stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
cat = [int(i) for i in cat]  # to make sure we have an array of integers
line = [int(i) for i in line]
cat = np.array(cat)

for i in range(len(dumps_number)):
    print("Reading and plotting dump " + str(dumps_number[i]) + "...")
    # x_cat1, x_cat2, x_cat3, x_cat4 = [], [], [], []
    # y_cat1, y_cat2, y_cat3, y_cat4 = [], [], [], []
    # x_cat, y_cat = [], []
    x, y = np.loadtxt("ascii_output/data_centered/" + list_dumps[i], usecols=(0, 1), unpack=True)

    index_min = np.searchsorted(dumps, dumps_number[i] - 0.5)
    index_max = np.searchsorted(dumps, dumps_number[i] + 0.5)-1

    # x_cat = x[int(line[index_min]):int(line[index_max])]
    # y_cat = y[int(line[index_min]):int(line[index_max])]
    x_cat = np.take(x, line[index_min:index_max])
    y_cat = np.take(y, line[index_min:index_max])
    cat_plot = cat[index_min:index_max]

    # for j in range(len(dumps)):
    #     if dumps[j] == dumps_number[i]:
    #         x_cat.append(x[line[j]]), y_cat.append(y[line[j]])
    #         # if cat[j] == 1:  # old and bound
    #         #     x_cat1.append(x[line[j]]), y_cat1.append(y[line[j]])
    #         # elif cat[j] == 2:  # new and bound
    #         #     x_cat2.append(x[line[j]]), y_cat2.append(y[line[j]])
    #         # elif cat[j] == 3:  # old and ICL
    #         #     x_cat3.append(x[line[j]]), y_cat3.append(y[line[j]])
    #         # elif cat[j] == 4:  # new and ICL
    #         #     x_cat4.append(x[line[j]]), y_cat4.append(y[line[j]])
    #     elif dumps[j] > dumps_number[i]:
    #         break

    # Plot
    if i < 3:
        axs[0, i].scatter(x_cat, y_cat, s=0.2, c=colors[cat_plot])
        # axs[0, i].scatter(x_cat1, y_cat1, s=0.2, c="darkgrey", label="Old and bound")
        # axs[0, i].scatter(x_cat2, y_cat2, s=0.2, c="darkviolet", label="New and bound")
        # axs[0, i].scatter(x_cat3, y_cat3, s=0.2, c="deepskyblue", label="Old and ICL")
        # axs[0, i].scatter(x_cat4, y_cat4, s=0.2, c="gold", label="New and ICL")

        axs[0, i].set_title(list_dumps[i])  # titles of subfigures
        axs[0, i].set_xlim(-xlim, xlim)
        axs[0, i].set_ylim(-ylim, ylim)
        axs[0, i].set_aspect("equal")

        # axs[0, i].tick_params(axis='x', direction='out', length=0)  # to hide x-axis tick marks for subplots in top row
        # if i != 0:
        #     axs[0, i].tick_params(axis='y', direction='out', length=0)  # to hide y-axis tick marks

    else:
        axs[1, i-3].scatter(x_cat, y_cat, s=0.2, c=colors[cat_plot])
        # axs[1, i-3].scatter(x_cat1, y_cat1, s=0.2, c="darkgrey", label="Old and bound")
        # axs[1, i-3].scatter(x_cat2, y_cat2, s=0.2, c="darkviolet", label="New and bound")
        # axs[1, i-3].scatter(x_cat3, y_cat3, s=0.2, c="deppskyblue", label="Old and ICL")
        # axs[1, i-3].scatter(x_cat4, y_cat4, s=0.2, c="gold", label="New and ICL")

        axs[1, i-3].set_title(list_dumps[i])  # titles of subfigures
        axs[1, i-3].set_xlabel("x [kpc]")
        axs[1, i-3].set_xlim(-xlim, xlim)
        axs[1, i-3].set_ylim(-ylim, ylim)
        axs[1, i-3].set_aspect("equal")

        # if i-3 != 0:
        #     axs[1, i-3].tick_params(axis='y', direction='out', length=0)  # to hide y-axis tick marks

# Set y-label
axs[0, 0].set_ylabel("y [kpc]"), axs[1, 0].set_ylabel("y [kpc]")
#axs.legend()
fig.tight_layout()
plt.savefig(pic_name + ".png")

# s_old_bound_dump, s_new_bound_dump, s_old_ICL_dump, s_new_ICL_dump = [], [], [], []
# s_old_bound_line, s_new_bound_line, s_old_ICL_line, s_new_ICL_line = [], [], [], []
# for i in range(len(cat)):
#     if cat == 1:  # old and bound
#         s_old_bound_dump.append(dump[i]), s_old_bound_line.append(line[i])
#     elif cat == 2:  # new and bound
#         s_new_bound_dump.append(dump[i]), s_new_bound_line.append(line[i])
#     elif cat == 3:  # old and ICL
#         s_old_ICL_dump.append(dump[i]), s_old_ICL_line.append(line[i])
#     elif cat == 4:  # new and ICL
#         s_new_ICL_dump.append(dump[i]), s_new_ICL_line.append(line[i])



