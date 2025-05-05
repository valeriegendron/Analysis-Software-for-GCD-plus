# Must run 'cm_recenter_stars.py' beforehand
import numpy as np
import os

t = 0  # will be used as index to keep track of dump number
for fileName in sorted(os.listdir("ascii_output")):
    if fileName.startswith("d"):  # DM file
        if len(fileName) == 4:  # to make sure it is an output file
            print("Centering particles in file" + str(fileName) + "...")
            columns = (0, 1, 2, 3, 4, 5)  # x, y, z, v_x, v_y, v_z

            # Read file
            x, y, z, v_x, v_y, v_z = np.loadtxt("ascii_output/" + str(fileName), usecols=columns, unpack=True)

            # Get CM of stars from 'cm_stars_data' file
            x_cm, y_cm, z_cm, v_x_cm, v_y_cm, v_z_cm = np.loadtxt("ascii_output/data_centered/cm_stars_data",
                                                                  usecols=columns, unpack=True)

            # Correction: correct each particle i for dump t
            for i in range(0, len(x)):
                x[i] = x[i] - x_cm[t]
                y[i] = y[i] - y_cm[t]
                z[i] = z[i] - z_cm[t]
                v_x[i] = v_x[i] - v_x_cm[t]
                v_y[i] = v_y[i] - v_y_cm[t]
                v_z[i] = v_z[i] - v_z_cm[t]

            # Write in new file
            columns2 = (6, 7, 8, 9, 10)
            c6, c7, c8, c9, c10 = np.loadtxt("ascii_output/" + str(fileName), usecols=columns2, unpack=True)
            data = np.column_stack([x, y, z, v_x, v_y, v_z, c6, c7, c8, c9, c10])

            # Save centered data
            datafile_path = "ascii_output/data_centered/" + str(fileName)
            np.savetxt(datafile_path, data, fmt='%13.5E' * 9 + '%10d' * 2)

            t += 1  # next dump
