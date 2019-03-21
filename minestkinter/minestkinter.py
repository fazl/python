# OK lets see if we can do a crude minesweeper in python
# Hey, coding in pycharm is more fun than in text editor!
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 


# Seems PEP8 conventions are checked by PyCharm
# Wants two blank lines after functions.

# menu handlers
def handleNewFile():
    status.config(text="clicked File|New")


def handleOpenFile():
    status.config(text="clicked File|Open")


def handleExit():
    status.config(text="So long..")
    print("clicked menu File|Exit")
    win.destroy()


def handleHelpAbout():
    status.config(text="clicked Help|About")


# Seems python has no const or final keyword.
# Just remember never to assign to an UPPERCASE variable
# (And hope you don't redeclare one you already defined..)
#
TILE_SIZE = 20  # pixels
GRID_ROWS = 15
GRID_COLS = GRID_ROWS

# basic window with title and standard controls
win = Tk.Tk()


# click event handler
def expand(x, y, r, c):
    return "mouse(%d,%d)==grid(%d,%d)" % (x, y, r, c)


def onClick(event):
    (row, col) = mouse2grid(event.x, event.y)
    str = "Clicked at %s" % expand(event.x, event.y, row, col)
    status.config(text=str)
    print(str)


def onRightClick(event):
    print("Right-clicked at", event.x, event.y)


def onDrag(event):
    print("Dragged to ", event.x, event.y)


# x <--> column
# y <--> row
def mouse2grid(xmouse, ymouse):
    gridX = int(xmouse / TILE_SIZE)
    gridY = int(ymouse / TILE_SIZE)
    return (gridX, gridY)


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

frame = Tk.Frame(win, width=TILE_SIZE * GRID_COLS, height=TILE_SIZE * GRID_ROWS)
frame.bind("<1>", onClick)
frame.bind("<3>", onRightClick)
frame.bind("<B1-Motion>", onDrag)  # Hmm this is cool
frame.pack()

# add a status line at bottom
status = Tk.Label(win, text="", bd=1, relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")

win.mainloop()
