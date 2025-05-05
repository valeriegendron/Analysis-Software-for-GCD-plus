import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('Agg')
mpl.rcParams.update({'font.size': 8})
mpl.rcParams['lines.markersize'] = 0.9  # size of scatter markers

# Input data
plan = 'xy'  # 'xy', 'xz' or 'yz', choice of plane to graph
dump_number = '000'  # format: xxx, in string
xlim, ylim = 75, 75  # x and y limits of subplots, in kpc
light_theme = True  # True for light theme, False for dark theme

if not light_theme:
    plt.style.use('dark_background')
    dcolor = 'lightgray'  # color of dark matter particles for scatter plot
else:
    dcolor = 'k'

# Setting the figure
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Get correct name of star, gas and dm files
sfile, gfile, dmfile = "s" + dump_number, "g" + dump_number, "d" + dump_number

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

# Plot
ax.scatter(dfa, dsa, color=dcolor, marker='o', label='Dm particles', alpha=0.5)
ax.scatter(gfa, gsa, color='tab:red', marker='o', label='Gas particles', alpha=0.9)
ax.scatter(sfa, ssa, color=(1, 0.9, 0), marker='o', label='Star particles', alpha=0.2)

ax.set_xlim(-xlim, xlim)
ax.set_ylim(-ylim, ylim)

ax.set_xlabel('Position in ' + plan[0] + ' [kpc]')
ax.set_ylabel('Position in ' + plan[1] + ' [kpc]')
ax.set_aspect(1)

#lgnd = axs[0, 1].legend(fontsize=8, frameon=True, loc=(1.05, 0.20))
lgnd = ax.legend(fontsize=8)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]
lgnd.legendHandles[2]._sizes = [30]

# save the figure to a png file
pic_name = 'galaxy_map_' + plan + '_' + dump_number + '_' + str(xlim) + 'kpc'
if not light_theme:
    pic_name += '_dark'
plt.savefig(pic_name, dpi=500)
