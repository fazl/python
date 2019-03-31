from shiptypes import fewestBricks

# change True to False to reduce logging output
def trace(msg:str):
    if False:
        print(msg)

def getItemCount( counts ) -> int :
    items = 0
    for i in counts:
        items += i
    return items

def describe(target, sizes, counts) -> str:
    assert len(sizes)==len(counts)
    ret = "Got "
    totLen = 0
    for i in range(len(sizes)):
        ret += "%d*%d" % (counts[i], sizes[i]) + (" + " if i<len(sizes)-1 else "" )
        totLen += counts[i] * sizes[i]
    ret += ", total len: %d" % totLen
    ret += ", items: %d" % getItemCount(counts)
    return ret

#ASSUMES sizes sorted DESCENDING
#hardcoded for array size 4
#returns list of pairs with first entry being count array, second being sum of counts
#list is sorted with best solution with smallest count at start
def generateConfigs(sizes:[], target:int) -> list:
    assert 4==len(sizes)
    (s0,s1,s2,s3)=(sizes[0],sizes[1],sizes[2],sizes[3])
    assert s3<=s2 and s2<=s1 and s1<=s0
    configs = []
    trace( "target:%d, sizes: %s"%(target, sizes) )
    i0Max = int(target/s0)
    for i0 in range(i0Max,-1,-1):
        tgt0 = target-i0*s0
        trace( "i%d=%d leaves %d to fill"%(0, i0, tgt0) )
        i1Max = int(tgt0/s1)
        for i1 in range(i1Max,-1,-1):
            tgt1 = tgt0-i1*s1
            trace("\ti%d=%d leaves %d to fill"%(1, i1, tgt1))
            i2Max = int(tgt1/s2)
            for i2 in range(i2Max,-1,-1):
                tgt2 = tgt1-i2*s2
                trace("\t\ti%d=%d leaves %d to fill"%(2, i2, tgt2))

                # No loop for i3, it either can work or not
                i3 = int(tgt2/s3)
                tgt3 = tgt2-i3*s3
                assert 0 <= tgt3
                counts = [i0, i1, i2, i3]
                if 0 == tgt3:
                    trace( "counts is %s"%counts)
                    trace( describe(target, sizes, counts) )
                    configs.append((counts, getItemCount(counts)))
                else:
                    trace( "Dropping: %s bc: %s (rem: %d)"%
                           (counts, describe(target,sizes,counts), tgt3) )
    # configs.sort(lambda x: x[1]) #sort on the second tuple element FAILS
    return sorted(configs, key=lambda x: x[1])  #smallest itemcount first



target = 30
sizes = [11,9,6,1] #must be ascending sorted
configs = generateConfigs(sizes, target)
print("Results: ")
for i in range(len(configs)) : print(configs[i])
print("Best is:", configs[0])
print(describe(target, sizes, configs[0][0]))

assert 4 == generateConfigs(sizes, target)[0][1]

(target,sizes) = (40,[9,6,5,1])
assert 6 == generateConfigs(sizes, target)[0][1]

(target,sizes) = (30,[9,6,5,1])
assert 4 == generateConfigs(sizes, target)[0][1]

(target,sizes) = (50,[10,7,3,2])
assert 5 == generateConfigs(sizes, target)[0][1]

