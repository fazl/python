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

def onDrag(event):
    print( "Dragged to ", event.x, event.y )


# Can we do this directly on a window ? Ans: NO.
#
# <Button-1> = left click  (or <ButtonPress-1> or just <1>)
# <Button-2> = middle click
# <Button-3> = right click
# <B1-Motion> = left drag
# <ButtonRelease-1> = left button released
# <DoubleButton-1> = left button double-clicked
# <TripleButton-1> = left button triple-clicked
# <Enter/Leave> = mouse pointer entered/left widget
# <Return> = keyboard 'Enter' key pressed with widget focused
# .. and lots of other standard keys..
#
# Can s/Button/ButtonPress/ or s/Button-//
#
frame = Tk.Frame( win, width=200, height=200 )
frame.bind("<1>", onClick)
frame.bind("<3>", onRightClick)
frame.bind("<B1-Motion>", onDrag)  #Hmm this is cool
frame.pack()

win.mainloop()

