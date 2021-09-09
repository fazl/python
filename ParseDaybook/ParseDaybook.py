# ParseDaybook
# Automate tedious and tricky adding up of hours worked

# TODO allow adding 20m worked-time like in breaks (i.e. non-ranges, durations)

# Program starts here
# ====================

# sys.argv is a list of args passed to the interpreter
# 
import fileinput
import re           # Raw strings (prefixed with r) are handy for regexps
from datetime import datetime as dt
from datetime import timedelta

# The last bit matches day names like Mon, Tue etc
DATE_PART=r"^[\t ]*2021-\d?\d-\d?\d [MTWFS][aouehr][neduit]"

# Almost identical: provides access to the date+day part like "2021-3-03 Tue"
DATE_PART_CAPTURE=r"^[\t ]*(2021-\d?\d-\d?\d [MTWFS][aouehr][neduit])"

# Matches clockin-clockout time range like 08:00-17:35
TIME_RANGE=r"[0-9]?[0-9]:[0-9][0-9]-[0-9]?[0-9]:[0-9][0-9]"

#------------------------------------------------------------------------------
# There has to be a better way than manually changing this to see debug output
def dbg(msg):
    #print(msg)
    pass #print(msg)
    
#------------------------------------------------------------------------------
#
# A dayline begins with a date stamp a bit like YYYY-mm-dd 
#
def isDayline(line):
    if re.match(DATE_PART, line):
        dbg("%s\n>> Day: %s" % ("-" * 80, line))
        return True
    return False

#------------------------------------------------------------------------------
#There must be a way to do this in python ?!
def getZeroDatetimeDelta():
    FMT = '%H:%M'
    return dt.strptime("00:00", FMT) - dt.strptime("00:00", FMT) 

#------------------------------------------------------------------------------
def dropNewlineChars(line):
    return re.sub(r"\n", "", line) 
        
#------------------------------------------------------------------------------
#
# The inOuts are time ranges like 07:53-22:35. Usually only one but 
# can have multiple ones, separated by a & (and maybe whitespace).
# We add these periods to the time worked, whereas the breaks 
# are subtracted from the time worked.
#
def parseDayLine(line):
#    print("parseDayLine(%s)" % (line))
    (inOuts, breaks) = re.split("breaks: *", line)
    dateDay = re.search(DATE_PART_CAPTURE, inOuts).group()
    inOuts = re.sub(DATE_PART, "", inOuts)        # drop date/day prefix
    breaks = re.split("=", breaks, 1)[0]          # drop any =.. 
                                                  # (eg hand calculated times)

    inOuts = re.sub(r'[ \t]+', "", inOuts)        # delete whitespace
    breaks = re.sub(r'[ \t]+', "", breaks)        # 'strip' should do this
                                                  # but python is python
    dbg(">>date/day: %s" % dateDay)
    dbg(">>inOuts: %s" % inOuts)
    dbg(">>breaks: %s" % breaks)
    
    return (dateDay, inOuts, breaks) 

#------------------------------------------------------------------------------
def timeRange2Delta(timeRange):
    dbg("timeRange2Delta(%s)-->"%timeRange)
    assert re.match(TIME_RANGE, timeRange) #eg 8:00-17:00       
    timeIn,timeOut = timeRange.split("-", 1)
    FMT = '%H:%M'
    tdelta = dt.strptime(timeOut, FMT) - dt.strptime(timeIn, FMT)
    dbg("..-->%s"%tdelta)
    if tdelta.days in [-1]:  # burning the midnight oil..
        print( "Burning the midnight oil! tdelta: %s" % tdelta )
        #tdelta.days = 0 #not allowed to change
        tdelta = timedelta(hours=tdelta.hours, minutes=tdelta.minutes)
    
    assert tdelta.days in [0]
    return tdelta

#------------------------------------------------------------------------------
def minutes2Delta(mins):
    dbg("minutes2Delta(%s)-->"%mins)
    assert re.match(r"^[1-5][0-9]$", mins) #eg 25
    mins = "00:" + (mins if len(mins)==2 else "0"+mins)
    dbg(">>minutes brk: %s" % mins)
    return timeRange2Delta("00:00-" + mins)

#------------------------------------------------------------------------------
#   
def processDay(date,inOuts,breaks):
    dbg(">>processDay() date=%s, inOuts=%s, breaks=%s" % (date, inOuts, breaks))
    inOuts = inOuts.split("&")
    workSum = getZeroDatetimeDelta()
    for inOut in inOuts:
        dbg(">>InOut: %s" % inOut)
        assert re.match(TIME_RANGE, inOut) #eg 8:00-17:00       
        tdelta = timeRange2Delta(inOut)
        dbg(">>work period: %s" % tdelta)
        workSum += tdelta
    # Probably worth documenting:
    # The breaks are either like inOuts -OR-
    # they are like 10m or 15           -OR-
    # they are like 1:40
    breaks = re.split('[+&]', breaks)
    dbg(">>eating %d breaks: %s" % (len(breaks), breaks))
    brkSum = getZeroDatetimeDelta()
    for brk in breaks:
        if re.match(TIME_RANGE, brk):               #eg 8:00-17:00
            dbg(">>range brk: %s" % brk)
            brkSum += timeRange2Delta(brk)
        elif re.match("[0-5]:[0-5][0-9]", brk):     #eg 1:25
            dbg(">>medium brk: %s" % brk)
            brkSum += timeRange2Delta(
              "00:00-" + ("0"+brk if(len(brk)<5) else brk)
            )
        elif re.match(r"^[1-5][0-9]min$", brk):     #eg 5min
            brk = re.sub("min$", "", brk)
            brkSum += minutes2Delta(brk)
        elif re.match(r"^[1-5][0-9]m$", brk):       #eg 5m
            brk = re.sub("m$", "", brk)
            brkSum += minutes2Delta(brk)
        elif re.match(r"^[1-5][0-9]$", brk):        #eg 5
            brkSum += minutes2Delta(brk)
        elif 0==len(brk):
            pass #print(">>empty brk: %s" % brk)
        else:
            print(">>WTF??: %s" % brk)
            assert False
            
    dbg("brkSum = %s" % brkSum)
    print(f">>{date}, => (billable:{workSum - brkSum})\t(worked: {workSum}) - (breaks: {brkSum})")
    
#------------------------------------------------------------------------------
def processLine(line):
    copy = dropNewlineChars(line)
#    print("LINE:%s" % copy) #when debugging

    if(isDayline(copy)):
        (date,inOuts,breaks) = parseDayLine(copy)
        processDay(date,inOuts,breaks) 
    else:
        pass #print(">>Txt:", copy)
        
              
#-----------------------------PROGRAM STARTS HERE------------------------------
for line in fileinput.input():
    processLine(line)





