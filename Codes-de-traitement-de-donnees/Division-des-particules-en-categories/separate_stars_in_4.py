import numpy as np

# Categories:
# 1) old & bound, 2) new & bound, 3) old & ICL, 4) new & ICL

unbound_particles_data_path = 'unbound_stars_data_v3-3'

# Preparing dumps for loop
dumps = np.linspace(0, 500, num=501)  # list containing dump number (int)
str_dumps = []  # list containing dump numbers in string format "xxx"
for i in range(0, len(dumps)):
    if len(str(int(dumps[i]))) == 1:
        str_dumps.append("00" + str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 2:
        str_dumps.append("0" + str(int(dumps[i])))
    elif len(str(int(dumps[i]))) == 3:
        str_dumps.append(str(int(dumps[i])))

for dump in range(0, len(dumps)):
    # Lists that will contain for each time dump the ID and line number of old, new, bound and intracluster stars
    s_old_ID, s_new_ID, s_ICL_ID, s_bound_ID = [], [], [], []
    s_old_line, s_new_line, s_ICL_line, s_bound_line = [], [], [], []

    print("Reading dump " + str(int(dumps[dump])) + " ...")
    ID = np.loadtxt('ascii_output/data_centered/s' + str_dumps[dump], usecols=25, unpack=True)  # stars

    if int(dump) == 0:
        s000_ID = np.loadtxt('ascii_output/data_centered/s' + str_dumps[dump], usecols=25, unpack=True)
        s_old_ID = s000_ID
        for i in range(len(s000_ID)):
            s_old_line.append(i)

    # Checking if ID of star particle is the same or not as a star in file s000
    else:
        for i in range(len(ID)):
            if ID[i] in s000_ID:
                s_old_ID.append(ID[i])
                s_old_line.append(i)

            # Assigning stars to s_new (stars that were formed after time 0)
            else:
                s_new_ID.append(ID[i])
                s_new_line.append(i)

    # Assigning stars to s_ICL (intracluster stars)
    ICL_dump, ICL_line, ICL_ID = np.loadtxt(unbound_particles_data_path, usecols=(0, 1, 2), dtype='int', unpack=True)
    for i in range(len(ICL_dump)):
        if ICL_dump[i] == int(dump):  # we only want data from the current dump
            s_ICL_ID.append(ICL_ID[i])
            s_ICL_line.append(ICL_line[i])
        elif ICL_dump[i] > int(dump):
            break

    # Assigning stars to s_bound (gravitationally bound stars)
    if len(s_ICL_ID) == 0:  # no intracluster stars for the current dump
        s_bound_ID = ID
        for i in range(len(ID)):
            s_bound_line.append(i)
    else:
        for i in range(len(ID)):
            if ID[i] not in s_ICL_ID:
                s_bound_ID.append(ID[i])
                s_bound_line.append(i)

    # Separate in the right 4 categories
    # 1) old & bound and 3) old and ICL
    s_old_bound_ID, s_old_ICL_ID = [], []
    s_old_bound_line, s_old_ICL_line = [], []
    for i in range(len(s_old_ID)):
        if s_old_ID[i] in s_ICL_ID:  # 3) old & ICL
            s_old_ICL_ID.append(s_old_ID[i])
            s_old_ICL_line.append(s_old_line[i])
        else:  # 1) old & bound
            s_old_bound_ID.append(s_old_ID[i])
            s_old_bound_line.append(s_old_line[i])

    # 2) new & bound and 4) new & ICL
    s_new_bound_ID, s_new_ICL_ID = [], []
    s_new_bound_line, s_new_ICL_line = [], []
    for i in range(len(s_new_ID)):
        if s_new_ID[i] in s_ICL_ID:  # 4) new and ICL
            s_new_ICL_ID.append(s_new_ID[i])
            s_new_ICL_line.append(s_new_line[i])
        else:  # 2) new and bound
            s_new_bound_ID.append(s_new_ID[i])
            s_new_bound_line.append(s_new_line[i])

    # Arrange data
    ID_data = s_old_bound_ID + s_new_bound_ID + s_old_ICL_ID + s_new_ICL_ID
    line_data = s_old_bound_line + s_new_bound_line + s_old_ICL_line + s_new_ICL_line
    categories_data = [1]*len(s_old_bound_ID) + [2]*len(s_new_bound_ID) + [3]*len(s_old_ICL_ID) + [4]*len(s_new_ICL_ID)
    dump_data = [int(dump)]*len(ID_data)
    #print(str(len(s_old_bound_ID)) + "<" + str(len(ID_data)))  # MUST BE TRUE, TO VERIFY!

    # Write in file
    f1 = open("stars_separated_in_4", "a")
    data = np.column_stack([categories_data, dump_data, line_data, ID_data])
    np.savetxt(f1, data, fmt='%10d' * 4)
    f1.write("\n")
    f1.close()  # Close each time so that the data will be saved even if there's a disconnection with the server
