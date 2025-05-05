# Must run 'cm_recenter_stars.py' beforehand
import numpy as np
import os

t = 0  # will be used as index to keep track of dump number
for fileName in sorted(os.listdir("ascii_output")):
    if fileName.startswith("f"):  # feedback file
        if len(fileName) == 4:  # to make sure it is an output file
            print("Centering particles in file" + str(fileName) + "...")
            columns = (0, 1, 2, 3, 4, 5)  # x, y, z, v_x, v_y, v_z

            # Read file
            if os.path.getsize("ascii_output/" + str(fileName)) == 0:  # if file is empty
                with open("ascii_output/data_centered/" + str(fileName), mode='a'):
                    pass

            else:
                with open("ascii_output/" + str(fileName), "r") as fp:
                    if len(fp.readlines()) == 1:
                        x, y, z, v_x, v_y, v_z = [], [], [], [], [], []
                        x1, y1, z1, v_x1, v_y1, v_z1 = np.loadtxt("ascii_output/" + str(fileName), usecols=columns, unpack=True)
                        x.append(x1), y.append(y1), z.append(z1), v_x.append(v_x1), v_y.append(v_y1), v_z.append(v_z1)
                    else:
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
                columns2 = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
                c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26 = \
                    np.loadtxt("ascii_output/" + str(fileName), usecols=columns2, unpack=True)
                data = np.column_stack(
                    [x, y, z, v_x, v_y, v_z, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21,
                    c22, c23, c24, c25, c26])

                # Save centered data
                datafile_path = "ascii_output/data_centered/" + str(fileName)
                np.savetxt(datafile_path, data, fmt='%13.5E' * 25 + '%10d' * 2)

            t += 1  # next dump
