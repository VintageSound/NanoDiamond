import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# path
path = str(r"D:/Experiments/2023-09-21/")

# Read the first CSV file
data = pd.read_csv(path + "1.csv", skiprows=14, nrows=1024)
freq = data['# MW frequency [MHz]']
counts = data['Photon counts number'].astype(float)

# Read the second CSV file
data = pd.read_csv(path + "30.csv", skiprows=14, nrows=1024)
freq_2 = data['# MW frequency [MHz]'].astype(float)
counts_2 = data['Photon counts number'].astype(float)

counts_2 = counts_2 * (np.sum(counts[20:200]) / np.sum(counts_2[20:200]))

# plot
fig, ax = plt.subplots()

ax.plot(counts, label='0')
ax.plot(counts_2, label='1')
ax.plot(counts - counts_2, label='1')
#ax.set_xlim([520, 690])
#ax.set_ylim([6.836e6, 7.599e6])
ax.legend()

plt.show()
