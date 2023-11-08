import numpy as np
import matplotlib.pyplot as plt

# load the file with results
exp_num = str(1)
data_name = str('result_') + exp_num
settings_name = str('settings_') + exp_num
x, y, z, v_x, v_y, v_z, t = np.loadtxt(fname=data_name, unpack=False)
q_p, m, AC_omega, q_c_max, R, x_0, y_0, z_0, v_x_0, v_y_0, v_z_0 = np.loadtxt(fname=settings_name, unpack=False)
print(q_p)

# FFT
x_fft = np.abs(np.fft.rfft(x))                                                          # for x-axes
y_fft = np.abs(np.fft.rfft(y))                                                          # for y-axes
z_fft = np.abs(np.fft.rfft(z))                                                          # for z-axes

freq = np.fft.rfftfreq(2 * len(x_fft) - 1, (t[-1] - t[0]) / (2 * len(x_fft) - 1))       # frequency axes

x_peak_freq = freq[2 + np.argmax(x_fft[2:])]
y_peak_freq = freq[2 + np.argmax(y_fft[2:])]
z_peak_freq = freq[2 + np.argmax(z_fft[2:])]

print('X Peak Frequency =', x_peak_freq)
print('Y Peak Frequency =', y_peak_freq)
print('Z Peak Frequency =', z_peak_freq)

# make a graph
fig1 = plt.figure()
plt.plot(freq, x_fft, label='x_fft')
plt.plot(freq, y_fft, label='y_fft')
plt.plot(freq, z_fft, label='z_fft')
plt.legend(loc='best')
plt.yscale('log')
plt.xlabel('freq')
plt.grid()

fig2 = plt.figure()
plt.plot(freq, x_fft + y_fft, label='x and y fft')
plt.legend(loc='best')
plt.yscale('log')
plt.xlabel('freq')
plt.grid()

plt.show()
