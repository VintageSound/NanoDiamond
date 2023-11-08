import matplotlib.pyplot as plt
import numpy as np

alfa = 0 * np.pi / 180
beta = 0 * np.pi / 180
gama = 109.5 * np.pi / 180
d = 10.5 * np.pi / 180

f_alfa = 0 * np.pi / 180
f_beta = 0 * np.pi / 180

r_0 = np.array([np.sin(alfa) * np.cos(beta),
                np.sin(alfa) * np.sin(beta),
                np.cos(alfa)])
print(np.linalg.norm(r_0))
r_1 = np.array([np.sin(alfa+gama) * np.cos(beta),
                np.sin(alfa+gama) * np.sin(beta),
                np.cos(alfa+gama)])
print(np.linalg.norm(r_1))
r_2 = np.array([np.sin(-alfa+gama) * np.cos(beta+gama+d),
                np.sin(-alfa+gama) * np.sin(beta+gama+d),
                np.cos(-alfa+gama)])
print(np.linalg.norm(r_2))
r_3 = np.array([np.sin(-alfa+gama) * np.cos(beta-gama-d),
                np.sin(-alfa+gama) * np.sin(beta-gama-d),
                np.cos(-alfa+gama)])
print(np.linalg.norm(r_3))

field = np.array([np.sin(f_alfa) * np.cos(f_beta),
                  np.sin(f_alfa) * np.sin(f_beta),
                  np.cos(f_alfa)])
"""
print(np.arccos(np.dot(r_0, field)) * 180 / np.pi)
print(np.arccos(np.dot(r_1, field)) * 180 / np.pi)
print(np.arccos(np.dot(r_2, field)) * 180 / np.pi)
print(np.arccos(np.dot(r_3, field)) * 180 / np.pi)

print(np.dot(r_0, field))
print(np.dot(r_1, field))
print(np.dot(r_2, field))
print(np.dot(r_3, field))
"""
r_0 = np.reshape(np.append(np.zeros(3), r_0), (2, 3))
r_0 = np.transpose(r_0)
r_1 = np.reshape(np.append(np.zeros(3), r_1), (2, 3))
r_1 = np.transpose(r_1)
r_2 = np.reshape(np.append(np.zeros(3), r_2), (2, 3))
r_2 = np.transpose(r_2)
r_3 = np.reshape(np.append(np.zeros(3), r_3), (2, 3))
r_3 = np.transpose(r_3)
field = np.reshape(np.append(np.zeros(3), field), (2, 3))
field = np.transpose(field)

# coordinate system
x = np.array([[0, 1], [0, 0], [0, 0]])
y = np.array([[0, 0], [0, 1], [0, 0]])
z = np.array([[0, 0], [0, 0], [0, 1]])

# plot
ax = plt.figure().add_subplot(projection='3d')

ax.plot(x[0], x[1], x[2], c='k')
ax.plot(y[0], y[1], y[2], c='k')
ax.plot(z[0], z[1], z[2], c='k')

ax.plot(r_0[0], r_0[1], r_0[2], c='tab:red')
ax.plot(r_1[0], r_1[1], r_1[2], c='tab:red')
ax.plot(r_2[0], r_2[1], r_2[2], c='tab:red')
ax.plot(r_3[0], r_3[1], r_3[2], c='tab:red')

ax.plot(field[0], field[1], field[2], c='tab:blue')

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

plt.show()