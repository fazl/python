try:
    import tkinter as Tk  ## python3: tkinter
    import tkinter.messagebox as messagebox    # stackoverflow.com/a/38181986
except ImportError:
    import Tkinter as Tk  ## python2: tkinter
    import tkMessageBox as messagebox

# Game Configuration setup
# Dialog grabs focus
#
class ConfigDialog:

    def mkEntry(selfs, d:Tk.Toplevel, var:Tk.IntVar, r:int, c:int, )->Tk.Entry:
        # Must do this in two steps; sadly grid() returns None..
        # (No warning of course from "Be my guest, make a mess" Python)
        #
        e = Tk.Entry(d, textvariable=var)
        e.grid(row=r, column=c)
        return e

    def __init__(self, ownerWnd, mineCount, gridRows, gridcols):
        print("In MyDialog.ctor")
        self.origMines = self.mines = Tk.IntVar(value=mineCount)
        self.origRows = self.rows = Tk.IntVar(value=gridRows)
        self.origCols = self.cols = Tk.IntVar(value=gridcols)
        self.changed = False

        d = self.top = Tk.Toplevel(ownerWnd)

        # Pressing Enter  --> OK
        # Pressing Escape --> Esc
        # CAVEAT <Enter> means mouse enters widget area
        # and causes untold comedy at runtime !
        #
        d.bind("<Return>", self.ok)
        d.bind("<Escape>", self.cancel)

        Tk.Label(d, text="Mines:").grid(row=0, column=0)
        Tk.Label(d, text="Rows: ").grid(row=1, column=0)
        Tk.Label(d, text="Cols: ").grid(row=2, column=0)

        self.eMines = self.mkEntry(d, self.mines, 0, 2)
        self.eRows  = self.mkEntry(d, self.rows,  1, 2)
        self.eCols  = self.mkEntry(d, self.cols,  2, 2)

        Tk.Button(d, text="OK", command=self.ok).grid(row=3, column=0)
        Tk.Button(d, text="CANCEL", command=self.cancel).grid(row=3, column=2)

    def validate(self):
        try:
            # Pity python couldn't use trim() like most of the world
            self.mines = int(self.eMines.get().strip())
            self.rows  = int(self.eRows.get().strip())
            self.cols  = int(self.eCols.get().strip())
            return True
        except ValueError:
            messagebox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )
            return False

    def ok(self, event=None):
        print("OK: mines: %s, rows: %s, cols: %s" %
              (self.eMines.get(), self.eRows.get(), self.eCols.get()))
        if self.validate():
            if self.origMines != self.mines or \
               self.origRows != self.rows or  \
               self.origCols != self.cols:
                self.changed = True
                # mineCount = self.mines
                # GRID_ROWS = self.rows
                # GRID_COLS = self.cols
        else:
            self.initial_focus.focus_set()  # put focus back
            return
        self.top.destroy()  # or withdraw??
    def cancel(self, event=None):
        print("Cancel.. ")
        self.changed = False
        self.top.destroy()  # or withdraw??