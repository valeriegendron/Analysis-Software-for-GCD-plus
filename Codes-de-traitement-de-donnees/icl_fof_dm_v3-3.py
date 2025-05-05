import numpy as np
from datetime import datetime
start_time = datetime.now()

# Parameters
r_lim = 3.0  # in kpc, initial ROI chosen by visual inspection
G = 6.6743*(10**(-11))*(10**(-9))*1.989*(10**(30))  # gravitational constant in units of km^3 M_sun^-1 s^-2
cte = 1/(3.0857*(10**(16)))  # conversion factor to get potential energy in units of M_sun km^2 s^-2 (see line 100)

dumps = np.linspace(0, 500, num=501)  # list containing dump number (int)
str_dumps = []  # list containing dump numbers in string format "xxx"
for i in range(0, len(dumps)):
    if len(str(int(dumps[i]))) == 1:
        str_dumps.append("00" + str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 2:
        str_dumps.append("0" + str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 3:
        str_dumps.append(str(int(dumps[i])))

# LOOP ON ALL DUMPS
# Reading files
for index in range(0, len(dumps)):
    print("Reading dump " + str(int(dumps[index])) + " ...")
    x, y, z, vx, vy, vz, m, ID = np.loadtxt('ascii_output/data_centered/s' + str_dumps[index], usecols=(0, 1, 2, 3, 4, 5, 6, 25),
                                            unpack=True)  # stars
    xg, yg, zg, vxg, vyg, vzg, mg, IDg = np.loadtxt('ascii_output/data_centered/g' + str_dumps[index],
                                                    usecols=(0, 1, 2, 3, 4, 5, 6, 25), unpack=True)  # gas
    xd, yd, zd, vxd, vyd, vzd, md, IDd = np.loadtxt('ascii_output/data_centered/d' + str_dumps[index],
                                                    usecols=(0, 1, 2, 3, 4, 5, 6, 9), unpack=True)  # dark matter

    # Constructing array
    radius, E_kin, Gm_R, candidates = np.zeros(len(x)+len(xg)+len(xd)), np.zeros(len(x)+len(xg)+len(xd)),\
                                      np.zeros(len(x)+len(xg)+len(xd)), np.ones(len(x)+len(xg)+len(xd))  # all particles are candidates (=1 instead of 0)

    data = np.column_stack([np.concatenate((x,xg,xd)), np.concatenate((y,yg,yd)), np.concatenate((z,zg,zd)),
                            np.concatenate((vx,vxg,vxd)), np.concatenate((vy,vyg,vyd)), np.concatenate((vz,vzg,vzd)),
                            np.concatenate((m,mg,md)), np.concatenate((ID,IDg,IDd)), radius, E_kin, Gm_R, candidates])

    # # Computing system's center of mass
    # mx, my, mz, mvx, mvy, mvz, mtot = 0, 0, 0, 0, 0, 0, 0
    # for i in range(data.shape[0]):  # to go through all particles (stars, gas and dm)
    #     mx += data[i, 6]*data[i, 0]  # 6: mass, 0: x
    #     my += data[i, 6]*data[i, 1]  # 1: y
    #     mz += data[i, 6]*data[i, 2]  # 2: z
    #
    #     mvx += data[i, 6]*data[i, 3]  # 3: vx
    #     mvy += data[i, 6]*data[i, 4]  # 4: vy
    #     mvz += data[i, 6]*data[i, 5]  # 5: vz
    #
    #     mtot += data[i, 6]
    #
    #     x_cm, y_cm, z_cm = mx/mtot, my/mtot, mz/mtot
    #     vx_cm, vy_cm, vz_cm = mvx/mtot, mvy/mtot, mvz/mtot
    #
    #     # AJOUTER DANS DES LISTES POUR ÉCRIRE DANS UN FICHIER À PART?
    #
    # # Centering data on center of mass
    # for i in range(data.shape[0]):
    #     data[i, 0] = data[i, 0] - x_cm
    #     data[i, 1] = data[i, 1] - y_cm
    #     data[i, 2] = data[i, 2] - z_cm
    #
    #     data[i, 3] = data[i, 3] - vx_cm
    #     data[i, 4] = data[i, 4] - vy_cm
    #     data[i, 5] = data[i, 5] - vz_cm

    # Computing radius, kinetic energy and factor Gm/R
    for i in range(data.shape[0]):
        # Radius
        data[i, 8] = np.sqrt((data[i, 0])**2 + (data[i, 1])**2 + (data[i, 2])**2)  # 8: radius, 0-1-2: x-y-z
        # Kinetic energy
        data[i, 9] = 0.5*data[i, 6]*((data[i, 3])**2+(data[i, 4])**2+(data[i, 5])**2)  # 0.5*m*(vx**2+vy**2+vz**2), in units of km^2 s^-2
        # Factor Gm/R
        data[i, 10] = cte*G*data[i, 6]/(data[i, 8])  # in units of km^2 s^-2

    # Mass in initial ROI
    M_central = 0
    for i in range(data.shape[0]):
        if data[i, 8] <= r_lim:  # particle in ROI
            M_central += data[i, 6]
            data[i, 11] = 0  # not a candidate anymore

    print("    Starting algorithm...")
    # Algorithm
    M_central_old = 0
    loop = 0
    while M_central_old < M_central:
        M_central_old = M_central  # so it is updated each iteration
        for i in range(data.shape[0]):
            if data[i, 11] == 1:  # is a candidate
                E_pot = -M_central*data[i, 10]
                if E_pot + data[i, 9] <= 0:  # gravitationally bound
                    M_central += data[i, 6]
                    data[i, 11] = 0  # not a candidate anymore
        loop += 1
        print("        Gone through the loop " + str(loop) + " time(s).")

    # # Write data for CM
    # f1 = open("cm_system_data", "a")
    # data_cm = np.column_stack([x_cm, y_cm, z_cm, vx_cm, vy_cm, vz_cm])
    # np.savetxt(f1, data_cm)
    # f1.write("\n")
    # f1.close()

    # Write data for intracluster stars from that time dump in file
    ICL_dump, ICL_line, ICL_ID = [], [], []
    for i in range(len(x)):  # to go through star particles only
        if int(data[i, 11]) == 1:  # ICL
            ICL_dump.append(dumps[index])
            ICL_line.append(i)
            ICL_ID.append(data[i, 7])

    f2 = open("unbound_stars_data_v3-3", "a")
    if len(ICL_dump) != 0:  # Only write in file if there is actually data to write
        data_ICL_stars = np.column_stack([ICL_dump, ICL_line, ICL_ID])
        np.savetxt(f2, data_ICL_stars, fmt='%10d' * 3)
        f2.write("\n")
    f2.close()  # Close each time so that the data will be saved even if there's a disconnection with the server

    # Write data for intracluster gas from that time dump in file
    g_ICL_dump, g_ICL_line, g_ICL_ID = [], [], []
    for i in range(len(x), len(x)+len(xg)):  # to go through gas particles only
        if int(data[i, 11]) == 1:  # unbound
            g_ICL_dump.append(dumps[index])
            g_ICL_line.append(i-len(x))
            g_ICL_ID.append(data[i, 7])

    f3 = open("unbound_gas_data_v3-3", "a")
    if len(g_ICL_dump) != 0:  # Only write in file if there is actually data to write
        data_ICL_gas = np.column_stack([g_ICL_dump, g_ICL_line, g_ICL_ID])
        np.savetxt(f3, data_ICL_gas, fmt='%10d' * 3)
        f3.write("\n")
    f3.close()

    # Write data for intracluster dm from that time dump in file
    d_ICL_dump, d_ICL_line, d_ICL_ID = [], [], []
    for i in range(len(x)+len(xg), len(x)+len(xg)+len(xd)):  # to go through dm particles only
        if int(data[i, 11]) == 1:  # unbound
            d_ICL_dump.append(dumps[index])
            d_ICL_line.append(i - len(x)-len(xg))
            d_ICL_ID.append(data[i, 7])

    f4 = open("unbound_dm_data_v3-3", "a")
    if len(d_ICL_dump) != 0:  # Only write in file if there is actually data to write
        data_ICL_dm = np.column_stack([d_ICL_dump, d_ICL_line, d_ICL_ID])
        np.savetxt(f4, data_ICL_dm, fmt='%10d' * 3)
        f4.write("\n")
    f4.close()

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
