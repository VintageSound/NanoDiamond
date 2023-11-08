# this file is trial to plot raw data from csv bitstream

import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# def pick_file():
#   file_path = filedialog.askopenfilename()
#   print(file_path)
#
#   with open(file_path, 'r') as csvfile:
#     reader = csv.reader(csvfile, delimiter='\t')
#     x_data = []
#     y1_data = []
#     y2_data = []
#     count = 0
#     for row in reader:
#       if count < 2*10**6:
#         x_data.append(int(row[0]))
#         y1_data.append(float(row[1]))
#         y2_data.append(float(row[2]))
#         count += 1
#       else:
#         break
#
#   plt.plot(x_data, y1_data, label='y1')
#   plt.plot(x_data, y2_data, label='y2')
#   plt.xlabel('x')
#   plt.ylabel('y')
#   plt.legend()
#   plt.show()
#
# root = tk.Tk()
# button = tk.Button(root, text='Pick a file', command=pick_file)
# button.pack()
#
# root.mainloop()

import pyvisa

def get_frequency_and_amplitude(gpib_address):
  resource = pyvisa.ResourceManager().open_resource("GPIB0::12::INSTR")
  response = resource.query("apply?")
  frequency, amplitude, offset = response.split(",")
  waveform, frequency = frequency.
  frequency = float(frequency)
  amplitude = float(amplitude)
  return frequency, amplitude

def save_to_file(frequency, amplitude):
  with open("data/data.txt", "a") as file:
    file.write(f"Amplitude : {amplitude:.2f} (Vpp)\n")
    file.write(f"Frequency: {frequency:.2f} (Hz)\n")

if __name__ == "__main__":
  gpib_address = 12
  frequency, amplitude = get_frequency_and_amplitude(gpib_address)
  save_to_file(frequency, amplitude)