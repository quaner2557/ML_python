import numpy as np
import matplotlib.pyplot as plt

def dist(theta, v0):
    g =9.8
    rad = np.pi * theta / 180
    return  -2 * v0 ** 2 / g *(np.sin(rad)*np.cos(rad))

print(dist(50,1))

theta = np.linspace(0,90,90)
plt.plot(theta, dist(theta, 1))
plt.xlabel(r'launch angle $\theta (^{\circ})$')
plt.ylabel('horizontal distance traveled')
plt.show()

from scipy.optimize import minimize
result = minimize(dist, 40, args=(1, ))
print(result)