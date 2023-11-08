import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numba import njit

# number of experimental cycle
exp_num = str(1)

# declare the physics constants
e_0 = 8.85418781762039e-12                                          # electrical constant, [m^3 kg^-1 sec^4 A^2]
mu_0 = 1.2566370614e-6                                              # vacuum permeability, [N A^-2]
g = -9.8*0                                                             # gravity acceleration, [m sec^-2]

# declare the time properties
stop_time = 10e-2*100
time_step = 1/125e6*10000
time = np.arange(0, stop_time, time_step)
print('Length of time scale =', len(time))
print('Time step =', time_step, 'sec')

# declare the grid properties for the paul ring
grid_size = 100
phi = np.linspace(0, 2*np.pi, grid_size)

# declare the particle properties
q_p = -1.602176634e-19 * 1000*3.5                                        # charge, [C]
m = 1e-15                                                         # mass, [kg]

# declare the AC field properties
AC_omega = 2 * np.pi * 300 * 1
AC_phase = np.pi / 2 * 0

# declare the paul trap properties
q_c_max = -1.602176634e-19 * 10000000                                # max charge, [C]
R = 4e-3                                                            # radius of the ring, [m]

# declare the initial conditions for the particle
x_0 = float(0)
y_0 = float(0)
z_0 = float(0)
v_x_0 = float(0.00001)
v_y_0 = float(0.00001)
v_z_0 = float(0.00001)
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


@njit
def electric_field(coord, x, y, z, t, num):
    value = float(0)
    for i in range(0, len(phi)):
        value = value + q_c(t) / (4 * np.pi * e_0) * vector_diff(coord, phi[i], num) / vector_diff_abs(x, y, z, phi[i])**3
    return value


@njit
def current(t):
    return (q_c(t + time_step) - q_c(t)) / time_step


@njit
def dx_c(angle, t):
    return R * np.cos(angle * (t + time_step)) - R * np.cos(angle * t)


@njit
def dy_c(angle, t):
    return R * np.sin(angle * (t + time_step)) - R * np.sin(angle * t)


@njit
def vector_multi(coordinate1, coordinate2, angle, t, num):
    if num == 1:
        return - vector_diff(coordinate2, angle, 3) * dy_c(angle, t)
    elif num == 2:
        return vector_diff(coordinate1, angle, 3) * dx_c(angle, t)
    elif num == 3:
        return vector_diff(coordinate1, angle, 1) * dy_c(angle, t) - vector_diff(coordinate2, angle, 2) * dx_c(angle, t)


@njit
def mag_field(co1, co2, x, y, z, t, num):
    mag_value = float(0)
    for i in range(0, len(phi)):
        mag_value = mag_value + mu_0 * current(t) / (4 * np.pi) * vector_multi(co1, co2, phi[i], t, num) / vector_diff_abs(x, y, z, phi[i])**3
    return mag_value


@njit
def ode_sol(r, t):
    x, y, z, v_x, v_y, v_z = r
    dx = v_x
    dy = v_y
    dz = v_z
    dxdt = q_p / m * (electric_field(x, x, y, z, t, 1) + v_y * mag_field(x, y, x, y, z, t, 3)*0 - v_z * mag_field(z, x, x, y, z, t, 2)*0)
    dydt = q_p / m * (electric_field(y, x, y, z, t, 2) + v_z * mag_field(y, z, x, y, z, t, 1)*0 - v_x * mag_field(x, y, x, y, z, t, 3)*0)
    dzdt = q_p / m * (electric_field(z, x, y, z, t, 3) + v_x * mag_field(z, x, x, y, z, t, 2)*0 - v_y * mag_field(y, z, x, y, z, t, 1)*0) - g
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

fig2 = plt.figure()
plt.plot(time, sol[:, 1], 'b', label='y-position_x')
plt.plot(time, sol[:, 4], 'g', label='y-velocity')
plt.legend(loc='best')
plt.xlabel('time')
plt.grid()

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
