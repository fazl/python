import json 
from collections import deque 

pendings=deque()

#==============================================================================
# returns
# - chopAmount = pro-rata amount of therapy (up to time given)
# - "chopped therapy":
#   o starting at time given and
#   o remaining amount and duration (after time given)
#
def chopPending( tFn, t ):
    time     = tFn[0]
    duration = tFn[1]
    name     = tFn[2]
    amount   = tFn[3]
    chopDuration = t - time
    chopAmount = (chopDuration * amount)/duration

    leftAmount = amount - chopAmount
    assert 0<=leftAmount

    leftDuration = duration - chopDuration
    assert 0<=leftDuration

    print("chopPending.. chop %s@%ss:{%.7sMU over [%s->+%s)s}->"
          "{%.7smU over (%s->%s)s},{%.7sMU over [%s->+%s)s}" % 
           (name,t,  amount,time,duration, 
            chopAmount,time,t, leftAmount,t,leftDuration))

    return chopAmount,(t,leftDuration,name,leftAmount)

#==============================================================================
# Consume therapy started record and potentially output datapoint(s) to plot
# based on merging pro-rata amounts from any pending therapies the new
# therapy starts partway into.
# Maintains a stack of pending therapies for this purpose.
# 
def eatTfn( time,duration,name,amount ):
    #
    # Case: No pendings
    #
    if 0 == len(pendings):
        print("eatTfn..first therapy %s (%s->+%ss: %smU)" %
              (name,time,duration,amount))
        pendings.append((time,duration,name,amount)) 
        return
    #
    # Case: Pendings exist
    #
    
    # Require new records don't precede those seen earlier!
    assert pendings[0][0] <= time

    #
    # Case: New record starts same time as pendings 
    #       (Can happen. Just add another pending.)
    #
    if pendings[0][0] == time :
        print("eatTfn.. case new tfn %s (%s->+%s]s starts same time as pendings"%
              (name,time,duration)) 
        #poor python paupers cant afford a push method
        pendings.append((time,duration,name,amount)) 
        return
        
#==============================================================================

    #
    # Case: New record starts later than pendings 
    #       (More usual. Chop pendings, usually where new Tfn starts.)
    #
    print("eatTfn.. case chop: %s %s->+%ss: %smU (starts after pendings) " % 
          (name,time,duration,amount))
    # Does any pending finish before new start time?
    if any( p[0]+p[1] < time for p in pendings ):
        print( "eatTfn.. OOPs! handle 'pendings end before new %s starts'" % name)
    else:
        print("eatTfn.. chop %d pendings at %ss (none end before new start) "% 
              (len(pendings),time))

        #new chunk: start=existing start, duration=(time - start)
        chunkStart = pendings[0][0]
        chunkDuration = time-chunkStart
        chunkAmount = 0
        # chopping can remove used up pending therapies
        tmpPendings=deque() 
        while 0<len(pendings):
            firstPending = pendings.popleft()
            (chopAmount,choppedPending) = chopPending( firstPending, time )
            chunkAmount += chopAmount
            #drop pending if duration or amount is used up 
            if not (0 in [choppedPending[1],choppedPending[-1]]): 
                tmpPendings.append(choppedPending)
            else:
                print("Drop pending %s chopped to %s" % (firstPending,choppedPending) );
        print("plot %.7smU from %ss to %ss "% (chunkAmount,chunkStart, chunkStart+chunkDuration))  
        pendings.extend( tmpPendings )
        pendings.append((time,duration,name,amount)) 

#==============================================================================
def handleMotorDelivery(data, values):
        pass
        #print( "..Skipping Motor delivery record" )

#==============================================================================
# Entry point for plotting ideal curve.
# Calls eatTfn() to eat a therapy started record.
# Need to figure out how to handle tbf started events.
#
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
        eatTfn( time,duration,tfnType,amount )
            
    # { "Time":0,   "Type":"T1Started", "Amount": 5000, "Duration": 1800 }
    # { "Time":120, "Type":"T2Started", "Amount":7000, "Duration":2100 }
    # { "Time":360, "Type":"TbfStarted", "Factor":2000, "Duration":900}
#   print( "Therapy %s at %s s, dur=%sSec,%s=%s\n" %
#          (tfnType,time,duration, 
#           ("Amt" if factor==None else "TBF"), 
#           (amount if factor==None else factor))
#         )
    #force error if it cant find 3 entries

#==============================================================================
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
