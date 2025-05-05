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

    # Write in file?
    print("[O/H] = " + str(O_H_mean) + " +/- " + str(delta_O_H))
    print("[Fe/H] = " + str(Fe_H_mean) + " +/- " + str(delta_Fe_H))
    print("[O/Fe] = " + str(O_Fe_mean) + " +/- " + str(delta_O_Fe))
