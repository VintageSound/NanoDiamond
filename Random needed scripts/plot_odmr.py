import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# font and plot properties
plt.rcParams['font.size'] = 18
plt.rcParams['axes.linewidth'] = 1.5

# path properties
path_name = str(r'D:\Experiments\2023-11-13')
file_name = str(r'\0.csv')
number_files = len(os.listdir(path_name))