import numpy as np
import matplotlib.pyplot as plt
from scipy.special import dawsn
import quamash
import pyrpl

r = pyrpl.RedPitaya()
# Constants
cs = 3e8  # Speed of light in m/s
ns = 1.33  # Refractive index of the solvent
l0 = 1.064e-6  # Wavelength in meters

# Parameters
a = 0.25e-6  # Particle radius in meters
w0 = 0.53e-3  # Beam waist radius in meters

# Calculate uniform-field polarizability
nr = ns +0.01 # Relative refractive index
d = 2 * a  # Particle diameter
alpha = (a**3 * nr**2) / (ns**2 * (nr**2 - ns**2))  # Uniform-field polarizability

# Calculate response function Gs(x, y, w0)
def response_function(x, y, w0):
    arg = 2 * x**2 / (w0**2)
    Gs = dawsn(np.sqrt(arg)) * np.exp(-arg)
    return Gs

# Calculate intensity modulation
def calculate_intensity_modulation(x, y, w0, Itot):
    Gs = response_function(x, y, w0)
    intensity_modulation = (2 * np.pi * cs * alpha * Itot * Gs) / (w0**4)
    return intensity_modulation

# Generate displacement values for x and y
x_values = np.linspace(-0.5 * w0, 0.5 * w0, 100)
y_values = np.linspace(-0.5 * w0, 0.5 * w0, 100)

# Calculate intensity modulation for each displacement
intensity_modulations = []
for y in y_values:
    intensity_row = []
    for x in x_values:
        intensity = calculate_intensity_modulation(x, y, w0, 1.0)
        intensity_row.append(intensity)
    intensity_modulations.append(intensity_row)

# Convert intensity modulation to dB scale for visualization
intensity_modulations_dB = 10 * np.log10(intensity_modulations)

# Plot intensity modulation in dB scale
plt.imshow(intensity_modulations_dB, extent=[-0.5 * w0, 0.5 * w0, -0.5 * w0, 0.5 * w0], origin='lower', aspect='auto')
plt.colorbar(label='Intensity Modulation (dB)')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Intensity Modulation in dB')
plt.show()