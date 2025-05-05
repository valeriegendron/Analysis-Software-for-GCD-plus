#AJOUTER TRANSPARENCE
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('Agg')
mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.2  # size of scatter markers

# Choice of plane to graph
plan = 'xy'  # 'xy', 'xz' or 'yz'

# Setting the figure
fig, axs = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(6, 8))

# Input data
dumps = ["000", "010", "020", "030"]

# Initialization of lists that will contain positions in x, y and z
x_stars, x_gas, x_dm = [], [], []
y_stars, y_gas, y_dm = [], [], []
z_stars, z_gas, z_dm = [], [], []

for i in range(len(dumps)):
    # Get correct name of star, gas and dm files
    sfile, gfile, dmfile = "s" + dumps[i], "g" + dumps[i], "d" + dumps[i]

    # Position of star particles
    x_stars, y_stars, z_stars = np.loadtxt(sfile, usecols=(0, 1, 2), unpack=True)
    # Position of gas particles
    x_gas, y_gas, z_gas = np.loadtxt(gfile, usecols=(0, 1, 2), unpack=True)
    # Position of dm particles
    x_dm, y_dm, z_dm = np.loadtxt(dmfile, usecols=(0, 1, 2), unpack=True)

    sfa, ssa, gfa, gsa, dfa, dsa = [], [], [], [], [], []  # first letter: s=star, g=gas, d=dm. Last two: fa=first axis, sa=second axis
    if plan == 'xy':
        sfa, ssa, gfa, gsa, dfa, dsa = x_stars, y_stars, x_gas, y_gas, x_dm, y_dm
    elif plan == 'xz':
        sfa, ssa, gfa, gsa, dfa, dsa = x_stars, z_stars, x_gas, z_gas, x_dm, z_dm
    elif plan == 'yz':
        sfa, ssa, gfa, gsa, dfa, dsa = y_stars, z_stars, y_gas, z_gas, y_dm, z_dm

    j, k = 0, 0
    if i == 1:
        j, k = 0, 1
    elif i == 2:
        j, k = 1, 0
    elif i == 3:
        j, k = 1, 1

    # Graphing in subplots for dump i
    axs[j, k].scatter(dfa, dsa, color='k', label='Dm particles', alpha=0.2)
    axs[j, k].scatter(gfa, gsa, color='tab:red', label='Gas particles', alpha=0.2)
    axs[j, k].scatter(sfa, ssa, color=(1, 0.9, 0), label='Star particles', alpha=0.2)

    axs[j, k].set_title('Dump ' + dumps[i])
    axs[j, k].set_xlabel('Position in ' + plan[0] + ' [kpc]')
    axs[j, k].set_ylabel('Position in ' + plan[1] + ' [kpc]')
    axs[j, k].set_aspect(1)

#lgnd = axs[0, 1].legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
lgnd = axs[0, 1].legend(fontsize=8)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]
lgnd.legendHandles[2]._sizes = [30]

# save the figure to a png file
pic_name = 'galaxy_map_pannel' + plan
plt.savefig(pic_name, dpi=500)
