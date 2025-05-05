import numpy as np

# FOR BOUND PARTICLES ONLY

# Sun
runs_isol = ["ISOL_B", "ISOL_C", "ISOL_I", "ISOL_I", "ISOL_I", "ISOL_G", "ISOL_G", "ISOL_G", "ISOL_G", "ISOL_A",
        "ISOL_A", "ISOL_A", "ISOL_A", "ISOL_A", "ISOL_J", "ISOL_J", "ISOL_J", "ISOL_J", "ISOL_E", "ISOL9_h_p3_mm",
        "ISOL9_h_p3_mm", "ISOL9_h_p3_mm", "ISOL9_h_p3_mm", "ISOL9_h_p3_mm", "ISOL_F", "ISOL_F", "ISOL_H", "ISOL_H",
        "ISOL_H", "ISOL_H", "ISOL8_h", "ISOL8_h", "ISOL8_h", "ISOL8_h", "ISOL8_h", "ISOL_D", "ISOL_D", "ISOL_D",
        "ISOL_D", "ISOL_D", "ISOL_D", "ISOL10_h_p3_mm"]

runs_tides = ["TIDES_G", "TIDES9_h_p3_mm", "TIDES_H", "TIDES8_h_p3_mm", "TIDES8_h_p2_mm", "TIDES8_h_r", "TIDES8_h_p_mm",
              "TIDES8_h_p_m", "TIDES8_h_r2", "TIDES8_h_a", "TIDES10_h_p3_mm"]
dump_numbers_isol = ["437", "272", "371", "452", "500", "111", "355", "399", "476", "085", "294", "313", "359", "500",
                     "201", "251", "323", "500", "484", "143", "172", "219", "354", "455", "264", "341", "061", "098",
                     "147", "265", "132", "154", "186", "272", "351", "122", "183", "297", "321", "440", "484", "223"]
runs = [runs_isol, runs_tides]
dump_numbers = [dump_numbers_isol, "500"]
r_center = 0.5  # radius of central zone, in kpc
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]
paths2 = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]

for type in range(len(runs)):
    for i in range(len(runs[type])):
        if type == 0:  # isol
            dump_number = dump_numbers[type][i]
        elif type == 1:  #tides
            dump_number = dump_numbers[i]

        # Read data
        R = np.loadtxt(runs[type][i] + paths[type] + dump_number + "r_v", usecols=11)
        m, He, O, Fe, Z = np.loadtxt(runs[i] + paths2[i] + dump_number, usecols=(6, 7, 10, 14, 15), unpack=True)
        H = m - He - Z  # operation on arrays
        data_Z = np.column_stack((H, Fe, O))

        # Cut data
        R_cut, data_Z_cut = [], np.zeros((len(R)-1, 3))  # will contain data only for particle which R[j] <= r_center

        k = 0
        for j in range(len(R)):
            if R[j] <= r_center:  # in central zone
                R_cut.append(R[j])
                data_Z_cut[k, :] = data_Z[j, :]
                k += 1

        data_Z_final = data_Z_cut[0:len(R_cut), :]

        # Compute mean [Fe/H], [O/H] and [O/Fe], and uncertainties
        Fe_H_mean = np.log10(np.sum(data_Z_final[:, 1])/np.sum(data_Z_final[:, 0])) - np.log10(Fe_sun / H_sun)
        O_H_mean = np.log10(np.sum(data_Z_final[:, 2]) / np.sum(data_Z_final[:, 0])) - np.log10(O_sun / H_sun)
        O_Fe_mean = np.log10(np.sum(data_Z_final[:, 2]) / np.sum(data_Z_final[:, 1])) - np.log10(O_sun / Fe_sun)

        H_mean, Fe_mean, O_mean = np.mean(data_Z_final[:, 0]), np.mean(data_Z_final[:, 1]), np.mean(data_Z_final[:, 2])
        delta_H, delta_Fe, delta_O = np.std(data_Z_final[:, 0])/np.sqrt(len(R_cut)), \
                                     np.std(data_Z_final[:, 1])/np.sqrt(len(R_cut)), \
                                     np.std(data_Z_final[:, 2])/np.sqrt(len(R_cut))

        delta_Fe_H = (1/np.log(10))*(delta_Fe/Fe_mean + delta_H/H_mean)/(Fe_mean/H_mean)  # np.log(10) = ln(10)
        delta_O_H = (1/np.log(10))*(delta_O/O_mean + delta_H/H_mean)/(O_mean/H_mean)
        delta_O_Fe = (1/np.log(10))*(delta_O/O_mean + delta_Fe/Fe_mean)/(O_mean/Fe_mean)

        # Write in file?
        f = open("metallicity_mean_Fe-O-H_vB", "a")
        data_file = np.column_stack([runs[type][i], dump_number, O_H_mean, Fe_H_mean, O_Fe_mean, delta_O_H,
                                       delta_Fe_H, delta_O_Fe])
        np.savetxt(f, data_file, fmt='%16s' + '%8d' + '%10.5E' * 6)
        f.write("\n")
        f.close()
