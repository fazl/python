# OK lets see if we can do a crude minesweeper in python
# Hey, coding in pycharm is more fun than in text editor!
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 
import random

TEXT_HIDDEN = "     "
TEXT_MARKED = "  x  "
TEXT_BOMB   = "  *  "
TEXT_MAYBE  = "  ?  "


class TileState():
    HIDDEN, MARKED, BOMB, MAYBE = range(0, 4)
    labels={
        BOMB   : TEXT_BOMB,
        HIDDEN : TEXT_HIDDEN,
        MARKED : TEXT_MARKED,
        MAYBE  : TEXT_MAYBE
    }

class Tile(Tk.Button):
    def __init__(self, master, col, row, label):
        Tk.Button.__init__(self, master, text=label)
        self.bind("<1>", self.tileClickLeft)
        self.bind("<3>", self.tileClickRight)
        self.col = col
        self.row = row
        self.isOpen = False
        self.hasMine = False
        self.label = label
        # self.detectedMines = 0
        self.state = TileState.HIDDEN

    def __str__(self):
        return "Tile at col=%d, row=%d hasMine=%s" \
            % (self.col, self.row, self.hasMine)

    def noOp(self, event):
        zzxzz = 0 # empty body not possible, right ?

    def tileClickLeft(self, event):
        #TODO simplify using __str__
        str = "L-clk: Tile at col=%d, row=%d hasMine=%s" \
            % (self.col, self.row, self.hasMine)
        status.config(text=str)
        print(str)

    # Cycle the label "" -> X -> ? -> ""
    # Disable left clicks for X and ? states
    # to protect against accidentally triggering mine
    def tileClickRight(self, event):
        transition = ""
        if self.state == TileState.HIDDEN:
            self.state = TileState.MARKED
            self.bind("<1>", self.noOp)
            self.config(state = "disabled")
            transition = "state->MARKED"
        elif self.state == TileState.MARKED:
            self.state = TileState.MAYBE
            self.bind("<1>", self.noOp)
            self.config(state = "disabled")
            transition = "state->MAYBE"
        elif self.state == TileState.MAYBE:
            self.state = TileState.HIDDEN
            transition = "state->HIDDEN"
            self.bind("<1>", self.tileClickLeft)
            self.config(state = "normal")
        else:
            raise AssertionError("row=%d,col=%d, unexpected state %s"%(self.row, self.col, self.state))

        str = "R-clk: Tile at col=%d, row=%d hasMine=%s (%s)" \
            % (self.col, self.row, self.hasMine, transition)
        status.config(text=str)
        print(str)

        #Update button label to new state
        self.config(text=TileState.labels[self.state])

    def getState(self):
        return self.state
    def setState(self,state):
        self.state = state



# Seems PEP8 conventions are checked by PyCharm
# Wants two blank lines after functions.

# menu handlers
#
def handleNewGame():
    str="clicked new game"
    status.config(text=str)
    print (str)
    newGame()


def handleQuit():
    str="clicked quit"
    status.config(text=str)
    print (str)
    win.destroy()

def handleHelpAbout():
    status.config(text="clicked Help|About")

# CONSTANTS
# Seems python has no const or final keyword.
# Just remember never to assign to an UPPERCASE variable
# To avoid declaring one you already defined, maybe put
# all constants definitions in one place.
#
TILE_SIZE = 20  # pixels
GRID_ROWS = 15
GRID_COLS = GRID_ROWS
firstTime = True
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
def mouse2grid(xmouse, ymouse) :
    gridX = int(xmouse / TILE_SIZE)
    gridY = int(ymouse / TILE_SIZE)
    return (gridX, gridY)

# Scatter mines randomly
# Example of typed arguments and return value in a function
def placeRandomMines(nMines : int, tileRows : list, bombIndexes : list ) -> int:
    N = GRID_COLS*GRID_ROWS
    if N < nMines :
        raise ValueError("Can't place %d mines in %d grid tiles" % (nMines,N ))
    origMines = nMines

    bombIndexes.clear()
    for attempt in range(1, 100):
        print("Lay mines iter: %d (outstanding %d mines)..  ", attempt, nMines)
        rCol, rRow = random.randint(0,GRID_COLS-1), random.randint(0,GRID_ROWS-1)
        tileRow = tileRows[rRow]
        tile = tileRow[rCol]
        print( "Chosen random tile: %s" % tile)
        # TODO continue work ..
    return nMines




# Fill the middle frame with a grid of squares
# Some of them have a mine in them
#
def newGame():
    countMarked = 0
    countOpened = 0
    tiles = []          #arraylist of rows
    for r in range(0, GRID_ROWS):
        tileRow = []    #arraylist of tiles
        for c in range(0,GRID_COLS):
            b = Tile(frame, c, r, TEXT_HIDDEN)
            tileRow.append(b)
            b.grid(row=r, column=c, sticky="ewns")
        tiles.append(tileRow)
    bombIndices = []
    mineCount = placeRandomMines( 15, tiles, bombIndices )

# I guess main starts here..

# just some buttons in a frame parked at the top, for a toolbar
# instead of text=".." can use image= for which you can load
# an image from disk using PhotoImage constructor.
toolbar = Tk.Frame( win )
b = Tk.Button(toolbar, text="new game", command=handleNewGame)
b.pack(side="left", padx=2, pady=2)

b = Tk.Button(toolbar, text="TODO use images!", command=handleQuit)
b.pack(side="left", padx=2, pady=2)

b = Tk.Button(toolbar, text="quit", command=handleQuit)
b.pack(side="right", padx=2, pady=2)

toolbar.pack(side="top", fill="x")

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
# TODO remove mouse handling for frame unless needed ?
#
frame = Tk.Frame(win, width=TILE_SIZE * GRID_COLS, height=TILE_SIZE * GRID_ROWS)
frame.bind("<1>", onClick)
frame.bind("<3>", onRightClick)
# frame.bind("<B1-Motion>", onDrag)  # Hmm this is cool
frame.pack()

#

# add a status line at bottom
status = Tk.Label(win, text="", bd=1, relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")
newGame()

win.mainloop()
