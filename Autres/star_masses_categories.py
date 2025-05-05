import numpy as np

dump_number = 500
dump_name = "s500"
run_name = "TIDES8_h_e"

# Read file
m = np.loadtxt(run_name + "/diskev/ascii_output/" + dump_name, usecols=6)

cat, dumps, line = np.loadtxt(run_name + "/diskev/stars_separated_in_4", usecols=(0, 1, 2), unpack=True)
cat = [int(i) for i in cat]  # to make sure we have an array of integers
line = [int(i) for i in line]

# To separate in the 4 categories of stars, we need to use the file "stars_separated_in_4"
# We only use the information related to the dump number chosen
index_min = np.searchsorted(dumps, dump_number - 0.5)
index_max = np.searchsorted(dumps, dump_number + 0.5)-1

m_cat = np.take(m, line[index_min:index_max])
cat_plot = cat[index_min:index_max]

# Count how much elements are in each of the four categories
cat_1, cat_2, cat_3, cat_4 = cat_plot.count(1), cat_plot.count(2), cat_plot.count(3), cat_plot.count(4)

# Computing masses
m_tot, m_1, m_2, m_3, m_4 = 0, 0, 0, 0, 0
for i in range(len(m_cat)):
    m_tot += m_cat[i]
    if 0 <= i < cat_1:
        m_1 += m_cat[i]
    elif cat_1 <= i < (cat_1 + cat_2):
        m_2 += m_cat[i]
    elif (cat_1 + cat_2) <= i < (cat_1 + cat_2 + cat_3):
        m_3 += m_cat[i]
    elif (cat_1 + cat_2 + cat_3) <= i < (cat_1 + cat_2 + cat_3 + cat_4):
        m_4 += m_cat[i]

m_1_ratio, m_2_ratio, m_3_ratio, m_4_ratio = m_1/m_tot, m_2/m_tot, m_3/m_tot, m_4/m_tot

m_tot_check = len(m)*m[0]  # m_tot should always equal m_tot_check!
m_1_ratio_check, m_2_ratio_check, m_3_ratio_check, m_4_ratio_check \
    = cat_1*m[0]/m_tot, cat_2*m[0]/m_tot, cat_3*m[0]/m_tot, cat_4*m[0]/m_tot

print("m_tot: " + str(m_tot) + " M_sun")
print("m1_ratio, m2_ratio, m3_ratio, m4_ratio = " + str(m_1_ratio) + ", " + str(m_2_ratio)
      + ", " + str(m_3_ratio) + ", " + str(m_4_ratio))

# print("m_tot_check: " + str(m_tot_check))
# print("m1_ratio_check, m2_ratio_check, m3_ratio_check, m4_ratio_check = "
#       + str(m_1_ratio_check) + ", " + str(m_2_ratio_check) + ", " + str(m_3_ratio_check) + ", " + str(m_4_ratio_check))
