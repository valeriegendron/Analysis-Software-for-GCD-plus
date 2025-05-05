import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# FOR BOUND PARTICLES ONLY

# Input
runs = ["ISOL_A", "TIDES8_h_p2_mm"]
dump_number = "500"
dt = 0.01  # in Gyr
nbins = [20, 20]  # for isolated run and run with tides, respectively
colors = ["#05cad2", "#8c0404"]
paths = ["/diskev/ascii_output/s", "/diskev/ascii_output/bound_data/s"]

choice = input("Press (1) to get the age distrubtion of stars or press (2) to get the formation epoch distribution,"
               " for dump " + dump_number + ": ")
while choice != '1' and choice != '2':
    choice = input("Wrong key. to get the age distrubtion of stars or press (2) to get the formation"
                   " epoch distribution, for dump " + dump_number + ": ")

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(len(runs)):
    # Read data
    m, age = np.loadtxt(runs[i] + paths[i] + dump_number, usecols=(6, 18), unpack=True)

    # Convert age units to Gyr
    age = age/(10**9)  # operation on array

    if choice == '2':
        for j in range(len(age)):
            age[j] = int(dump_number)*dt - age[j]  # "age" becomes formation epoch
            # if age[j] < 0:
            #     age[j] = 0

    # Make histogram
    sns.histplot(x=age, weights=m, bins=nbins[i], kde=False, color=colors[i], element="step", fill=False,
                 label=runs[i])

if choice == '1':
    plt.xlabel("Age [Gyr]")
    pic_name = "star_age_bound_"
else:
    plt.xlabel("Formation epoch [Gyr]")
    pic_name = "star_fepoch_bound_"
plt.ylabel("Stellar mass [M$_\odot$]")
plt.legend()

# Save figure
plt.savefig(pic_name + runs[0] + "_" + runs[1] + "_" + str(nbins) + "bins_" + dump_number)
