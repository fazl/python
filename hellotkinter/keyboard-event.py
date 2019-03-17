# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

# For Python2 need uppercase T i.e. Tkinter 
#
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 

# To invoke this listener needs two pre-requisites:
# 1) connect function to event using bind()
# 2) keyboard events will pass to widget that has focus
#
def onKeyPress(event):
    print( "pressed", repr(event.char) )

# basic window with title and standard controls
win = Tk.Tk() # won't accept args width=200, height=200 


# click event handler
def onClick(event):
    print( "Clicked at", event.x, event.y )

# Can we do this directly on a window ?
#
frame = Tk.Frame( win, width=200, height=200 )

frame.bind("<Button-1>", onClick)
frame.bind("<Key>", onKeyPress)
frame.pack()
frame.focus_set()  # Doh, why not setFocus() ?!

win.mainloop()

