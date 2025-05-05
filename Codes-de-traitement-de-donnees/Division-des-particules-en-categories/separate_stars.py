import numpy as np


def separate_stars(unbound_particles_data_path, s000_path, current_dump, sx, sy, ID, plan, choice):
    """
    For a single time dump, separates the stars in up to 4 categories: i) stars that were already formed before the
    simulation started, ii) stars that have formed with the interaction of the galaxies, a) intracluster stars and
    b) gravitationally bound stars.

    :param unbound_particles_data_path: path to the 'unbound_particles_data' file
    :param s000_path: path to the 's000' file
    :param current_dump: number of the current time dump in string format (ex: "152")
    :param sx: list of x coordinates of star file corresponding to current_dump
    :param sy: list of y coordinates of star file corresponding to current_dump
    :param ID: list of ID of star particles corresponding to current_dump
    :param plan: choice of coordinates ('xy', 'xz' or 'yz')
    :param choice: user input. '1' to get stars that were formed during the interaction or '2' to get intracluster stars

    :returns s_before_x, s_before_y: lists of x and y coordinates corresponding to stars in category i)
             s_after_x, s_after_y: lists of x and y coordinates corresponding to stars in category ii)
             s_ICL_x, s_ICL_y: lists of x and y coordinates corresponding to stars in category a)
             s_bound_x, s_bound_y: lists of x and y coordinates corresponding to stars in category b)
    """

    # Lists that will contain, for a specific time dump, the x et y coordinates of stars in categorie i), ii), a) and b)
    s_before_x, s_after_x, s_ICL_x, s_bound_x = [], [], [], []
    s_before_y, s_after_y, s_ICL_y, s_bound_y = [], [], [], []

    if choice == '1':
        # Assigning stars to s_before (stars that were formed before the simulation)
        s000_ID = np.loadtxt(s000_path, usecols=25)

        if int(current_dump) == 0:
            s000_x, s000_y, s000_z = np.loadtxt(s000_path, usecols=(0, 1, 2), unpack=True)
            #global s000_ID
            if plan == 'xy':
                s_before_x, s_before_y = s000_x, s000_y
            elif plan == 'xz':
                s_before_x, s_before_y = s000_x, s000_z
            elif plan == 'yz':
                s_before_x, s_before_y = s000_y, s000_z

        # Checking if ID of star particle is the same or not as a star in file s000
        else:
            for i in range(len(sx)):
                if ID[i] in s000_ID:
                    s_before_x.append(sx[i]), s_before_y.append(sy[i])

                # Assigning stars to s_after (stars that were formed by interaction)
                else:
                    s_after_x.append(sx[i]), s_after_y.append(sy[i])

            # s_before_x.append(sx[ID == s000_ID]), s_before_y.append(sy[ID == s000_ID])
            #
            # # Assigning stars to s_after (stars that were formed by interaction)
            # s_after_x.append(sx[ID != s000_ID]), s_after_y.append(sy[ID != s000_ID])

    elif choice == '2':
        # Assigning stars to s_ICL (intracluster stars)
        ICL_dump, ICL_line, ICL_ID = np.loadtxt(unbound_particles_data_path, usecols=(0, 1, 2), dtype='int', unpack=True)
        ID_index = []  # list that will be used to keep track of intracluster stars' ID at a specific time dump
        for i in range(len(ICL_dump)):
            if ICL_dump[i] == int(current_dump):
                s_ICL_x.append(sx[ICL_line[i]]), s_ICL_y.append(sy[ICL_line[i]])
                ID_index.append(ICL_ID[i])
            elif ICL_dump[i] > int(current_dump):
                break

        # Assigning stars to s_bound (gravitationally bound stars)
        if len(ID_index) == 0:  # no intracluster stars
            s_bound_x = sx
            s_bound_y = sy
        else:
            for i in range(len(sx)):
                if ID[i] not in ID_index:
                    s_bound_x.append(sx[i]), s_bound_y.append(sy[i])
            #s_bound_x.append(sx[ID != ID_index]), s_bound_y.append(sy[ID != ID_index])

    return (s_before_x, s_before_y, s_after_x, s_after_y) if choice == '1' else (s_bound_x, s_bound_y, s_ICL_x, s_ICL_y)