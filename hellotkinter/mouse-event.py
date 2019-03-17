# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

# For Python2 need uppercase T i.e. Tkinter 
#
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 

# basic window with title and standard controls
win = Tk.Tk() # won't accept args width=200, height=200 


# click event handler
def onClick(event):
    print( "Clicked at", event.x, event.y )

def onRightClick(event):
    print( "Right-clicked at", event.x, event.y )


# Can we do this directly on a window ? Ans: NO.
#
# <Button-1> = left click  (or <ButtonPress-1> or just <1>)
# <Button-2> = middle click
# <Button-3> = right click
#
# Can s/Button/ButtonPress/ or s/Button-//
#
frame = Tk.Frame( win, width=200, height=200 )
frame.bind("<1>", onClick)
frame.bind("<3>", onRightClick)
frame.pack()

win.mainloop()

