import re
import numpy as np
import pandas as pd
from PIL import ImageGrab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import os
import pyvisa


def is_new_measurement_checked():
    return new_measurement_var.get()


def export_png():
    # Take a screenshot of the window
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    x1 = x0 + root.winfo_width()
    y1 = y0 + root.winfo_height()
    screenshot = ImageGrab.grab(bbox=(x0, y0, x1, y1))

    # Save the screenshot as a PNG file
    screenshot.save(data_name + '.png')
    print('PNG file exported')


def get_trap_parameters():
    resource_name = "GPIB0::12::INSTR"
    resource = pyvisa.ResourceManager().open_resource(resource_name)
    print(resource.query("*IDN?"))
    str = resource.query("apply?")
    trap_frequency, trap_amplitude, trap_offset = str.split(",")
    trap_frequency = trap_frequency.split("N")[1]
    trap_offset = trap_offset.split('''"''')[0]
    trap_frequency, trap_amplitude, trap_offset = float(trap_frequency), float(trap_amplitude) * 1000, float(
        trap_offset)
    return trap_frequency, trap_amplitude, trap_offset


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=".", title="Select a file", filetypes=[("BIN and CSV files", "*.bin; *.csv")])
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Selected file: {file_path}")
    print(f"File name without extension: {file_name}")
    return file_name


def extract_sample_number(txt: str) -> int:
    lines = txt.split('\n')
    channel_1_sample = 0
    channel_2_sample = 0
    for line in lines:
        if 'The total amount of data transmitted on: Channel 1' in line:
            channel_1_sample = int(lines[lines.index(line) + 1].split()[0].replace('-', ''))
        if 'The total amount of data transmitted on: Channel 2' in line:
            channel_2_sample = int(lines[lines.index(line) + 1].split()[0].replace('-', ''))
    if channel_1_sample == channel_2_sample:
        return channel_1_sample
    else:
        raise Exception('Sample numbers on Channel 1 and Channel 2 are not the same.')


def read_log_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        match = re.search(r'Current ADC speed:\s+(\d+)', text)
        if match:
            sample_rate = int(match.group(1))
        else:
            raise ValueError('Could not find ADC speed in text file.')
        samples_number = extract_sample_number(text)
    return sample_rate, samples_number


def read_from_binary(data_input: str):
    f = open(data_input, "rb")
    content = f.read()                                                          # Read file as hex bytes
    data = np.frombuffer(content, np.int16)
    f.close()
    return data


