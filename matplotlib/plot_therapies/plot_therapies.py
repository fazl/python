# import csv
# 
# def readCsv(plotCsv):
#     xValues = []
#     yValues = []
#     with open(plotCsv, 'r') as f:
#         c = csv.reader(f, delimiter = ",")
#         for row in c:
#             #print("row: ", row)
#             #force error if it cant find 3 entries
#             time, ideal, real = row[0], row[1], row[2]
#             xValues.append(row[0])
#             yValues.append(row[1])        
#     return xValues, yValues
    
# Try it:
# mS, mU = readCsv("plot.csv")
# print("Got  %s times and %s amounts" % (len(mS), len(mU)))
# assert len(mS)==len(mU), "Oops different lengths mS: %s vs mU: %s" % (len(mS), len(mU))

# Artificial setup, just to see if two arrays works
mS = [0,2,4,6,10]
mU = [0,1,4,5,9]

import matplotlib.pyplot as plt
import numpy as np
#from my_plotter import my_plotter;

fig, ax = plt.subplots(1, 1)

plt.title('Artificial: Therapies Only')
plt.xlabel('mS')
plt.ylabel('mU')
plt.legend()

out = ax.plot(mS, mU)
plt.show()
