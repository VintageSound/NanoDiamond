import numpy as np
import matplotlib.pyplot as plt

# Constants
A = 112.5 # kPa^-1 cm^-1
B = 2737.5 # V / (kPa cm)
pascals_per_torr = 133.322
e0 = 8.8541878128e-12

def paschen_curve(d, p_min, p_max, n_points=10000):
    p = np.linspace(p_min, p_max, n_points)
    V = B / (p * pascals_per_torr * d) * np.log(A * p * pascals_per_torr * d)
    return p, V

d = 385e-6 # Electrode distance in meters
p_min = 0.002 # Minimum pressure in Torr
p_max = 730 # Maximum pressure in Torr

p, V = paschen_curve(d, p_min, p_max)

plt.plot(p, V)
plt.xlabel('Pressure (Torr)')
plt.ylabel('Breakdown Voltage (V)')
plt.title(f'Paschen Curve for Air (d={d} m)')
plt.show()