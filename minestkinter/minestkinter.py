# OK lets see if we can do a crude minesweeper in python
# Hey, coding in pycharm is more fun than in text editor!
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 
import random

## SUMMARY OF IDEAS FOR IMPROVEMENTS, EASY TO HARD
#  TODO dialogs on winning / losing should be trivial
#  TODO could display running totals in status line ??
#  TODO dialog to configure game ?
#  TODO add keyboard navigation should be straightforward
#  TODO use images in buttons



# GLOBALS AND CONSTANTS
# Seems python has no const or final keyword.
# Must simply never assign to an UPPERCASE variable more than once
# To help prevent redeclaring one you already defined, maybe put
# all constants definitions in one place.
#
COLOR_DEAD   = "red"
COLOR_HIDDEN = "darkgrey"
COLOR_MARKED = "black"
COLOR_OPEN   = "lightgrey"
DEATH_CROSS = '\u2620'      #skull & crossbones symbol
GRID_ROWS = 15
GRID_COLS = GRID_ROWS
TEXT_HIDDEN = "     "
TEXT_MARKED = "  x  "
TEXT_BOMB   = "  *  "
TEXT_MAYBE  = "  ?  "
TILE_SIZE = 20  # pixels
#TODO could display running totals in status line ??
clearedCount : int  = 0
markedCount : int  = 0
tiles = []  # arraylist of rows, module global aids debugging
frame : Tk.Frame = None


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
        Tk.Button.__init__(self, master, text=label, bg=COLOR_HIDDEN, disabledforeground=COLOR_MARKED)
        self.bind("<1>", self.tileClickLeft)
        self.bind("<3>", self.tileClickRight)
        self.col = col
        self.row = row
        self.isOpen = False
        self.hasMine = False
        self.label = label
        self.detectedMines = 0
        self.state = TileState.HIDDEN

    def setLabel(self, lbl) :
        self.config(text=lbl)
        self.label = lbl

    def __str__(self):
        return "Tile at x=%d, y=%d, live=%s, live ngbs=%d" \
            % (self.col, self.row, self.hasMine, self.detectedMines)

    def noOp(self, event):
        zzxzz = 0 # empty body not possible, right ?

    def tileClickLeft(self, event):
        # log("L-clk: " + self.__str__())
        if self.hasMine :
            self.userLost()
        else :
            if self.detectedMines == 0:
                self.openCluster()
            else :
                self.open() #also sets label

    def userLost(self):
        log("You're DEAD %s" % self)
        self.setLabel(DEATH_CROSS)
        self.config(fg=COLOR_DEAD, font="-weight bold" )

    # 1) User left-clicked empty tile, or
    # 2) Called as part of clearing a cluster
    # Set label to nr detected mines
    # Disable button so it no longer reacts to clicks
    # Increment cleared mine count
    def open(self):
        if not self.isOpen :
            self.isOpen = True
            self.setLabel(str(self.detectedMines) if 0<self.detectedMines else "  ")
            self.config(bg=COLOR_OPEN)
            self.bind("<1>", self.noOp)
            self.bind("<3>", self.noOp)
            self.config(state = "disabled")
            #without this, the module-global variable not seen here!
            global clearedCount
            clearedCount += 1
            checkGameWon(self)

    def openCluster(self):
        self.open()
        for ngbTile in getNeighbourTiles(tiles, self):
            if not ngbTile.isOpen and not ngbTile.hasMine:
                ngbTile.open()
                if ngbTile.detectedMines == 0 :
                    ngbTile.openCluster() #NB recursion

    # Cycle the label "" -> X -> ? -> ""
    # Disable left clicks for X and ? states
    # to protect against accidentally triggering mine
    def tileClickRight(self, event):
        transition = ""
        global markedCount
        if self.state == TileState.HIDDEN:
            self.state = TileState.MARKED
            self.bind("<1>", self.noOp)
            self.config(state = "disabled")
            transition = "state->MARKED"
            markedCount += 1
            checkGameWon(self)
        elif self.state == TileState.MARKED:
            self.state = TileState.MAYBE
            self.bind("<1>", self.noOp)
            self.config(state = "disabled")
            transition = "state->MAYBE"
            markedCount -= 1
        elif self.state == TileState.MAYBE:
            self.state = TileState.HIDDEN
            transition = "state->HIDDEN"
            self.bind("<1>", self.tileClickLeft)
            self.config(state = "normal")
        else:
            raise AssertionError("row=%d,col=%d, unexpected state %s"%(self.row, self.col, self.state))
        #log("R-clk: %s (%s)" % (self.__str__(), transition))

        #Update button label to new state
        self.config(text=TileState.labels[self.state])



