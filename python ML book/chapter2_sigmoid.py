# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:57:19 2016

@author: quan
"""

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

z = np.arange(-7,7, 0.1)
phi_z = sigmoid(z)
plt.plot(z,phi_z)