def read_lost(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
    lost = []
    for line in lines:
        numbers = re.findall(r'\b(?<!Channel )\d+\b', line)
        lost.append(numbers)
    return np.array(lost, dtype=int)


def XY_from_data(data: np.ndarray, lost: np.ndarray):
    lost1 = 2
    X_parts = []
    Y_parts = []
    for i in range(0, len(lost)):
        if i == 0:
            shift = 40 #20
            shift_0 = 40 #20
        else:
            shift = 46 #23
        package_position = shift_0 + i * (16384*2 + shift)
        if lost[i][lost1] == 0:
            X_parts.append(data[package_position: package_position + 16384])
            Y_parts.append(data[package_position + 16384: package_position + 16384*2])
    X = np.concatenate(X_parts)
    Y = np.concatenate(Y_parts)
    return X, Y


def run_code():
    global data_name
    data_name = select_file()
    data_output = data_name + ".csv"  # Output file
    if is_new_measurement_checked():
        data_input = data_name + ".bin"  # Input File
        data_log = data_name + ".bin.log"  # Log file
        lost_input = data_name + ".bin.log.lost"  # Lost file
        sample_rate, samples_number = read_log_file(data_log)
        time_step = 1 / sample_rate
        data = read_from_binary(data_input)
        lost = read_lost(lost_input)
        X, Y = XY_from_data(data, lost)
        time = np.arange(0, samples_number * time_step, time_step)
        trap_frequency, trap_amplitude, trap_offset = get_trap_parameters()
        # Create an array to hold the data and trap parameters
        data_array = np.zeros((max(3, len(time) + 1), 4), dtype=object)
        data_array[:4, 3] = [f'Trap Parameters:', f'Trap Frequency: {trap_frequency} Hz', f'Trap Amplitude: {trap_amplitude} V',
                             f'Trap Offset: {trap_offset} V']
        data_array[0, :3] = ['Time', 'X(V)', 'Y(V)']
        data_array[1:len(time) + 1, 0] = time
        data_array[1:len(X) + 1, 1] = X
        data_array[1:len(Y) + 1, 2] = Y
        # Remove the zeros from the fourth column
        data_array[:, 3] = np.where(data_array[:, 3] == 0, '', data_array[:, 3])
        # Write the data and trap parameters to the CSV file
        np.savetxt(data_output, data_array, delimiter=',', fmt='%s')
        print('CSV file created')
    # Read the CSV file
    data = pd.read_csv(data_output, low_memory=False)
    # Make the first value of the first column start from zero
    data.iloc[:, 0] = data.iloc[:, 0] + data.iloc[0, 0]
    # Center the position_x column around 0
    position_x = data.iloc[:, 1] - data.iloc[:, 1].mean()
    position_y = data.iloc[:, 2] - data.iloc[:, 2].mean()
    # Normalize the position_x column
    position_x = position_x / position_x.abs().max()
    position_y = position_y / position_y.abs().max()
    trap_frequency, trap_amplitude, trap_offset = data.iloc[0:3, 3]
    headline_text = f'{trap_frequency}, {trap_amplitude}, {trap_offset}'
    label_headline = tk.Label(root, text=headline_text)
    label_headline.pack()

    # Create a new figure and add subplots to it
    fig = Figure(figsize=(20, 8))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    # Plot the first subplot
    ax1.plot(data.iloc[:, 0], position_x)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Position_x (a.u.)')
    # Set the x-axis limits
    ax1.set_xlim(left=0, right=data.iloc[:, 0].max())

    # Plot the second subplot
    ax2.plot(data.iloc[:, 0], position_y, 'r')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Position_y (a.u.)')
    # Set the x-axis limits
    ax2.set_xlim(left=0, right=data.iloc[:, 0].max())

    # Compute the sampling frequency in Hz
    fs = 1 / (abs(data.iloc[0, 0] - data.iloc[1, 0]))

    # Plot the third subplot
    fx, Pxx_den = signal.periodogram(position_x, fs=fs)
    ax3.semilogy(fx[1:], Pxx_den[1:])
    ax3.set_xlabel('frequency [Hz]')
    ax3.set_ylabel('PSD_X [V**2/Hz]')
    # Set the y-axis limits
    ax3.set_ylim(bottom=0.1 * Pxx_den[1:].min(), top=10 * Pxx_den[1:].max())
    # Set the x-axis limits
    ax3.set_xlim(left=10, right=2100)

    # Plot the fourth subplot
    fy, Pyy_den = signal.periodogram(position_y, fs=fs)
    ax4.semilogy(fy[1:], Pyy_den[1:], 'r')
    ax4.set_xlabel('frequency [Hz]')
    ax4.set_ylabel('PSD_Y [V**2/Hz]')
    # Set the y-axis limits
    ax4.set_ylim(bottom=0.1 * Pyy_den[1:].min(), top=10 * Pyy_den[1:].max())
    # Set the x-axis limits
    ax4.set_xlim(left=10, right=2100)

    # Create a canvas to display the figure on the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Create a new Tkinter window
root = tk.Tk()

# Set the size of the window
root.geometry('1400x600')

# Add a headline to the top of the window
headline_text = f'Select file'
label_headline = tk.Label(root, text=headline_text)
label_headline.pack()

# Add a checkbox to the window for selecting a new measurement
new_measurement_var = tk.BooleanVar(value=False)
checkbox_new_measurement = tk.Checkbutton(root, text='New measurement', variable=new_measurement_var)
checkbox_new_measurement.pack()

# Add a button to the window for exporting the figure as a PNG
button_export_png = tk.Button(root, text='Export PNG', command=export_png)
button_export_png.pack()

# Add a button to the window for selecting a file
button_select_file = tk.Button(root, text='Select File', command=run_code)
button_select_file.pack()

# Run the main loop of the Tkinter window
root.mainloop()

