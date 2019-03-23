# OK lets see if we can do a crude minesweeper in python
# Hey, coding in pycharm is more fun than in text editor!
try:
    import tkinter as Tk  ## python3: tkinter 
    import tkinter.messagebox as messagebox    # stackoverflow.com/a/38181986
except ImportError:
    import Tkinter as Tk  ## python2: tkinter
    import tkMessageBox as messagebox
import random

## SUMMARY OF IDEAS FOR IMPROVEMENTS, EASY TO HARD
#  DONE dialogs on winning / losing should be trivial
#  DONE could display running totals in status line ??
#  TODO dialog to configure game ?
#  TODO add keyboard navigation should be straightforward
#  TODO use images in buttons



# GLOBALS AND CONSTANTS
# Seems python has no const or final keyword.
# Must simply never assign to an UPPERCASE variable more than once
# To help prevent redeclaring one you already defined, maybe put
# all constants definitions in one place.
#
# A very annoying feature of python is that it allows code
# in nested scopes to inherit names from outer scopes but
# only for reading, not for writing. Inconsistency. Don't like.
# If you suddenly need to also write to it, python creates
# a new local variable.  At least it has the decency to
# puke an error for the earlier reads.  Sigh.
#
# So these constants DON'T need to be accessed via 'global'
# but variables that must be mutated from nested scopes
# do.
#
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

# Putting 'global' vars in a class so can explicitly refer to
# their scope in other classes.
class G():
    clearedCount : int  = 0
    markedCount : int  = 0
    mineCount : int = 15
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
            G.markedCount += 1
            logMinesRemaining()
            self.userWonCheck()
        elif self.state == TileState.MARKED:
            self.state = TileState.MAYBE
            self.bind("<1>", self.noOp)
            self.config(state = "disabled")
            transition = "state->MAYBE"
            G.markedCount -= 1
            logMinesRemaining()
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

    def tileClickLeft(self, event):
        # log("L-clk: " + self.__str__())
        if self.hasMine :
            self.userLost()
        else :
            if self.detectedMines == 0:
                self.openCluster()
            else :
                self.open() #also sets label
            logMinesRemaining()

    def userLost(self):
        # log("You're DEAD %s" % self)
        self.setLabel(DEATH_CROSS)
        self.config(font="-weight bold" )
        self.bind("<1>", self.noOp)
        self.bind("<3>", self.noOp)
        self.config(state="disabled")

        if messagebox.askokcancel("KaBOOM! You just died..", "Start new game?"):
            newGame()

    def userWonCheck(self):
        if GRID_COLS * GRID_ROWS <= G.clearedCount + G.markedCount:
            log("You won! Congratulations.")
            if messagebox.askokcancel("Congratulations!", "Start new game?"):
                newGame()


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
            G.clearedCount += 1
            self.userWonCheck()

    def openCluster(self):
        self.open()
        for ngbTile in getNeighbourTiles(G.tiles, self):
            if not ngbTile.isOpen and not ngbTile.hasMine:
                ngbTile.open()
                if ngbTile.detectedMines == 0 :
                    ngbTile.openCluster() #NB recursion



# Seems PEP8 conventions are checked by PyCharm
# Wants two blank lines after functions.

def confirmExit():
    if messagebox.askokcancel("Quit", "Really quit?"):
        win.destroy()


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

def log(msg:str):
    statusLine.config(text=msg)
    print (msg)

def logMinesRemaining():
    log("Mines left: %d\t Cleared: %d" % (G.mineCount - G.markedCount, G.clearedCount))

# Fill the middle frame with a grid of squares
# Then ranomly place a mine under some of them
#
def newGame():
    G.markedCount = 0
    G.clearedCount = 0
    G.tiles.clear()
    for r in range(GRID_ROWS):
        tileRow = []
        for c in range(GRID_COLS):
            tile = Tile(G.frame, c, r, TEXT_HIDDEN)
            tileRow.append(tile)
            tile.grid(row=r, column=c, sticky="ewns") #ewns = fill grid cell
        G.tiles.append(tileRow)
    mineIndices = []
    # TODO dialog to configure game ?
    placeMinesRandomly(15, G.tiles, mineIndices)
    logMinesRemaining()

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


def quit():
    log("clicked quit")
    win.destroy()

#Activate tracing : False -> True
def trace(msg:str):
    if(False): print (msg)


# Program starts here
# ====================

# basic window with title and standard controls
win = Tk.Tk()
win.protocol("WM_DELETE_WINDOW", confirmExit)
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

G.frame = Tk.Frame(win, width=TILE_SIZE * GRID_COLS, height=TILE_SIZE * GRID_ROWS)
G.frame.pack()

# add a status line at bottom
statusLine = Tk.Label(win, text="", bd=1, relief="sunken", anchor="w")
statusLine.pack(side="bottom", fill="x")
newGame()

win.mainloop()
