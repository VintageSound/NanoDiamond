from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter


# Function to load settings
def load_settings(data_dir, exp_num):
    # Define the settings file name
    set_name = f'{data_dir}/data_{exp_num}/settings.txt'
    # Load the settings file
    settings = np.loadtxt(set_name, delimiter=' ', dtype=str, max_rows=4)
    print(settings)
    return settings


def sin_fit(i, a, b, c, d):
    return a * np.sin(b * i + c) + d


def twoD_Gaussian(X, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x, y = X
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(- (a * ((x - xo) ** 2) + 2 * b * (x - xo) * (y - yo) + c * ((y - yo) ** 2)))
    return g.ravel()


# Function to process data
def process_data(data_dir, exp_num, settings):
    # Extract parameters from settings
    pic_num = int(settings[3, 1])
    numbers = 4
    width = int(settings[0, 1])
    height = int(settings[1, 1])
    fps = float(settings[2, 1])
    duration = 1 / fps

    x_position = np.zeros(pic_num)
    y_position = np.zeros(pic_num)
    amplitude = np.zeros(pic_num)
    x_width = np.zeros(pic_num)
    y_width = np.zeros(pic_num)
    time = np.linspace(0, duration * pic_num, pic_num, dtype=float)
    exc_array = np.array([0])

    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    x, y = np.meshgrid(x, y)

    for iii in range(pic_num):
        name = f'{data_dir}/data_{exp_num}/data_{iii}'
        name_txt = name + '.txt'
        file = np.loadtxt(name_txt, delimiter=';')
        data = np.zeros([height, width, numbers])

        var = 0
        for i in range(height):
            for ii in range(width):
                data[i, ii] = file[var:var + 4]
                var += 4

        if np.amax(data[:, :, 0]) >= 5:
            index = np.where(data[:, :, 0] == np.amax(data[:, :, 0]))
            if len(index[0]) == 1:
                x_guess = int(index[1])
                y_guess = int(index[0])
            else:
                x_guess = int(index[1][0])
                y_guess = int(index[0][0])
            initial_guess = (np.amax(data[:, :, 0]), x_guess, y_guess, 3, 3, 0, 5)
            data1 = data[:, :, 0].ravel()
            popt, pcov = curve_fit(twoD_Gaussian, (x, y), data1, p0=initial_guess)
            print(iii, popt)
            x_position[iii] = popt[1]
            y_position[iii] = popt[2]
            amplitude[iii] = popt[0]
            x_width[iii] = popt[3]
            y_width[iii] = popt[4]
        else:
            exc_array = np.append(exc_array, iii)

    exc_array = np.delete(exc_array, [0])
    time = np.delete(time, exc_array)
    x_position = np.delete(x_position, exc_array)
    y_position = np.delete(y_position, exc_array)
    amplitude = np.delete(amplitude, exc_array)
    x_width = np.delete(x_width, exc_array)
    y_width = np.delete(y_width, exc_array)

    # FFT
    x_fft = np.abs(np.fft.rfft(x_position))
    y_fft = np.abs(np.fft.rfft(y_position))
    freq = np.fft.rfftfreq(2 * len(x_fft) - 1, (time[-1] - time[0]) / (2 * len(x_fft) - 1))
    amp_fft = np.abs(np.fft.rfft(amplitude))
    fit_freq = freq[20 + np.argmax(x_fft[20:])]

    return time, x_position, y_position, amplitude, x_width, y_width, x_fft, y_fft, freq, amp_fft, fit_freq


# Function to save results
def save_results(data_dir, exp_num, time, freq, x_fft, y_fft, x_position, y_position, amplitude):
    save_name = f'{data_dir}/data_{exp_num}/FFT_results.txt'
    np.savetxt(save_name, (freq, x_fft, y_fft), delimiter=' ')
    save_name = f'{data_dir}/data_{exp_num}/position_results.txt'
    np.savetxt(save_name, (time, x_position, y_position), delimiter=' ')
    save_name = f'{data_dir}/data_{exp_num}/Amplitude_results.txt'
    np.savetxt(save_name, (time, amplitude), delimiter=' ')


# Function to plot X-axis analysis
def plot_x_axis_analysis(data_dir, exp_num, time, x_position):
    fig1 = plt.figure()
    plt.scatter(time * 1000, x_position, s=0.2)
    plt.plot(time * 1000, x_position, label='X-coordinate', linewidth=0.5)
    plt.xlabel('Time, msec')
    plt.ylabel('Position, $\mu$m')
    plt.legend()
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_particle_oscillations.pdf', dpi=500)


# Function to plot Y-axis analysis
def plot_y_axis_analysis(data_dir, exp_num, time, y_position):
    fig2 = plt.figure()
    plt.scatter(time * 1000, y_position, s=0.2)
    plt.plot(time * 1000, y_position, label='Y-coordinate', linewidth=0.5)
    plt.xlabel('Time, msec')
    plt.ylabel('Position, $\mu$m')
    plt.legend()
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_particle_oscillations.pdf', dpi=500)


# Function to plot Y-axis width analysis
def plot_y_axis_width_analysis(data_dir, exp_num, time, y_width):
    fig7 = plt.figure()
    plt.scatter(time * 1000, y_width, s=0.2)
    plt.plot(time * 1000, y_width, linewidth=0.5)
    plt.xlabel('Time, msec')
    plt.ylabel('Amplitude, arb.un.')
    plt.title('$\sigma$ along Y-axis')
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_y_width.png')


# Function to plot Y-axis FFT analysis
def plot_y_axis_fft_analysis(data_dir, exp_num, freq, y_fft, fit_freq):
    fig8 = plt.figure()
    plt.plot(freq, y_fft, label='Y-coordinate')
    plt.yscale('log')
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude, arb.un.')
    plt.title('FFT for Y-axis')
    plt.legend()
    text = str(int(fit_freq)) + 'Hz'
    plt.annotate(text=text, xy=(fit_freq + 5, np.amax(y_fft[50:])))
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_y_fft.png')


# Function to plot amplitude analysis
def plot_amplitude_analysis(data_dir, exp_num, time, amplitude):
    fig9 = plt.figure()
    plt.scatter(time * 1000, amplitude, s=0.2)
    plt.plot(time * 1000, amplitude, linewidth=0.5)
    plt.xlabel('Time, msec')
    plt.ylabel('Amplitude, arb.un.')
    plt.title('Fluorescence intensity')
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_total_intencity.pdf', dpi=500)


# Function to plot amplitude FFT analysis
def plot_amplitude_fft_analysis(data_dir, exp_num, freq, amp_fft, fit_freq):
    fig10 = plt.figure()
    plt.plot(freq, amp_fft, label='Amp')
    plt.yscale('log')
    plt.xlabel('Frequency, Hz')
    plt.ylabel('Amplitude, arb.un.')
    plt.title('FFT for amplitude')
    plt.legend()
    text = str(int(fit_freq)) + 'Hz'
    plt.annotate(text=text, xy=(fit_freq + 5, np.amax(amp_fft[10:])))
    plt.savefig(f'{data_dir}/data_{exp_num}/picture_amp_fft.png')


def today_date():
    # Get today's date
    today = datetime.today()

    # Format it as dd.mm.yy
    date_string = today.strftime("%d.%m.%y")
    return date_string


# Main function
def main():
    # Define experiment number and data directory
    exp_num = 37
    data_dir = 'imaging/' + today_date()
    # Load settings
    settings = load_settings(data_dir, exp_num)
    # Process data
    time, x_position, y_position, amplitude, x_width, y_width, x_fft, y_fft, freq, amp_fft, fit_freq = process_data(data_dir, exp_num, settings)
    # Save results
    save_results(data_dir, exp_num, time, freq, x_fft, y_fft, x_position, y_position, amplitude)
    # Plot X-axis analysis
    plot_x_axis_analysis(data_dir, exp_num, time, x_position)
    # Plot Y-axis analysis
    plot_y_axis_analysis(data_dir, exp_num, time, y_position)
    # Plot Y-axis width analysis
    plot_y_axis_width_analysis(data_dir, exp_num, time, y_width)
    # Plot Y-axis FFT analysis
    plot_y_axis_fft_analysis(data_dir, exp_num, freq, y_fft, fit_freq)
    # Plot amplitude analysis
    plot_amplitude_analysis(data_dir, exp_num, time, amplitude)
    # Plot amplitude FFT analysis
    plot_amplitude_fft_analysis(data_dir, exp_num, freq, amp_fft, fit_freq)
    # Show all plots
    plt.show()


# Run main function if script is run directly
if __name__ == "__main__":
    main()
