import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from scipy.optimize import curve_fit

# font and plot properties
#mpl.rcParams['font.family'] = 'Century Gothic'
plt.rcParams['font.size'] = 18
plt.rcParams['axes.linewidth'] = 1.5

# path properties
path_name = str(r'D:\Experiments\2023-11-08')
file_name = str(r'\30.csv')
number_files = len(os.listdir(path_name))

# integration boundaries
step = int(37)  # for 300 ns

# load the first data file to use it for normalization and prepare result array
file_data = pd.read_csv(path_name + file_name, skiprows=14, dtype=float)
counts_0 = file_data['Photon counts number'].astype(float)
result = np.zeros(number_files, dtype=float)
first_max_index_0 = counts_0[:340].argmax()
norm_factor_0 = np.sum(counts_0[first_max_index_0:first_max_index_0 + 160])

for i in range(0, number_files):
    # load each data file one by one
    file_name = r'/' + str(i) + '.csv'
    file_data = pd.read_csv(path_name + file_name, skiprows=14, dtype=float)
    counts = file_data['Photon counts number'].astype(float)
    # Because of the laser power drift it's necessary to make normalization.
    # For that just integrate first fluorescence pulse counts for each data file
    # and compare it with the same value but for first data file.
    # Their ratio gives you factor which you need just multiply by current data
    # and that's it, you implemented your normalization. You're amazing!
    first_max_index = counts[:340].argmax()
    norm_factor = np.sum(counts[first_max_index:first_max_index + 160])
    counts = counts * (norm_factor_0 / norm_factor)
    # Now you need to measure decrease in fluoresce signal of the second pulse at its beginning.
    # Eventually, it will show your desired Rabi oscillation.
    # For that just integrate second fluorescence pulse (at the beginning) for 0.5 msec.
    # Okay, it seems that now you got it! Just plot it.
    start_1 = int(340 + counts[340:].argmax())
    end_1 = start_1 + step
    result[i] = np.sum(counts[start_1:end_1])

# time array
time_step = 0.008                       # [us]
time = np.arange(0, len(result)*time_step, time_step)
fit_time = np.linspace(0, 1.5, 1000)


def fit_func(t, a, omega, T, phi, b, f):
    return (a - b * np.cos(omega * t + phi)) * np.exp(-t / T) + f

# fitting
init_guess = np.array([1.1e8, 0.0009, 0.2, 3.14, 0, 1e8])
popt, pcov = curve_fit(fit_func, time, result, init_guess)

# plotting
fig2 = plt.figure(figsize=(7, 4))
ax = fig2.add_axes([0.15, 0.18, 0.8, 0.8])
ax.plot(time, result, c='tab:blue')
ax.plot(fit_time, fit_func(fit_time, *popt), c='tab:red')
ax.set_xlabel(r'MW pulse duration, [$\mu$s]')
ax.set_ylabel(r'Fluorescence signal, [a.u.]')
ax.set_xlim([np.amin(fit_time), np.amax(fit_time)])
ax.text(0.9, 1.20, r'$\Omega$ = ' + str(np.round(popt[1], 2)) + r' $\pm$ ' + str(np.round(np.sqrt(np.diag(pcov))[1], 2)) + r' MHz')
ax.text(0.9, 1.14, r'$T_2$ = ' + str(np.round(popt[2], 2)) + r' $\pm$ ' + str(np.round(np.sqrt(np.diag(pcov))[2], 2)) + r' $\mu$s')

print(popt)
#print(pcov)

plt.savefig('Rabi_oscillations.png', dpi=300)

plt.show()