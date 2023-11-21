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
path_name = str(r'E:\Diamond\Diamond Experiments\2023-11-08')
file_name = str(r'\0.csv')
number_files = len(os.listdir(path_name))
result = np.zeros(number_files, dtype=float)
step = int(37)  # for 300 ns

# This version uses Hezi's way of normalization

for i in range(0, number_files):
    file_name = r'/' + str(i) + '.csv'
    file_data = pd.read_csv(path_name + file_name, skiprows=14, dtype=float)
    counts = file_data['Photon counts number'].astype(float)
    start_1 = int(340 + counts[340:].argmax())
    end_1 = start_1 + step
    start_2 = end_1 + 370
    end_2 = start_2 + step
    A = np.sum(counts[start_1:end_1])
    B = np.sum(counts[start_2:end_2])
    result[i] = (A - B)/(A + B)
    #print(A, B, result[i])

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