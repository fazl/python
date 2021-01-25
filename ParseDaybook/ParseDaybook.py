# ParseDaybook
# Automate tedious adding up of hours worked

try:
    import tkinter as Tk  ## python3: tkinter
    import tkinter.messagebox as messagebox    # stackoverflow.com/a/38181986
except ImportError:
    import Tkinter as Tk  ## python2: tkinter
    import tkMessageBox as messagebox
import random

# Program starts here
# ====================

# sys.argv is a list of args passed to the interpreter
# 
import fileinput
import re           # Raw strings (prefixed with r) are handy for regexps

DATE_PART=r"^[\t ]*2021-\d?\d-\d?\d [MTWFS][aouehr][neduit]"
DATE_PART_CAPTURE=r"^[\t ]*(2021-\d?\d-\d?\d [MTWFS][aouehr][neduit])"
TIME_RANGE=r"[0-9]?[0-9]:[0-9][0-9]-[0-9]?[0-9]:[0-9][0-9]"

#------------------------------------------------------------------------------
def log(msg):
    pass #print(msg)
    
#------------------------------------------------------------------------------
#
# A dayline begins with a date stamp a bit like YYYY-mm-dd 
#
def isDayline(line):
    if re.match(DATE_PART, line):
        log("%s\n>> Day: %s" % ("-" * 80, line))
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
# can have multiple ones, separated by a & and whitespace.
# We add these periods to the time worked, whereas the breaks 
# are subtracted from the time worked.
#
def parseDayLine(line):
#    print("parseDayLine(%s)" % (line))
    (inOuts, breaks) = re.split("breaks: *", line)
    dateDay = re.search(DATE_PART_CAPTURE, inOuts).group()  # capture the date/day
    inOuts = re.sub(DATE_PART, "", inOuts)        # drop date/day prefix
    breaks = re.split("=", breaks, 1)[0]          # drop any =.. calcuated times

    inOuts = re.sub(r'[ \t]+', "", inOuts)        # delete whitespace
    breaks = re.sub(r'[ \t]+', "", breaks)        # delete whitespace
    #print(">>date/day: %s" % dateDay)
    #print(">>inOuts: %s" % inOuts)
    #print(">>breaks: %s" % breaks)
    
    return (dateDay, inOuts, breaks) 

#------------------------------------------------------------------------------
def timeRange2Delta(timeRange):
    log("timeRange2Delta(%s)-->"%timeRange)
    assert re.match(TIME_RANGE, timeRange) #eg 8:00-17:00       
    timeIn,timeOut = timeRange.split("-", 1)
    FMT = '%H:%M'
    tdelta = dt.strptime(timeOut, FMT) - dt.strptime(timeIn, FMT)
    log("..-->%s"%tdelta)
    assert tdelta.days == 0
    return tdelta

#------------------------------------------------------------------------------
def minutes2Delta(mins):
    log("minutes2Delta(%s)-->"%mins)
    assert re.match(r"^[1-5][0-9]$", mins) #eg 25
    mins = "00:" + (mins if len(mins)==2 else "0"+mins)
    log(">>minutes brk: %s" % mins)
    return timeRange2Delta("00:00-" + mins)

#------------------------------------------------------------------------------
# TODO Use a datetime 
#   
from datetime import datetime as dt
def processDay(date,inOuts,breaks):
    log(">>processDay() date=%s, inOuts=%s, breaks=%s" % (date, inOuts, breaks))
    inOuts = inOuts.split("&")
    workSum = getZeroDatetimeDelta()
    for inOut in inOuts:
        log(">>InOut: %s" % inOut)
        assert re.match(TIME_RANGE, inOut) #eg 8:00-17:00       
        tdelta = timeRange2Delta(inOut)
        log(">>work period: %s" % tdelta)
        workSum += tdelta
    # 
    # The breaks are either like inOuts -OR-
    # they are like 10m or like 1:40
    breaks = re.split('[+&]', breaks)
    log(">>eating %d breaks: %s" % (len(breaks), breaks))
    brkSum = getZeroDatetimeDelta()
    for brk in breaks:
        if re.match(TIME_RANGE, brk):           #eg 8:00-17:00
            log(">>range brk: %s" % brk)
            brkSum += timeRange2Delta(brk)
        elif re.match("[0-5]:[0-5][0-9]", brk): #eg 1:25
            log(">>medium brk: %s" % brk)
            brkSum += timeRange2Delta(
              "00:00-" + ("0"+brk if(len(brk)<5) else brk)
            )
        elif re.match(r"^[1-5][0-9]min$", brk):  #eg 5min
            brk = re.sub("min$", "", brk)
            brkSum += minutes2Delta(brk)
        elif re.match(r"^[1-5][0-9]m$", brk):    #eg 5m
            brk = re.sub("m$", "", brk)
            brkSum += minutes2Delta(brk)
        elif re.match(r"^[1-5][0-9]$", brk):    #eg 5
            brkSum += minutes2Delta(brk)
        elif 0==len(brk):
            pass #print(">>empty brk: %s" % brk)
        else:
            print(">>WTF??: %s" % brk)
            assert False
            
    log("brkSum = %s" % brkSum)
    print(">>%s, (worked: %s) - (breaks: %s) => (billable:%s)" % 
          (date, workSum, brkSum, workSum - brkSum))
        
        
    

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





