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
#
# A dayline begins with a date stamp a bit like YYYY-mm-dd 
#
def isDayline(line):
    if re.match(DATE_PART, line):
        print("%s\n>> Day: %s" % ("-" * 80, line))
        return True
    return False

#
# The inOuts are time ranges like 07:53-22:35. Usually only one but 
# can have multiple ones, separated by a & and whitespace.
# We add these periods to the time worked, whereas the breaks 
# are subtracted from the time worked.
#
def parseInOuts(line):
#    print("parseInOuts(%s)" % (line))
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


# TODO Use a datetime 
#   
from datetime import datetime as dt
def processDayline(date,inOuts,breaks):
    print(">>processDayline() date=%s, inOuts=%s, breaks=%s" % (date, inOuts, breaks))
    inOuts = inOuts.split("&")
    for inOut in inOuts:
        print(">>InOut: %s" % inOut)
        assert re.match(r"[-:0-9]+", inOut) # 08:00-17:00       
        timeIn,timeOut = inOut.split("-", 1)
        FMT = '%H:%M'
        tdelta = dt.strptime(timeOut, FMT) - dt.strptime(timeIn, FMT)
        assert tdelta.days == 0
        print(">>worktime: %s" % tdelta)
    

        
        
def processLine(line):
    copy = re.sub(r"\n", "", line) #erase any newlines
#    print("LINE:%s" % copy) #when debugging

    if(isDayline(copy)):
#        print("LINE:%s" % copy) #when debugging
        (date,inOuts,breaks) = parseInOuts(copy)
        processDayline(date,inOuts,breaks) 
    else:
        pass #print(">>Txt:", copy)
        
        
       

for line in fileinput.input():
    processLine(line)





