import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# font and plot properties
plt.rcParams['font.size'] = 18
plt.rcParams['axes.linewidth'] = 1.5

# path properties
path_name = str(r'C:\Users\user\PycharmProjects\NanoDiamond\data\2023-11-20 lambda2 test')
file_name = str(r'\0.csv')
number_files = len(os.listdir(path_name))
file_data = pd.read_csv(path_name + file_name, skiprows=7, dtype=float)
freq = file_data['# MW frequency [MHz]'].astype(float)

for i in range(0, number_files):
    # load each data file one by one
    file_name = r'/' + str(i) + '.csv'
    file_data = pd.read_csv(path_name + file_name, skiprows=7, dtype=float)
    counts = file_data['Photon counts number'].astype(float)
    counts -= np.min(counts)
    counts /= np.max(counts)
    plt.plot(freq, counts)

plt.show()