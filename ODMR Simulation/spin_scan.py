import matplotlib.pyplot as plt
import numpy as np

# physics constants
mu_B = 1.4                      # Bohr magnetron, [MHz/G]
g_s = 2.003                     # Lande factor

# define Lorentzian parameters
freq_0 = 2870
fwhm = 4
start_freq = 2650
stop_freq = 3100
freq = np.linspace(start_freq, stop_freq, 1000)

# parameters of NV axes
alfa = 0 * np.pi / 180
beta = 0 * np.pi / 180
gama = 109.5 * np.pi / 180
d = 10.5 * np.pi / 180

# parameters of magnetic field vector
npoints = 100
f_alfa = np.linspace(0, 2*np.pi, npoints)
f_beta = np.linspace(0, 2*np.pi, npoints)
B_abs = 20                       # amplitude of magnetic field, [G]
splitting = 2 * g_s * mu_B * B_abs
print(splitting)

# calculation of NV axes vectors
r_0 = np.array([np.sin(alfa) * np.cos(beta),
                np.sin(alfa) * np.sin(beta),
                np.cos(alfa)])
r_1 = np.array([np.sin(alfa+gama) * np.cos(beta),
                np.sin(alfa+gama) * np.sin(beta),
                np.cos(alfa+gama)])
r_2 = np.array([np.sin(-alfa+gama) * np.cos(beta+gama+d),
                np.sin(-alfa+gama) * np.sin(beta+gama+d),
                np.cos(-alfa+gama)])
r_3 = np.array([np.sin(-alfa+gama) * np.cos(beta-gama-d),
                np.sin(-alfa+gama) * np.sin(beta-gama-d),
                np.cos(-alfa+gama)])


def projection(x):
    result = np.zeros((npoints, npoints))
    for i in range(0, npoints):
        for ii in range(0, npoints):
            field = np.array([np.sin(f_alfa[i]) * np.cos(f_beta[ii]),
                              np.sin(f_alfa[i]) * np.sin(f_beta[ii]),
                              np.cos(f_alfa[i])])
            result[i, ii] = np.dot(x, field)
    return result


def lorentzian(x, x0):
    return fwhm / np.pi / ((x - x0)**2 + fwhm**2)


# projections
r_0_proj = projection(r_0)
r_1_proj = projection(r_1)
r_2_proj = projection(r_2)
r_3_proj = projection(r_3)

# splittings
alfa_point = 15
beta_point = 15
r_0_minus = freq_0 - splitting * r_0_proj[alfa_point, beta_point]
r_0_plus = freq_0 + splitting * r_0_proj[alfa_point, beta_point]
r_1_minus = freq_0 - splitting * r_1_proj[alfa_point, beta_point]
r_1_plus = freq_0 + splitting * r_1_proj[alfa_point, beta_point]
r_2_minus = freq_0 - splitting * r_2_proj[alfa_point, beta_point]
r_2_plus = freq_0 + splitting * r_2_proj[alfa_point, beta_point]
r_3_minus = freq_0 - splitting * r_3_proj[alfa_point, beta_point]
r_3_plus = freq_0 + splitting * r_3_proj[alfa_point, beta_point]

# plot
"""
fig1, ax = plt.subplots(figsize=(5, 5))
ax.imshow(abs(r_0_proj))

fig2, ax = plt.subplots(figsize=(5, 5))
ax.imshow(abs(r_1_proj))

fig3, ax = plt.subplots(figsize=(5, 5))
ax.imshow(abs(r_2_proj))

fig4, ax = plt.subplots(figsize=(5, 5))
ax.imshow(abs(r_3_proj))

fig5, ax = plt.subplots(figsize=(5, 5))
ax.imshow(abs(r_0_proj)+abs(r_1_proj)+abs(r_2_proj)+abs(r_3_proj))
"""
fig6, ax = plt.subplots(figsize=(5, 5))

ax.plot(freq, lorentzian(freq, r_0_minus), label='r_0 -1')
ax.plot(freq, lorentzian(freq, r_0_plus), label='r_0 +1')
ax.plot(freq, lorentzian(freq, r_1_minus), label='r_1 -1')
ax.plot(freq, lorentzian(freq, r_1_plus), label='r_1 +1')
ax.plot(freq, lorentzian(freq, r_2_minus), label='r_2 -1')
ax.plot(freq, lorentzian(freq, r_2_plus), label='r_2 +1')
ax.plot(freq, lorentzian(freq, r_3_minus), label='r_3 -1')
ax.plot(freq, lorentzian(freq, r_3_plus), label='r_3 +1')

ax.plot(freq, lorentzian(freq, r_0_minus) + lorentzian(freq, r_0_plus) +
              lorentzian(freq, r_1_minus) + lorentzian(freq, r_1_plus) +
              lorentzian(freq, r_2_minus) + lorentzian(freq, r_2_plus) +
              lorentzian(freq, r_3_minus) + lorentzian(freq, r_3_plus), label='sum')

ax.legend(loc='best')

plt.show()