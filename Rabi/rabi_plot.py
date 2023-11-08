import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv
import re
from collections import defaultdict


def natural_sort_key(s):
    """Key function for natural sorting"""
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', s)]


# path
folder_path = str(r"D:\Experiments\2023-09-21/")

# Get a sorted list of CSV files in the folder
files = sorted(os.listdir(folder_path), key=natural_sort_key)

# Find number of files in the folder
num = os.listdir(folder_path).__len__()

# first point
first_file_path = os.path.join(folder_path, files[0])
init_parameters = pd.read_csv(first_file_path, nrows=14).to_numpy()
init_data = pd.read_csv(first_file_path, skiprows=14)
init_counts = init_data['Photon counts number']
#init_counts.astype(float)


# total sum
step = init_parameters[1][1]
result = []
timestep = 300                          #amount of time to sum in ns
Astart = 375
Astop = Astart+23
print(Astop)
print(Astop-Astart)
Bstop = int(536)
Bstart = Bstop - (Astop - Astart)

for filename in files:
    i = 0
    try:
        file_path = os.path.join(folder_path, filename)
        data = pd.read_csv(file_path, skiprows=14, nrows=1024)
        freq = data['# MW frequency [MHz]']
        counts = data['Photon counts number']
        counts.astype(float)
    except Exception:
        print(filename)

    # normalization
    # counts = counts * (np.sum(init_counts[start:stop]) / np.sum(counts[start:stop]))
    # counts = counts * (np.sum(init_counts[20:200]) / np.sum(counts[20:200]))
    # print(np.sum(init_counts[start:stop]) / np.sum(counts[start:stop]))

    # calculation of the rabi signal point
    sumA = np.sum(counts[Astart:Astop])
    sumB = np.sum(counts[Bstart:Bstop])
    # sum[i] = np.sum(counts[begin:end])
    if i < 1:
        print("sumA = ", sumA)
        print("sumB = ", sumB)
    result.append((sumA - sumB)/(sumA + sumB))
    i = i+1

maxi = max(result)
print(maxi)
norm_res = [x/maxi for x in result]
# plot
x_axis = np.linspace(0, num-1, num)*0.008
fig, ax = plt.subplots()

# ax.plot(x_axis,sum[0:])
ax.plot(result)


plt.show()