# Seems PEP8 conventions are checked by PyCharm
# Wants two blank lines after functions.

def log(msg:str):
    statusLine.config(text=msg)
    print (msg)

#Activate tracing : False -> True
def trace(msg:str):
    if(False): print (msg)


def checkGameWon( tile : Tile ):
    if GRID_COLS*GRID_ROWS <= clearedCount + markedCount :
        print( "TODO congrats dialog needed here")
        log("You won! Congratulations.")

# Example of typed arguments and return value in a function
#
def placeMinesRandomly(nMines : int, tileRowArray : list, mineIndexes : list) -> int:
    N = GRID_COLS*GRID_ROWS
    if N < nMines :
        raise ValueError("Can't place %d mines in %d grid tiles" % (nMines,N ))
    origMines = nMines

    mineIndexes.clear()
    for attempt in range(1, 100):
        print("Lay mines iter: %d (outstanding %d mines)..  " % (attempt, nMines))
        rCol, rRow = random.randint(0,GRID_COLS-1), random.randint(0,GRID_ROWS-1)
        tileRow = tileRowArray[rRow]
        tile = tileRow[rCol]
        print( "Chosen random tile: %s" % tile)

        if not tile.hasMine :
            tile.hasMine = True
            mineIndexes.append(tile)

            ngbList = getNeighbourTiles(tileRowArray, tile)
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
    trace("Collect ngbs of Tile: %s" % tile)
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
                trace("\tNgb (dRow %d, dCol %d): %s" % (dRow, dCol, ngbTile)  )
                ngbs.append(ngbTile)
            else:
                trace("\tSelf (dRow %d, dCol %d): %s" % (dRow, dCol, ngbTile)  )
    return ngbs


def quit():
    log("clicked quit")
    win.destroy()

# Fill the middle frame with a grid of squares
# Some of them have a mine in them
#
def newGame():
    global frame
    markedCount = 0
    openedCount = 0
    tiles.clear()
    for r in range(GRID_ROWS):
        tileRow = []
        for c in range(GRID_COLS):
            tile = Tile(frame, c, r, TEXT_HIDDEN)
            tileRow.append(tile)
            tile.grid(row=r, column=c, sticky="ewns") #ewns = fill grid cell
        tiles.append(tileRow)
    mineIndices = []
    # TODO dialog to configure game ?
    placeMinesRandomly(15, tiles, mineIndices)

# I guess main starts here..

# basic window with title and standard controls
win = Tk.Tk()

# Toolbar = some buttons in a frame parked at the top
# Instead of text=".." can use image= for which you can load
# an image from disk using PhotoImage constructor.
#
# Binding events:
# <1> or <Button-1> or <ButtonPress-1> = left click
# <2> = middle click
# <3> = right click
# <B1-Motion> = left drag
# <ButtonRelease-1> = left button released
# <DoubleButton-1> = left button double-clicked
# <TripleButton-1> = left button triple-clicked
# <Enter/Leave> = mouse pointer entered/left widget
# <Return> = keyboard 'Enter' key pressed with widget focused
# .. and lots of other standard keys..
#
toolbar = Tk.Frame( win )
Tk.Button(toolbar, text="new game", command=newGame).pack(side="left", padx=2, pady=2)
Tk.Button(toolbar, text="quit",     command=quit).pack(side="right", padx=2, pady=2)
Tk.Button(toolbar, text="TODO use images!").pack(side="left", padx=2, pady=2)
toolbar.pack(side="top", fill="x")

frame = Tk.Frame(win, width=TILE_SIZE * GRID_COLS, height=TILE_SIZE * GRID_ROWS)
frame.pack()

# add a status line at bottom
statusLine = Tk.Label(win, text="", bd=1, relief="sunken", anchor="w")
statusLine.pack(side="bottom", fill="x")
newGame()

win.mainloop()
