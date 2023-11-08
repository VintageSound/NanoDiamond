import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy import signal
from numba import njit
from ring_Capacitance import toroid_capacitance

# declare the physics constants
e_0 = 8.85418781762039e-12                                          # electrical constant, [m^3 kg^-1 sec^4 A^2]
mu_0 = 1.2566370614e-6                                              # vacuum permeability, [N A^-2]
g = -9.82                                                            # gravity acceleration, [m sec^-2]


# number of experimental cycle
exp_num = str(1)

# declare the time properties
stop_time = 10e-3*100
time_step = 1/125e6*10
fs = 1/time_step
time = np.arange(0, stop_time, time_step)
print('Length of time scale =', len(time))
print('Time step =', time_step, 'sec')

# declare the grid properties for the paul ring
grid_size = 100*2
phi = np.linspace(0, 2*np.pi, grid_size)

# declare the particle properties
q_p = -1.602176634e-19 * 5000                                   # charge, [C]
m = 1e-15 *(5000/3600)                                                        # mass, [kg]

# declare the AC field properties
AC_omega = 2 * np.pi * 1300
AC_phase = np.pi / 2 * 1

# declare the paul trap properties
R = 2.5e-3                                                            # radius of the ring, [m]
d = 0.0008                                                            # ring wire thickness, [m]
V = 6000                                                              # Voltage on the paul trap
C = toroid_capacitance(1, 2*R+2*d, d)                               # Capacitance of Ring with Radius R
print(C)
q_c_max = -C*V                                                        # max charge, [C]
q_c_max_Compare = -1.602176634e-19 * 100000000                        # max charge Dima original simulation
print(q_c_max/q_c_max_Compare)


# feedback electrodes properties
FX_omega = 2 * np.pi * 85  # Frequency for the X feedback electrode
FY_omega = 2 * np.pi * 915.8 # Frequency for the Y feedback electrode
E_x_max = 2e-0 * 0
E_y_max = 2e-0 * 0

# declare the initial conditions for the particle
x_0 = float(0)
y_0 = float(0)
z_0 = float(0)
v_x_0 = float(0.000001)
v_y_0 = float(0.000001)
v_z_0 = float(0.000001)
init_cond = [x_0, y_0, z_0, v_x_0, v_y_0, v_z_0]


# charge per calculation cell, [C]
@njit
def q_c(t):
    return q_c_max * np.sin(AC_omega * t + AC_phase) / len(phi)


@njit
def vector_diff(coordinate, angle, num):
    if num == 1:
        return coordinate - R * np.cos(angle)
    elif num == 2:
        return coordinate - R * np.sin(angle)
    elif num == 3:
        return coordinate


@njit
def vector_diff_abs(x, y, z, angle):
    return np.sqrt(vector_diff(x, angle, 1)**2 + vector_diff(y, angle, 2)**2 + z**2)


#Calculate the electric field in the particle coordinates
@njit
def electric_field(coord, x, y, z, t, num):
    value = float(0)
    for i in range(0, len(phi)):
        value = value + q_c(t) / (4 * np.pi * e_0) * vector_diff(coord, phi[i], num) / vector_diff_abs(x, y, z, phi[i])**3
    return value


@njit
def ode_sol(r, t):
    x, y, z, v_x, v_y, v_z = r
    dx = v_x
    dy = v_y
    dz = v_z
    dxdt = q_p / m * (electric_field(x, x, y, z, t, 1) + E_x_max * np.sin(FX_omega * t))
    dydt = q_p / m * (electric_field(y, x, y, z, t, 2) + E_y_max * np.sin(FY_omega * t)) + g
    dzdt = q_p / m * (electric_field(z, x, y, z, t, 3))
    return [dx, dy, dz, dxdt, dydt, dzdt]


sol = odeint(ode_sol, init_cond, time)

# save the result and the settings to 2 txt-files
data_name = str('result_') + exp_num
settings_name = str('settings_') + exp_num
settings = [q_p, m, AC_omega, q_c_max, R, x_0, y_0, z_0, v_x_0, v_y_0, v_z_0]
np.savetxt(data_name, (sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3], sol[:, 4], sol[:, 5], time))
np.savetxt(settings_name, settings)

# make a graph
fig1 = plt.figure()
plt.plot(time, sol[:, 0], 'b', label='x-position_x')
plt.plot(time, sol[:, 3], 'g', label='x-velocity')
plt.legend(loc='best')
plt.xlabel('time')
plt.grid()

fx, Pxx_den = signal.periodogram(sol[:, 0], fs=fs)
fig10 = plt.figure()
plt.semilogy(fx[1:], Pxx_den[1:])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.ylim(bottom=0.1*Pxx_den[1:].min(), top=10*Pxx_den[1:].max())
plt.xlim(left=2, right=2400)
plt.plot()


fig2 = plt.figure()
plt.plot(time, sol[:, 1], 'b', label='y-position_x')
plt.plot(time, sol[:, 4], 'g', label='y-velocity')
plt.legend(loc='best')
plt.xlabel('time')
plt.grid()

fy, Pyy_den = signal.periodogram(sol[:, 0], fs=fs)
fig20 = plt.figure()
plt.semilogy(fy[1:], Pyy_den[1:])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.ylim(bottom=0.1*Pyy_den[1:].min(), top=10*Pyy_den[1:].max())
plt.xlim(left=2, right=2400)
plt.plot()

fig3 = plt.figure()
plt.plot(time, sol[:, 2], 'b', label='z-position_x')
plt.plot(time, sol[:, 5], 'g', label='z-velocity')
plt.legend(loc='best')
plt.xlabel('time')
plt.grid()

fig4 = plt.figure()
plt.plot(sol[:, 0], sol[:, 1], 'b')
plt.plot(np.linspace(-R, R, 100), np.sqrt(R**2 - np.linspace(-R, R, 100)**2), 'g')
plt.plot(np.linspace(-R, R, 100), -np.sqrt(R**2 - np.linspace(-R, R, 100)**2), 'g')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

fig5 = plt.figure()
ax = plt.axes(projection='3d')
ax.plot(sol[:, 0], sol[:, 1], sol[:, 2], 'b')
plt.plot(np.linspace(-R, R, 100), np.sqrt(R**2 - np.linspace(-R, R, 100)**2), 'g')
plt.plot(np.linspace(-R, R, 100), -np.sqrt(R**2 - np.linspace(-R, R, 100)**2), 'g')
ax.set_zlim([-R, R])
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

plt.show()
