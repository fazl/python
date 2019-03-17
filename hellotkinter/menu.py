# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-application-windows.htm

# For Python2 need uppercase T i.e. Tkinter 
#
try:
    import tkinter as Tk  ## python3: tkinter 
    import tkinter.messagebox as messagebox    # stackoverflow.com/a/38181986
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 
    import tkMessageBox as messagebox


# menu handlers
def handleNewFile():
    print("clicked menu NewFile")

def handleOpenFile():
    print("clicked menu OpenFile")

def handleExit():
    print("clicked menu Exit")
    win.destroy()

def handleHelpAbout():
    print("clicked menu About")

# basic window with title and standard controls
win = Tk.Tk() 
frame = Tk.Frame( win, width=200, height=200 )


# create main menu
mainMenu = Tk.Menu(win)
win.config(menu=mainMenu)

# add file menu
filemenu = Tk.Menu(mainMenu)
mainMenu.add_cascade(label="File", menu=filemenu)

filemenu.add_command(label="New", command=handleNewFile)
filemenu.add_command(label="Open..", command=handleOpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=handleExit)

# add help menu
mainMenu.add_separator()
helpmenu = Tk.Menu(mainMenu)
mainMenu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About", command=handleHelpAbout)

win.mainloop()
#win.destroy()

