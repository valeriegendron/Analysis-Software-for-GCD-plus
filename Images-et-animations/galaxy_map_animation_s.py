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

# Parameters
#galaxy_name = 'Af_v1'
plan = 'yz'  # xy, xz or yz
pic_name = "galaxy_map_" + plan + "_anim_s.mp4"
lim = 10  # max extent of axi in kpc

# 0->x, 1->y, 2->z.
if plan == 'xy':
    columns = (0, 1)
elif plan == 'xz':
    columns = (0, 2)
elif plan == 'yz':
    columns = (1, 2)

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
t = 0.5  # transparency

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
liste_xdata = ['sx']
liste_ydata = ['sy']
frames = []
for index in range(0, len(dumps)):
    print("Reading and animating dump " + str(int(dumps[index])) + " ...")
    for fileName in os.listdir('ascii_output/data_centered'):
        if len(fileName) == 4:  # to make sure it is an output file
            # Stars
            if fileName.startswith("s"):
                if fileName.endswith(str_dumps[index]):
                    sx, sy = np.loadtxt('ascii_output/data_centered/' + fileName, usecols=columns, unpack=True)
            else:
                continue
        else:
            continue


    # Animation
    data_x = sx.tolist()
    data_y = sy.tolist()
    colors = np.array(['y'])
    sizes = np.array([0.2])
    s_cat = [0]*len(sx)
    categories = np.array(s_cat)
    frame = plt.scatter(data_x, data_y, c=colors[categories], alpha=t, s=sizes[categories])

    dump_label = plt.text(x=0.87, y=0.94, ha='center', va='center', transform=ax.transAxes,
                          s="{0:.2f} Gyr".format(time[index]), color='w', bbox=dict(facecolor='k', edgecolor='k'))
    frames.append([frame, dump_label])

# Save animation
print("Saving...")
ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True, repeat=False)
writervideo = animation.FFMpegWriter(fps=5)
ani.save(pic_name, writer=writervideo)
