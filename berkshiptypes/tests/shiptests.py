from shiptypes import fewestBricks

# change True to False to reduce logging output
def trace(msg:str):
    if msg:
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

#Requires sizes sorted in descending order!
#Returns list of count arrays
#list is not sorted but you can get a sorted copy of the returned value like this:
#
#sortConfigs = sorted(generateConfigs(sizes, target), key=lambda x: getItemCount(x))
#
#this uses getItemCount() function (see above) to help sort the configs
#so the best configs are at the beginning, worst at the end
#
def generateConfigs(sizes:[], target:int, silent=False) -> list:
    if not silent:
        trace("generateConfigs(%s,%d)"%(sizes,target))
    ret = []
    if 1<len(sizes):        #Recursive case
        (size, sRest) = (sizes[0], sizes[1:])
        # print("size: %d, sRest: %s"%(size, sRest))
        assert sRest[0]<size
        for count in range(int(target / size), -1, -1):
            targetRest = target - size*count
            # trace("size %d: %d*%d leaves %d, collect subconfs using %s:" % (size,count,size,targetRest,sRest))
            assert 0<=targetRest
            for sub in generateConfigs(sRest, targetRest, silent ):
                config = [count] + sub
                #trace("Prepend %d to subconfig %s -> %s" % (count, sub, config))
                ret.append(config)
    elif 1 == len(sizes):   #Base case
        count = int(target/sizes[0])
        targetRest = target - sizes[0] * count
        if 0 == targetRest: #works
            # trace("Works: %d*%d"%(count,sizes[0]))
            ret.append([count])
        # else:               #drop
            # trace("Fails: %d (remainder: %d)"%(sizes[0],targetRest))
    else:
        raise AssertionError("generateConfig() called with empty sizes list")
    return ret

print("Results: ")
(target,sizes) = (30,[11,9,6,2]) #must be ascending sorted
configs = sorted(generateConfigs(sizes, target), key=lambda x: getItemCount(x))  #smallest itemcount first
for i in range(len(configs)) : print(configs[i],describe(target,sizes,configs[i]))
print("Best is:", configs[0])
print(describe(target, sizes, configs[0]))

# Some more tests

def testCase(expect, sizes, target):
    print("Verifying minimal shipping of %d with sizes %s is %d"%(target,sizes,expect))
    assert expect == getItemCount(
        sorted(
            generateConfigs(sizes, target, True), #silent
            key=lambda x: getItemCount(x)         #sort on number of items used
        )[0]                                      #first result
)

testCase(4, [11,9,6,2], 30)
testCase(6, [9,6,5,1],  40)
testCase(4, [9,6,5,1],  30)
testCase(5, [10,7,3,2], 50)
testCase(11,[5, 3, 1],  53)
testCase(10,[5,1],      50)
testCase(10,[5],        50)
