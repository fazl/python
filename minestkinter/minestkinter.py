# OK lets see if we can do a crude minesweeper in python
# Hey, coding in pycharm is more fun than in text editor!
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 
import random

# GLOBALS AND CONSTANTS
# Seems python has no const or final keyword.
# Just remember never to assign to an UPPERCASE variable
# To avoid declaring one you already defined, maybe put
# all constants definitions in one place.
#
GRID_ROWS = 15
GRID_COLS = GRID_ROWS
TEXT_HIDDEN = "     "
TEXT_MARKED = "  x  "
TEXT_BOMB   = "  *  "
TEXT_MAYBE  = "  ?  "
TILE_SIZE = 20  # pixels
openedCount : int  = 0
tiles = []  # arraylist of rows, module global aids debugging


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
        self.detectedMines = 0
        self.state = TileState.HIDDEN

    def __str__(self):
        return "Tile at x=%d, y=%d, live=%s, live ngbs=%d" \
            % (self.col, self.row, self.hasMine, self.detectedMines)

    def noOp(self, event):
        zzxzz = 0 # empty body not possible, right ?

    def tileClickLeft(self, event):
        log("L-clk: " + self.__str__())
        if self.hasMine :
            #TODO
            userLost()
        else :
            if self.detectedMines == 0:
                #TODO
                openCluster(self)
            else :
                self.open() #also sets label

    def open(self):
        if not self.isOpen :
            #TODO ??also change button color to 'cleared'??
            self.isOpen = True
            self.label = str(self.detectedMines)
            self.config(text = self.label)

            #without this, the module-global variable not seen here!
            global openedCount
            openedCount += 1

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

        log("R-clk: %s (%s)" % (self.__str__(), transition))

        #Update button label to new state
        self.config(text=TileState.labels[self.state])

    def getState(self):
        return self.state
    def setState(self,state):
        self.state = state



# Seems PEP8 conventions are checked by PyCharm
# Wants two blank lines after functions.

def log(msg:str):
    status.config(text=msg)
    print (msg)

# menu handlers
#
def handleNewGame():
    log("clicked new game")
    newGame()


def handleQuit():
    log("clicked quit")
    win.destroy()

def handleHelpAbout():
    log("clicked Help|About")

def userLost():
    log("You lost!")

# basic window with title and standard controls
win = Tk.Tk()


# click event handlers
def expand(x, y, r, c):
    return "mouse(%d,%d)==grid(%d,%d)" % (x, y, r, c)


def onClick(event):
    (row, col) = mouse2grid(event.x, event.y)
    log("Clicked at %s" % expand(event.x, event.y, row, col))


def onRightClick(event):
    log("Right-clicked at x=%d,y=%d" % (event.x, event.y))


def onDrag(event):
    log("Dragged to x=%d,y=%d" % (event.x, event.y))

# x <--> column
# y <--> row
def mouse2grid(xmouse, ymouse) :
    gridX = int(xmouse / TILE_SIZE)
    gridY = int(ymouse / TILE_SIZE)
    return (gridX, gridY)

def openCluster( tile : Tile ):
    log ("TODO openCluster around tile: %s" % tile)

# Scatter mines randomly
# Example of typed arguments and return value in a function
def placeRandomMines(nMines : int, tileRows : list, mineIndexes : list) -> int:
    N = GRID_COLS*GRID_ROWS
    if N < nMines :
        raise ValueError("Can't place %d mines in %d grid tiles" % (nMines,N ))
    origMines = nMines

    mineIndexes.clear()
    for attempt in range(1, 100):
        print("Lay mines iter: %d (outstanding %d mines)..  " % (attempt, nMines))
        rCol, rRow = random.randint(0,GRID_COLS-1), random.randint(0,GRID_ROWS-1)
        tileRow = tileRows[rRow]
        tile = tileRow[rCol]
        print( "Chosen random tile: %s" % tile)

        if not tile.hasMine :
            tile.hasMine = True
            mineIndexes.append(tile)

            ngbList = getNeighbourTiles(tileRows, tile)
            for ngb in ngbList :
                dm = ngb.detectedMines
                ngb.detectedMines += 1
                if dm+1 != ngb.detectedMines :
                    raise ValueError("failed to increment detected mines!")

            print("Placed mine at (col:%d, row:%d)" % (rCol, rRow))
            nMines -= 1
            if nMines <= 0 :
                print("Success: %d mines laid in %d iterations" % (origMines, attempt))
                break
        else :
            print("\nAlready occupied: (col:%d, row:%d)\n", (rCol, rRow))

    return nMines

def getNeighbourTiles( tileRows : list, tile : Tile ) -> list :
    print("Collect ngbs of Tile:", tile)
    ngbs = []
    tRow, tCol = tile.row, tile.col
    # range has inclusive lower and exclusive upper bounds,
    # unlike randomint :(
    for dRow in range(-1,2):
        ngbRow = tRow+dRow
        if ngbRow not in range(GRID_ROWS): continue
        tileRow = tileRows[ngbRow]
        for dCol in range(-1,2):
            ngbCol = tCol + dCol
            if ngbCol not in range(GRID_COLS): continue
            ngbTile : Tile = tileRow[ngbCol]
            if ngbTile.row != ngbRow and ngbTile.col != ngbCol :
                raise ValueError(
                    "Misplaced ngb at r:%d,c:%d has row %d, col %d"
                    % (ngbRow, ngbCol,ngbTile.row, ngbTile.col)
                )
            if ngbTile != tile :
                print("\tNgb (dRow %d, dCol %d): %s" % (dRow, dCol, ngbTile)  )
                ngbs.append(ngbTile)
            else:
                print("\tSelf (dRow %d, dCol %d): %s" % (dRow, dCol, ngbTile)  )
    return ngbs


# Fill the middle frame with a grid of squares
# Some of them have a mine in them
#
def newGame():
    countMarked = 0
    countOpened = 0
    tiles.clear()
    for r in range(GRID_ROWS):
        tileRow = []    #arraylist of tiles
        for c in range(GRID_COLS):
            b = Tile(frame, c, r, TEXT_HIDDEN)
            tileRow.append(b)
            b.grid(row=r, column=c, sticky="ewns")
        tiles.append(tileRow)
    mineIndices = []
    # TODO dialog to configure game ?
    mineCount = placeRandomMines( 15, tiles, mineIndices )

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
