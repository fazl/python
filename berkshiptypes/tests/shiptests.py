from shiptypes import fewestBricks

#Test script runs here

#for n in range(10):    print(n);
#for n in range(10,0,-1):    print(n);


#fewest = fewestBricks([1,5,6,9],40)
# fewest = fewestBricks([1],40)
# assert 40 == fewest, "Expected 40, got %d [from fewestBricks([1],40)]." % fewest
#
# fewest = fewestBricks([3],7)
# assert None == fewest, "Expected None, got %d [from fewestBricks([3],7)]." % fewest

def describe(target, sizes, counts) -> str:
    assert len(sizes)==len(counts)
    ret = "Got "
    sum = 0
    for i in range(len(sizes)):
        ret += "%d*%d" % (counts[i], sizes[i]) + (" + " if i<len(sizes)-1 else "" )
        sum += counts[i] * sizes[i]
    ret += ", totals: %d" % sum
    assert target == sum
    return ret

def flatVersion():
    sizes = [9,6,5,1]
    (s0,s1,s2,s3)=(sizes[0],sizes[1],sizes[2],sizes[3])
    target = 30
    print( "target:%d, sizes: %s"%(target, sizes) )
    i0Max = int(target/s0)
    for i0 in range(i0Max,-1,-1):
        tgt0 = target-i0*s0
        print( "i%d=%d leaves %d to fill"%(0, i0, tgt0) )
        i1Max = int(tgt0/s1)
        for i1 in range(i1Max,-1,-1):
            tgt1 = tgt0-i1*s1
            print("\ti%d=%d leaves %d to fill"%(1, i1, tgt1))
            i2Max = int(tgt1/s2)
            for i2 in range(i2Max,-1,-1):
                tgt2 = tgt1-i2*s2
                print("\t\ti%d=%d leaves %d to fill"%(2, i2, tgt2))
                # No loop for i3, it either can work or not
                i3Max = int(tgt2/s3)
                tgt3 = tgt2-i3Max*s3
                print( describe(sizes,[i0,i1,i2,i3Max]) )
                if 0 != tgt3: print("Fails with remainder:", tgt3)

flatVersion()