import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from numba import njit

# number of experimental cycle
exp_num = str(1)

# declare the physics constants
e_0 = 8.85418781762039e-12                                          # electrical constant, [m^3 kg^-1 sec^4 A^2]
mu_0 = 1.2566370614e-6                                              # vacuum permeability, [N A^-2]
g = -9.8                                                            # gravity acceleration, [m sec^-2]

# declare the time properties
stop_time = 10e-2*100
time_step = 1/125e6*1000
time = np.arange(0, stop_time, time_step)
print('Length of time scale =', len(time))
print('Time step =', time_step, 'sec')

# declare the grid properties for the paul ring
grid_size = 100*2
phi = np.linspace(0, 2*np.pi, grid_size)

# declare the particle properties
q_p = -1.602176634e-19 * 10*160*2                                    # charge, [C]
m = 1e-15                                                           # mass, [kg]

# declare the AC field properties
AC_omega = 2 * np.pi * 1000
AC_phase = np.pi / 2 * 1

# declare the paul trap properties
q_c_max = -1.602176634e-19 * 100000000                                # max charge, [C]
R = 2e-3                                                            # radius of the ring, [m]
ring_z = 2e-3                                                       # z coordinate of paul trap ring
wire_x = R / np.sqrt(2)                                             # x coordinate of wire
wire_y = -R / np.sqrt(2)                                            # y coordinate of wire
npoints = 100                                                       # number of point in the wire
wire_z = np.linspace(-ring_z, ring_z, npoints)              # z coordinates of the wire

# feedback electrodes properties
FX_omega = 2 * np.pi * 85
FY_omega = 2 * np.pi * 915.8
E_x_max = 2e-0 * 0
E_y_max = 2e-0 * 1

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
def vector_diff(coordinate, angle, num, z_pos):
    if num == 1:
        return coordinate - R * np.cos(angle)
    elif num == 2:
        return coordinate - R * np.sin(angle)
    elif num == 3:
        return coordinate - ring_z * z_pos                  # z_pos is either 1 or -1 (for each ring)

@njit
def vector_diff_2(coordinate, num, i):   # more convenient for the wire calculation
    if num == 1:
        return coordinate - wire_x
    elif num == 2:
        return coordinate - wire_y
    elif num == 3:
        return coordinate - wire_z[i]

@njit
def vector_diff_abs(x, y, z, angle, z_pos):
    return np.sqrt(vector_diff(x, angle, 1, 1)**2 + vector_diff(y, angle, 2, 1)**2 + (z - ring_z * z_pos)**2)

@njit
def vector_diff_abs_2(x, y, z, i):   # more convenient for the wire calculation
    return np.sqrt(vector_diff_2(x, 1, i)**2 + vector_diff_2(y, 2, i)**2 + (z - wire_z[i])**2)

@njit
def electric_field(coord, x, y, z, t, num):
    value = float(0)
    for i in range(0, len(phi)):
        value = value + q_c(t) / (4 * np.pi * e_0) * vector_diff(coord, phi[i], num, 1) / vector_diff_abs(x, y, z, phi[i], 1)**3
        value = value + q_c(t) / (4 * np.pi * e_0) * vector_diff(coord, phi[i], num, -1) / vector_diff_abs(x, y, z, phi[i], -1) ** 3
    for i in range(0, len(wire_z)):
        value = value + (2 * ring_z * q_c(t) / (2 * np.pi * R * npoints)) / (4 * np.pi * e_0) * vector_diff_2(coord, num, i) / vector_diff_abs_2(x, y, z, i) ** 3
    return value


@njit
def ode_sol(r, t):
    x, y, z, v_x, v_y, v_z = r
    dx = v_x
    dy = v_y
    dz = v_z
    dxdt = q_p / m * electric_field(x, x, y, z, t, 1)
    dydt = q_p / m * electric_field(y, x, y, z, t, 2) + g
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
plt.plot(np.linspace(-R, R, 100), np.sqrt(R**2 - np.linspace(-R, R, 100)**2), ring_z * np.ones(100), 'g')
plt.plot(np.linspace(-R, R, 100), -np.sqrt(R**2 - np.linspace(-R, R, 100)**2), ring_z * np.ones(100), 'g')
plt.plot(np.linspace(-R, R, 100), np.sqrt(R**2 - np.linspace(-R, R, 100)**2), -ring_z * np.ones(100), 'g')
plt.plot(np.linspace(-R, R, 100), -np.sqrt(R**2 - np.linspace(-R, R, 100)**2), -ring_z * np.ones(100), 'g')
plt.plot(wire_x * np.ones(100), wire_y * np.ones(100), np.linspace(-ring_z, ring_z, 100), 'g')
ax.set_zlim([-R, R])
plt.xlabel('x')
plt.ylabel('y')
plt.grid()

plt.show()