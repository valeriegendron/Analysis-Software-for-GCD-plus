import numpy as np

dump_number = "500"  # string format
s_dump, g_dump, d_dump = "s" + dump_number, "g" + dump_number, "d" + dump_number
dump_names = np.array([s_dump, g_dump, d_dump])
ICL_file_names = np.array(["unbound_stars_data_v3-3", "unbound_gas_data_v3-3", "unbound_dm_data_v3-3"])
ID_column = np.array([25, 25, 9])
fmts = np.array(['%13.5E'*25 + '%10d'*2, '%13.5E' * 25 + '%10d' * 2, '%13.5E' * 9 + '%10d' * 2])

for k in range(len(dump_names)):
    print("Sorting file " + dump_names[k] + "...")
    # Read file
    data = np.loadtxt("ascii_output/" + dump_names[k], unpack=False)

    # Separate particles (we only want bound particles)
    ICL_dumps, ICL_lines, ICL_IDs = np.loadtxt(ICL_file_names[k], usecols=(0, 1, 2), dtype='int', unpack=True)

    # We only use the information related to the dump number chosen
    index_min = np.searchsorted(ICL_dumps, int(dump_number) - 0.5)
    index_max = np.searchsorted(ICL_dumps, int(dump_number) + 0.5)

    # Truncating the lists ICL_lines and ICL_IDs
    ICL_lines_dump, ICL_IDs_dump = ICL_lines[index_min:index_max], ICL_IDs[index_min:index_max]

    # Only keeping information related to bound particles
    # i_to_delete = []  # rows that will be deleted, since they correspond to ICL particles
    # for i in range(data.shape[0]):  # going through all rows (one row per particle)
    #     if data[i, ID_column[k]] in ICL_IDs_dump:  # ICL particle to delete
    #         i_to_delete.append(i)
    #
    # data_bound = np.delete(data, i_to_delete, 0)  # deleting all rows identified as ICL
    data_bound = np.delete(data, ICL_lines_dump, 0)

    # Saving information in new file
    datafile_path = "ascii_output/bound_data/" + dump_names[k]
    np.savetxt(datafile_path, data_bound, fmt=fmts[k])
