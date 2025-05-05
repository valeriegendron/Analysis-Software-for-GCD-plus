import numpy as np

# FOR BOUND PARTICLES ONLY

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
        elif type == 1:  # tides
            dump_number = dump_numbers[type]

        # Read data
        R = np.loadtxt(runs[type][i] + paths[type] + dump_number + "r_v", usecols=11)
        m, He, O, Fe, Z = np.loadtxt(runs[type][i] + paths2[type] + dump_number, usecols=(6, 7, 10, 14, 15), unpack=True)
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

        # Computing metallicities
        Fe_H, O_H, O_Fe = [], [], []
        for j in range(len(R_cut)):
            Fe_H.append(np.log10(data_Z_cut[j, 1] / data_Z_cut[j, 0]) - np.log10(Fe_sun / H_sun))  # [Fe/H]
            O_H.append(np.log10(data_Z_cut[j, 2] / data_Z_cut[j, 0]) - np.log10(O_sun / H_sun))  # [O/H]
            O_Fe.append(np.log10(data_Z_cut[j, 2] / data_Z_cut[j, 1]) - np.log10(O_sun / Fe_sun))  # [O/Fe]

        # Computing mean [Fe/H], [O/H], [O/Fe]
        Fe_H_mean, O_H_mean, O_Fe_mean = np.mean(Fe_H), np.mean(O_H), np.mean(O_Fe)

        # Computing uncertainties
        delta_Fe_H = np.std(Fe_H)/np.sqrt(len(R_cut))
        delta_O_H = np.std(O_H)/np.sqrt(len(R_cut))
        delta_O_Fe = np.std(O_Fe)/np.sqrt(len(R_cut))

        # Write in file
        f = open("metallicity_mean_Fe-O-H", "a")
        # data_ICL_dm = np.column_stack([runs[type][i], dump_number, O_H_mean, delta_O_H, Fe_H_mean, delta_Fe_H,
        #                                O_Fe_mean, delta_O_Fe])
        data_file = np.column_stack([runs[type][i], dump_number, "{:.5f}".format(O_H_mean), "{:.5f}".format(delta_O_H),
                                      "{:.5f}".format(Fe_H_mean), "{:.5f}".format(delta_Fe_H), "{:.5f}".format(O_Fe_mean),
                                      "{:.5f}".format(delta_O_Fe)])
        np.savetxt(f, data_file, fmt='%16s' + '%5s' + '%10s' * 6)
        f.write("\n")
        f.close()
