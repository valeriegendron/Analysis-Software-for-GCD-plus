import numpy as np
import matplotlib.pyplot as plt

# FOR BOUND PARTICLES ONLY


def symmetrize_axi(axes):
    x_max, y_max = np.abs(axes.get_xlim()).max(), np.abs(axes.get_ylim()).max()
    axes.set_xlim(xmin=-x_max, xmax=x_max)
    axes.set_ylim(ymin=-y_max, ymax=y_max)
    axes.hlines(y=0, xmin=-x_max, xmax=x_max, linewidth=0.5, color='k')
    axes.vlines(x=0, ymin=-y_max, ymax=y_max, linewidth=0.5, color='k')


# Input
tides_option = True
paths = ["ascii_output/", "ascii_output/bound_data/"]  # isol, tides
colors = ["#05cad2", "#8c0404"]  # isol, tides
dump_numbers = ["000", "500"]

if tides_option: index = 1
else: index = 0

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Read data
V_tan_ini = np.loadtxt(paths[index] + "detilted/s" + dump_numbers[0] + "r_v", usecols=8)  # initial velocities
V_tan_final = np.loadtxt(paths[index] + "detilted/s" + dump_numbers[1] + "r_v", usecols=8)  # final velocities

ID_ini = np.loadtxt(paths[index] + "s" + dump_numbers[0], usecols=25)  # initial IDs
ID_final = np.loadtxt(paths[index] + "s" + dump_numbers[1], usecols=25)  # final IDs

# Remove star particles that were formed during the simulation
i_to_delete = []  # rows that will be deleted
for i in range(len(ID_final)):  # going through all rows (one row per particle)
    if ID_final[i] not in ID_ini:  # particle to delete
        i_to_delete.append(i)
ID_final_truncated, V_tan_final_truncated = np.delete(ID_final, i_to_delete), np.delete(V_tan_final, i_to_delete)

if len(ID_final_truncated) != len(ID_ini):  # some star particles from t=0 exploded
    j_to_delete = []  # rows that will be deleted
    for j in range(len(ID_ini)):
        if ID_ini[j] not in ID_final_truncated:
            j_to_delete.append(j)
    ID_ini_truncated, V_tan_ini_truncated = np.delete(ID_ini, j_to_delete), np.delete(V_tan_ini, j_to_delete)
else:  # all star particles that were there at t=0 are still there at t=5 Gyr.
    ID_ini_truncated, V_tan_ini_truncated = ID_ini, V_tan_ini

# ID_ini_truncated and ID_final_truncated must be the same (in the same order) so that V_tan_ini_truncated's lines
# refer to the same particles as and V_tan_finale_truncated
ID_final_sorted = sorted(ID_final_truncated, key=ID_ini_truncated.tolist().index)
index_order = list(map(lambda x: ID_final_truncated.tolist().index(x), ID_final_sorted))
V_tan_final_sorted = [V_tan_final_truncated[k] for k in index_order]

# Scatter plot
comparison = ID_final_sorted == ID_ini_truncated
if comparison.all():  # the arrays are the same
    ax.scatter(V_tan_ini_truncated, V_tan_final_sorted, color=colors[index], s=0.2)
    symmetrize_axi(ax)
    ax.set_xlabel("V$_\mathrm{ini}$ [km/s]")
    ax.set_ylabel("V$_\mathrm{final}$ [km/s]")
else:
    raise Exception("The ID lists differ. The scatter plot obtained would be wrong.")

# Count number of points in each quadrant
counter_co, co_co, counter_counter, co_counter = 0, 0, 0, 0
for i in range(len(V_tan_ini_truncated)):
    if (V_tan_ini_truncated[i] < 0) and (V_tan_final_sorted[i] > 0):
        counter_co += 1
    elif (V_tan_ini_truncated[i] > 0) and (V_tan_final_sorted[i] > 0):
        co_co += 1
    elif (V_tan_ini_truncated[i] < 0) and (V_tan_final_sorted[i] < 0):
        counter_counter += 1
    elif (V_tan_ini_truncated[i] > 0) and (V_tan_final_sorted[i] < 0):
        co_counter += 1

ax.text(0, 1, str(counter_co), transform=ax.transAxes, ha='left', va='top')
ax.text(1, 1, str(co_co), transform=ax.transAxes, ha='right', va='top')
ax.text(0, 0, str(counter_counter), transform=ax.transAxes, ha='left', va='bottom')
ax.text(1, 0, str(co_counter), transform=ax.transAxes, ha='right', va='bottom')

# Save figure
plt.savefig("velocity_co-counter_rotation.png")
