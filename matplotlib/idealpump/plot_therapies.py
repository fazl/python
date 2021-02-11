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
    
import json
# data = json.loads('{"one" : "1", "two" : "2", "three" : "3"}')
# print data['two']    
def readScenarioTherapies(scenarioOutFile):

  xValues = []
  yValues = []

  with open(scenarioOutFile, 'r') as f:
    #c = csv.reader(f, delimiter = ",")
    for row in f:
      row=row.strip()
      data = json.loads(row)
      tfnType = data["Type"]
      if tfnType.startswith("Delivery"):
          print( "..Skipping motor delivery record" )
          continue
      print("row: %s" % row)
      time = data["Time"]
      duration = data["Duration"]
      factor = None
      amount = None
      if tfnType.startswith("Tbf"):
        factor = data["Factor"] 
      else:
        amount = data["Amount"] 
          
      # { "Time":0,   "Type":"T1Started", "Amount": 5000, "Duration": 1800 }
      # { "Time":120, "Type":"T2Started", "Amount":7000, "Duration":2100 }
      # { "Time":360, "Type":"TbfStarted", "Factor":2000, "Duration":900}
      print( "Therapy row: t=%s, tfn=%s, dur=%sSec,%s=%s\n" %
             (time,tfnType,duration, 
              ("Amt" if factor==None else "TBF"), 
              (amount if factor==None else factor))
            )
      #force error if it cant find 3 entries
      time, ideal, real = row[0], row[1], row[2]
      xValues.append(row[0])
      yValues.append(row[1])    
  return xValues, yValues
    
# Try it:
# mS, mU = readCsv("plot.csv")
# print("Got  %s times and %s amounts" % (len(mS), len(mU)))
# assert len(mS)==len(mU), "Oops different lengths mS: %s vs mU: %s" % (len(mS), len(mU))

# Artificial setup, just to see if two arrays works
readScenarioTherapies("210210_scenario5.txt")

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
