import csv

def readCsv(plotCsv):
    mS = []
    mU = []
    with open(plotCsv, 'r') as f:
        c = csv.reader(f, delimiter = ",")
        for row in c:
            #print("row: ", row)
            #force error if it cant find 3 entries
            time, ideal, real = row[0], row[1], row[2]
            mS.append(row[0])
            mU.append(row[1])        
    #        if row[0] == "mS":
    #            mS.append(row[1:])
    #        elif row[0] == "mU":
    #            mU.append(row[1:])

    for i in range(len(mS)):
        print("mS:%s, mU:%s" % (mS[i], mU[i]) )
    return mS, mU
    
    
# Try it:

readCsv("plot.csv")

