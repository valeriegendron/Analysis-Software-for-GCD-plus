import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from separate_stars import separate_stars

mpl.use('Agg')
mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.2  # size of scatter markers

# Choice of plane to graph
plan = 'xy'  # 'xy', 'xz' or 'yz'
# 0->x, 1->y, 2->z, 25->ID.
if plan == 'xy':
    columns = (0, 1, 25)
elif plan == 'xz':
    columns = (0, 2, 25)
elif plan == 'yz':
    columns = (1, 2, 25)

# Input data
dump_number = 500
dump_name = "500"
lim = 70  # limit in kpc

# User input
choice = input("Press (1) to get stars formed during the interaction or (2) to get intracluster stars: ")
while choice != '1' and choice != '2':
    choice = input("Wrong key. Press (1) to get stars formed during the interaction or (2) to get intracluster stars: ")

# Setting the figure
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Position of star particles
x_stars, y_stars, ID = np.loadtxt('ascii_output/data_centered/s' + dump_name, usecols=columns, unpack=True)
sx1, sy1, sx2, sy2 = separate_stars('unbound_stars_data_v3-3', 'ascii_output/s000', dump_name, x_stars, y_stars, ID,
                                    plan, choice)

# Plot
ax.scatter(sx1, sy1, color='deeppink', alpha=0.8)  # bound stars (or old stars, if choice=1)
ax.scatter(sx2, sy2, color=(1, 0.9, 0), alpha=0.8)  # ICL stars (or new stars, if choice=1)
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)

ax.grid(which='major')
ax.grid(which='minor')
ax.set_xlabel('Position in ' + plan[0] + ' [kpc]')
ax.set_ylabel('Position in ' + plan[1] + ' [kpc]')
ax.set_aspect(1)
ax.minorticks_on()

# Save the figure to a png file
pic_name = 'galaxy_map_' + plan + '_' + dump_name + "_ICL"
plt.savefig(pic_name, dpi=500)
