import numpy as np
import os

# Go through all star files to calculate center of mass
cm_x, cm_y, cm_z, cm_vx, cm_vy, cm_vz = [], [], [], [], [], []  # Will contain position of stars center of mass for each dump
for fileName in sorted(os.listdir("ascii_output")):
    if fileName.startswith("s"):  # star file
        if len(fileName) == 4:  # to make sure it is an output file
            print("Centering particles in file" + str(fileName) + "...")
            columns = (0, 1, 2, 3, 4, 5, 6)  # x, y, z, v_x, v_y, v_z and particle masse

            # Read file
            x, y, z, v_x, v_y, v_z, mass = np.loadtxt("ascii_output/" + str(fileName), usecols=columns, unpack=True)

            # Compute center of mass
            mx, my, mz, mv_x, mv_y, mv_z, m_tot = 0, 0, 0, 0, 0, 0, 0
            for i in range(0, len(x)):
                mx += mass[i] * x[i]
                my += mass[i] * y[i]
                mz += mass[i] * z[i]
                mv_x += mass[i] * v_x[i]
                mv_y += mass[i] * v_y[i]
                mv_z += mass[i] * v_z[i]
                m_tot += mass[i]

            x_cm, y_cm, z_cm = mx / m_tot, my / m_tot, mz / m_tot
            v_x_cm, v_y_cm, v_z_cm = mv_x / m_tot, mv_y / m_tot, mv_z / m_tot

            # Add to lists
            cm_x.append(x_cm), cm_y.append(y_cm), cm_z.append(z_cm)
            cm_vx.append(v_x_cm), cm_vy.append(v_y_cm), cm_vz.append(v_z_cm)

            # Correction
            for i in range(0, len(x)):
                x[i] = x[i] - x_cm
                y[i] = y[i] - y_cm
                z[i] = z[i] - z_cm
                v_x[i] = v_x[i] - v_x_cm
                v_y[i] = v_y[i] - v_y_cm
                v_z[i] = v_z[i] - v_z_cm

            # Write in new file
            columns2 = (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26)
            c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26 = np.loadtxt(
                "ascii_output/" + str(fileName), usecols=columns2, unpack=True)
            data = np.column_stack(
                [x, y, z, v_x, v_y, v_z, mass, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21,
                 c22, c23, c24, c25, c26])

            # Save centered data
            datafile_path = "ascii_output/data_centered/" + str(fileName)
            np.savetxt(datafile_path, data, fmt='%13.5E'*25 + '%10d'*2)


# Save stars CM data (to be used to recenter gas and DM)
datafile_path2 = "ascii_output/data_centered/cm_stars_data"
data_cm = np.column_stack([cm_x, cm_y, cm_z, cm_vx, cm_vy, cm_vz])
np.savetxt(datafile_path2, data_cm)
