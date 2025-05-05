print('Importing')
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rcParams['animation.ffmpeg_path'] = r'/home/vgendron/scratch/ffmpeg/ffmpeg'
mpl.rcParams['lines.markersize'] = 0.2  # size of scatter markers
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ffmpeg
import os
from get_time import get_time
from separate_stars import separate_stars

# Parameters
plan = 'xy'  # xy, xz or yz
pic_name = "galaxy_map_" + plan + "_anim_v3_"
icl_stars_file = 'unbound_stars_data_v3-3'
icl_gas_file = 'unbound_gas_data_v3-3'
lim = 10  # max extent of axi in kpc

# 0->x, 1->y, 2->z, 25->ID.
if plan == 'xy':
    columns = (0, 1, 25)
elif plan == 'xz':
    columns = (0, 2, 25)
elif plan == 'yz':
    columns = (1, 2, 25)

# Figure setting
plt.style.use('dark_background')
fig = plt.figure()
ax = fig.add_subplot(111)
plt.gca().set_aspect(1)
# plt.title("Run " + str(galaxy_name) + " evolution")
plt.xlabel('Position in ' + plan[0] + ' [kpc]')
plt.ylabel('Position in ' + plan[1] + ' [kpc]')
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# User input
choice = input("Press (1) to get stars formed during the interaction or (2) to get intracluster stars: ")
while choice != '1' and choice != '2':
    choice = input("Wrong key. Press (1) to get stars formed during the interaction or (2) to get intracluster stars: ")

print("Reading")
# Lists containing dump number and corresponding time
dumps = np.linspace(0, 500, num=501)
dt = get_time("ini/input.dat")[0]  # getting time interval between dumps using 'get_time' function and 'input.dat' file
time = []
for dump in dumps:
    time.append(round(dt*dump, 2))

str_dumps = []  # list containing dumps number in string format "xxx"
for i in range(0, len(dumps)):
    if len(str(int(dumps[i]))) == 1:
        str_dumps.append("00"+str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 2:
        str_dumps.append("0"+str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 3:
        str_dumps.append(str(int(dumps[i])))

# Initialization for data reading
liste_xdata = ['sx', 'gx']
liste_ydata = ['sy', 'gy']
frames = []
for index in range(0, len(dumps)):
    print("Reading and animating dump " + str(int(dumps[index])) + " ...")
    for fileName in os.listdir('ascii_output/data_centered/'):
        if len(fileName) == 4:  # to make sure it is an output file
            # Stars
            if fileName.startswith("s"):
                if fileName.endswith(str_dumps[index]):
                    sx, sy, ID = np.loadtxt('ascii_output/data_centered/' + fileName, usecols=columns, unpack=True)
            # Gas
            if fileName.startswith("g"):
                if fileName.endswith(str_dumps[index]):
                    gx, gy, g_ID = np.loadtxt('ascii_output/data_centered/' + fileName, usecols=columns, unpack=True)
            else:
                continue
        else:
            continue


    # Animation
    sx1, sy1, sx2, sy2 = separate_stars(icl_stars_file, 'ascii_output/s000', str_dumps[index], sx, sy, ID, plan, choice)
    gx1, gy1, gx2, gy2 = separate_stars(icl_gas_file, 'ascii_output/g000', str_dumps[index], gx, gy, g_ID, plan, choice)
    data_x = list(sx1) + list(sx2) + list(gx1) + list(gx2)  # sx1 and sy1 are coordinates of either stars that were already formed before the start of the simulation or bound stars
    data_y = list(sy1) + list(sy2) + list(gy1) + list(gy2)  # sx2 and sy2 are coordinates of either stars formed with the the interaction or intracluster stars
    colors = np.array(['deeppink', 'y', 'darkmagenta', 'orange'])
    sizes = np.array([0.2, 0.2, 0.2, 0.2])
    t = np.array([0.2, 1.0, 0.2, 1.0])  # transparency
    cat1, cat2, cat3, cat4 = [0]*len(sx1), [1]*len(sx2), [2]*len(gx1), [3]*len(gx2)
    categories = np.array(cat1 + cat2 + cat3 + cat4)
    frame = plt.scatter(data_x, data_y, c=colors[categories], alpha=t[categories], s=sizes[categories])

    dump_label = plt.text(x=0.87, y=0.94, ha='center', va='center', transform=ax.transAxes,
                          s="{0:.2f} Gyr".format(time[index]), color='w', bbox=dict(facecolor='k', edgecolor='k'))
    frames.append([frame, dump_label])

# Save animation
print("Saving...")
if choice == '1':
    pic_name += 'new_stars.mp4'
elif choice == '2':
    pic_name += 'ICL_g-s.mp4'
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps=5)
ani.save(pic_name, writer=writervideo)
