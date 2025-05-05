import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt


r_eff_isol = [1.7435, 1.6957, 1.8469, 1.8215, 1.7784, 1.9853, 1.9181, 1.9071, 2.1486, 1.6575, 1.6166, 1.5830, 1.5857,
              1.5467, 1.6927, 1.6503, 1.6128, 1.5394, 1.8003, 1.8066, 1.7743, 1.6158, 1.6197, 1.6286, 1.5934, 1.5046,
              1.7813, 1.9336, 1.7801, 1.7180, 1.7210, 1.6209, 1.5814, 1.5451, 1.6090, 1.9273, 1.9920, 1.7766, 1.8124,
              1.6472, 1.5992, 1.9063]
m_star_isol = [7.2579e8, 7.2590e8, 8.1399e8, 8.2700e8, 8.4002e8, 7.2610e8, 8.1405e8, 8.2720e8, 8.4960e8, 7.2595e8,
               8.1370e8, 8.2695e8, 8.4950e8, 8.9125e8, 8.1388e8, 8.2695e8, 8.4927e8, 8.9322e8, 8.9938e8, 8.1410e8,
               8.2700e8, 8.4990e8, 8.9910e8, 9.3070e8, 8.9902e8, 9.3111e8, 8.1405e8, 8.2725e8, 8.4935e8, 8.9965e8,
               8.1395e8, 8.2665e8, 8.4950e8, 8.9925e8, 9.3100e8, 8.9925e8, 9.3090e8, 10.163e8, 10.330e8, 10.825e8,
               11.060e8, 26.60e8]
# isol_labels = []

r_eff_tides = [1.5461, 1.2153, 1.1273, 1.1526, 0.9839, 0.8538, 0.7402, 0.6316, 0.9953, 1.2551, 1.0401]
m_star_tides = [7.2579e8, 8.1407e8, 8.2699e8, 8.4959e8, 8.9936e8, 9.3102e8, 10.164e8, 10.332e8, 10.828e8,
                11.0622e8, 26.60e8]  # bound stars only
# tides_labels = ["TIDES_G", "TIDES9_h_p3_mm", "TIDES_H", "TIDES8_h_p3_mm", "TIDES8_h_p2_mm", "TIDES8_h_r",
#                 "TIDES8_h_p_mm", "TIDES8_h_p_m" "TIDES8_h_r2", "TIDES8_h_a", "TIDES10_h_p3_mm"]

# Setting figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Plot
#colors = iter(cm.gist_rainbow(np.linspace(0, 1, 5)))  # a color for each run
for i in range(len(r_eff_isol)):
    #c = next(colors)
    ax.scatter(m_star_isol[i], r_eff_isol[i], color="#242363", s=25, marker="x")  # isolated runs
for i in range(len(r_eff_tides)):
    ax.scatter(m_star_tides[i], r_eff_tides[i], color="#ec3c34", s=25, marker='.')  # runs with tides

ax.set_xlabel("Stellar mass [M$_\odot$]")
ax.set_ylabel("Effective radius [kpc]")
#ax.legend()
fig.tight_layout()

# Save figure
plt.savefig("remnant_figures/r_eff_comparison.png", dpi=500)
