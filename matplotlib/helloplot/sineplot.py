# Sine curve plot program from 
# https://matplotlib.org/

import matplotlib.pyplot as plt
import numpy as np

# Clearly pyplot (plt) knows about numpy linspace objects

x = np.arange(0, 10, 0.2)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x,y)
plt.show()

