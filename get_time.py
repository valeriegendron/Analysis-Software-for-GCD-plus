def get_time(file_path):
    """
    Computes the time interval between two dumps of the simulation, using the 'input.dat' file.
    Uses the total number of output files and the total time of the simulation, specified in the 'input.dat' file
    :param file_path: path to the input file to open
    :return: dt (time interval in Gyr)
             noutput (number of output files)
    """
    file = open(file_path)
    content = file.readlines()
    ligne3_str = content[3]
    ligne7_str = content[7]

    noutput_str = ''
    for j in range(0, len(ligne3_str)):
        try:
            int(ligne3_str[j])
            noutput_str = noutput_str + ligne3_str[j]
        except ValueError:
            break
    noutput = int(noutput_str)

    total_time_str = ''
    for i in range(4, len(ligne7_str)):
        try:
            int(ligne7_str[i])
            total_time_str = total_time_str + ligne7_str[i]
        except ValueError:
            if ligne7_str[i] == '.':
                total_time_str = total_time_str + ligne7_str[i]
            else:
                break

    total_time = float(total_time_str)
    dt = total_time/noutput
    return dt, noutput
