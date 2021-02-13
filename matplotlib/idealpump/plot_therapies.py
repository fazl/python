import json
from collections import deque
pendings=deque()

# return the amount of therapy i up to time given
# also reduce its amount by this
# also reduce its duration and increase its start to time
def chopPending( pends, i, time ):
  tFn = pends[i]
  tFnTime     = tFn[0]
  tFnDuration = tFn[1]
  tFnType     = tFn[2]
  tFnAmount   = tFn[3]
  chopDuration = time - tFnTime
  chopAmount = (chopDuration * tFnAmount)/tFnDuration
  leftAmount = tFnAmount - chopAmount
  assert 0<=leftAmount
  leftDuration = tFnDuration - chopDuration
  assert 0<=leftDuration
  print("chopPending.. chop %s at %sS, was %sMU over (%s->+%s);  %.7smU from %s->%sS, leaves %.7sMU over (%s->+%s) " % 
         (tFnType, time,tFnAmount,tFnTime,tFnDuration,chopAmount,tFnTime,time, leftAmount,time,leftDuration))
  # update record before leaving here
  pends[i] = (time,leftDuration,tFnType,leftAmount)
  #tFn[0]=time     
  #tFn[1]=leftDuration 
  #tFn[3]=leftAmount   

  return chopAmount

def eat( time,duration,tfnType,amount ):
  if 0 != len(pendings):
    #print("eat.. we have pendings")
    assert pendings[0][0] <= time
    if pendings[0][0] == time :
      print("eat..new pending: startTime %s->+%s identical to pending therapies"%(time,duration)) 
      #python paupers cant afford a push method
      pendings.append((time,duration,tfnType,amount)) 
    else:
      print("eat.. chop/pop: new pending: startTime %s->+%s later than pending therapies" % (time,duration))
      # Does any pending finish before new start time?
      if any( p[0]+p[1] < time for p in pendings ):
        print( "eat.. OOPs! new %s starts after at least one pending ended!! please handle." % tfnType)
      else:
        print("eat.. no pending finishes before new one starts; chop at new start %s"% time)
        #new chunk starts at existing start, duration is time - existing time
        chunkStart = pendings[0][0]
        chunkDuration = time-chunkStart
        chunkAmount = 0
        for i in range(len(pendings)):
          chopAmount = chopPending( pendings, i, time )
          chunkAmount += chopAmount
        print("plot %.7smU from %ss to %ss "% (chunkAmount,chunkStart, chunkStart+chunkDuration))  
        
      
  else: 
      print("therapy %s is first pending starting at %s->+%s" %(tfnType,time,duration))
      pendings.append((time,duration,tfnType,amount)) 

def handleMotorDelivery(data, values):
    pass
    #print( "..Skipping Motor delivery record" )

def handleTherapyStart(data, values):
  tfnType = data["Type"]
  time = data["Time"]
  duration = 55 if tfnType.startswith("Bolus") else data["Duration"]
  factor = None
  amount = None
  if tfnType.startswith("Tbf"):
    factor = data["Factor"] 
    values.append( (time,duration,tfnType,factor) )
  else:
    amount = data["Amount"] 
    values.append( (time,duration,tfnType,amount) )
    eat( time,duration,tfnType,amount )
      
  # { "Time":0,   "Type":"T1Started", "Amount": 5000, "Duration": 1800 }
  # { "Time":120, "Type":"T2Started", "Amount":7000, "Duration":2100 }
  # { "Time":360, "Type":"TbfStarted", "Factor":2000, "Duration":900}
#   print( "Therapy %s at %s s, dur=%sSec,%s=%s\n" %
#          (tfnType,time,duration, 
#           ("Amt" if factor==None else "TBF"), 
#           (amount if factor==None else factor))
#         )
  #force error if it cant find 3 entries

def readScenarioTherapies(scenarioOutFile):
  motorValues = []
  therapyValues = []
  with open(scenarioOutFile, 'r') as f:
    for row in f:
      row=row.strip()
      data = json.loads(row)
      tfnType = data["Type"]
      if tfnType.endswith("Finished"):
        #print( "..Skipping therapy Finished record" )
        continue
      #print("row: %s" % row)
      if tfnType.startswith("Delivery"):
        handleMotorDelivery(data, motorValues)
      else:
        handleTherapyStart(data, therapyValues)

  return therapyValues
    
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
