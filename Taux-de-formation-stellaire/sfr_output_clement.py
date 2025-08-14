import numpy as np


np.printoptions(threshold=np.inf)

run_name = 'run_name_here'

interval = float(input("What is the time interval between your timesteps (in years, use scientific notation)?"))

times, m_stars, m_gas, sfr = [], [], [], []

times.append(0)
m_stars.append(np.sum(np.loadtxt("ascii_output/s000", usecols=6, unpack=True)))
m_gas.append(np.sum(np.loadtxt("ascii_output/g000", usecols=6, unpack=True)))
sfr.append(0)

filenames_s, filenames_g = ["s000"], ["g000"]

timestep = 1

while True:
    filenames_s.append(f"s{str(timestep).zfill(3)}")
    filenames_g.append(f"g{str(timestep).zfill(3)}")

    filename_s = filenames_s[-1]
    filename_g = filenames_g[-1]
    Id_old = np.loadtxt("ascii_output/" + filenames_s[timestep - 1], usecols=25, unpack=True)

    try:
        stars = np.loadtxt("ascii_output/" + filename_s, usecols=(6, 25), unpack=True)
        gas = np.loadtxt("ascii_output/" + filename_g, usecols=6, unpack=True)
    except FileNotFoundError:
        break

    mask = ~np.isin(stars[1], Id_old)

    times.append(timestep*interval)
    m_stars.append(np.sum(stars[0]))
    m_gas.append(np.sum(gas))
    sfr.append(np.sum(stars[0][mask])/interval)

    timestep += 1

data = np.array([times, m_stars, m_gas, sfr])

np.savetxt(f'{run_name}_sfr', data.T, fmt=['%.3e','%.5e', '%.5e', '%.5e'])