import numpy as np

# Units of sortie.out: t [4.71E+08 yr], (x,y,z) [100 kpc], (vx,vy,vz) [207.4 km/s]
# Final units: t [Gyr], (x,y,z) [kpc], (vx,vy,vz) [km/s]

run = 'TIDES2_h'
file_path = run + "/diskev/sortie.out"

file = open(file_path)
content = file.readlines()[64:]  # skip 64 first lines

t, x, y, z, vx, vy, vz = [], [], [], [], [], [], []  # lists that will contain the values of time, position in x,y,z and velocity for each step

# Extracting useful data
for i in range(len(content)):
    line = content[i]

    # We need to read lines starting with "POT"
    if line[0] == "P" and line[1] == "O" and line[2] == "T":
        t_str, x_str, y_str, z_str, vx_str, vy_str, vz_str = '', '', '', '', '', '', ''  # will contain values in string
        list_str = [t_str, x_str, y_str, z_str, vx_str, vy_str, vz_str]

        list_str_index = 0  # to go through the variables in list_str
        spaces = 0  # to count the number of blank spaces between values
        for j in range(5, len(line)):  # skipping the 'POT:'
            try:
                int(line[j])
                list_str[list_str_index] += line[j]
                spaces = 0
            except ValueError:
                if line[j] == '.' or line[j] == 'E':
                    list_str[list_str_index] += line[j]
                    spaces = 0
                elif line[j] == '+' or line[j] == '-':
                    if spaces == 1:
                        list_str_index += 1  # we have a blank space followed by a + or - sign, meaning we are reading the value of the next variable
                    list_str[list_str_index] += line[j]
                    spaces = 0
                else:
                    spaces += 1
                    if spaces == 2:
                        list_str_index += 1  # we have two blank spaces, meaning we will be reading the value of a new variable next
                        spaces = 0  # reinitialisation for next line

        t.append(float(list_str[0])*(4.71E+08)/(10**9))  # time now in Gyr
        x.append(float(list_str[1])*100), y.append(float(list_str[2])*100), z.append(float(list_str[3])*100)  # positions now in kpc
        vx.append(float(list_str[4])*207.4), vy.append(float(list_str[5])*207.4), vz.append(float(list_str[6])*207.4)  # velocities now in km/s

# Delete duplicates
len_old_t = len(t)  # we want a fixed value (len(t) will change in the loop)
for i in range(1, len_old_t):
    i_reverse = len_old_t - i  # we want to start by the end to make sure the index are not modified while we delete values
    if t[i_reverse] == t[i_reverse-1]:
        del t[i_reverse]
        del x[i_reverse], y[i_reverse], z[i_reverse]
        del vx[i_reverse], vy[i_reverse], vz[i_reverse]

# Writing in new file
data = np.column_stack([t, x, y, z, vx, vy, vz])
np.savetxt(run + "/diskev/sortie_data", data, fmt='%13.5E' * 7)
