# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

# For Python2 need uppercase T i.e. Tkinter 
#
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 

# basic window with title and standard controls
# (there must be a way to set title)
win = Tk.Tk()


# click event handler
def onClick(event):
    print( "Clicked at", event.x, event.y )


# Can we do this directly on a window ?
#
frame = Tk.Frame( win, width=200, height=200 )
frame.bind("<Button-1>", onClick)
frame.pack()

win.mainloop()

