# -*- coding: utf-8 -*-
import numpy as np
from numpy import convolve
import matplotlib.pyplot as plt

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

x = [1,2,3,4,5,6,7,8,9,10]
y = [3,5,2,4,9,1,7,5,9,1]

yMA = movingaverage(y,3)
print('yikes yMA ',yMA)

plt.plot(x[len(x)-len(yMA):],yMA)
plt.plot(x,y)
plt.show()