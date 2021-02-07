import matplotlib.pyplot as plt
import numpy as np

from my_plotter import my_plotter;

data1, data2, data3, data4 = np.random.randn(4, 100)
fig, ax = plt.subplots(1, 1)
my_plotter(ax, data1, data2, {'marker': 'x'})
plt.show()
