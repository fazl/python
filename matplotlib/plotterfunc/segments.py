# Simple plot program from 
# introductory tutorial on usage at
# https://matplotlib.org/

import matplotlib.pyplot as plt
import numpy as np

# Clearly pyplot (plt) knows about numpy linspace objects

#x = np.linspace(0, 40000, 100)
x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
#plt.plot(x, x**2, label='quadratic')
#plt.plot(x, x**3, label='cubic')

plt.xlabel('millisec')
plt.ylabel('milliunit')

plt.title("Simple Plot")

plt.legend()

plt.show()

