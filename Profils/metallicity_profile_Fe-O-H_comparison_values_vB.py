import numpy as np

# FOR BOUND PARTICLES ONLY

# Sun
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_numbers = ["500", "500"]
r_center = 0.5  # radius of central zone, in kpc
H_sun, O_sun, Fe_sun = 0.706, 9.59E-3, 1.17E-3  # masses of H, O and Fe in solar masses
paths = ["/diskev/ascii_output/detilted/s", "/diskev/ascii_output/bound_data/detilted/s"]
paths2 = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]

for i in range(len(runs)):
    # Read data
    R = np.loadtxt(runs[i] + paths[i] + dump_numbers[i] + "r_v", usecols=11)
    m, He, O, Fe, Z = np.loadtxt(runs[i] + paths2[i] + dump_numbers[i], usecols=(6, 7, 10, 14, 15), unpack=True)
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

    #H_mean, Fe_mean, O_mean = np.mean(data_Z_final[:, 0]), np.mean(data_Z_final[:, 1]), np.mean(data_Z_final[:, 2])
    delta_H, delta_Fe, delta_O = np.std(data_Z_final[:, 0])/np.sqrt(len(R_cut)), \
                                 np.std(data_Z_final[:, 1])/np.sqrt(len(R_cut)), \
                                 np.std(data_Z_final[:, 2])/np.sqrt(len(R_cut))

    # delta_Fe_H = (1/np.log(10))*(delta_Fe/Fe_mean + delta_H/H_mean)/(Fe_mean/H_mean)  # np.log(10) = ln(10)
    # delta_O_H = (1/np.log(10))*(delta_O/O_mean + delta_H/H_mean)/(O_mean/H_mean)
    # delta_O_Fe = (1/np.log(10))*(delta_O/O_mean + delta_Fe/Fe_mean)/(O_mean/Fe_mean)

    # Max values
    Fe_H_max = np.log10(np.sum(data_Z_final[:, 1])/np.sum(data_Z_final[:, 0]) + (delta_Fe+delta_H)) - np.log10(Fe_sun/H_sun)
    O_H_max = np.log10(np.sum(data_Z_final[:, 2])/np.sum(data_Z_final[:, 0]) + (delta_O+delta_H)) - np.log10(O_sun/H_sun)
    O_Fe_max = np.log10(np.sum(data_Z_final[:, 2])/np.sum(data_Z_final[:, 1]) + (delta_O+delta_Fe)) - np.log10(O_sun/Fe_sun)

    # Min values
    Fe_H_min = np.log10(np.sum(data_Z_final[:, 1])/np.sum(data_Z_final[:, 0]) - (delta_Fe+delta_H)) - np.log10(Fe_sun/H_sun)
    O_H_min = np.log10(np.sum(data_Z_final[:, 2])/np.sum(data_Z_final[:, 0]) - (delta_O+delta_H)) - np.log10(O_sun/H_sun)
    O_Fe_min = np.log10(np.sum(data_Z_final[:, 2])/np.sum(data_Z_final[:, 1]) - (delta_O+delta_Fe)) - np.log10(O_sun/Fe_sun)

    # Uncertainties
    delta_Fe_H_1, delta_Fe_H_2 = Fe_H_max - Fe_H_mean, Fe_H_mean - Fe_H_min
    delta_O_H_1, delta_O_H_2 = O_H_max - O_H_mean, O_H_mean - O_H_min
    delta_O_Fe_1, delta_O_Fe_2 = O_Fe_max - O_Fe_mean, O_Fe_mean - O_Fe_min

    # Write in file?
    print("[O/H] = " + str(O_H_mean) + " + " + str(delta_O_H_1) + " - " + str(delta_O_H_2))
    print("[Fe/H] = " + str(Fe_H_mean) + " + " + str(delta_Fe_H_1) + " - " + str(delta_Fe_H_2))
    print("[O/Fe] = " + str(O_Fe_mean) + " + " + str(delta_O_Fe_1) + " - " + str(delta_O_Fe_2))
