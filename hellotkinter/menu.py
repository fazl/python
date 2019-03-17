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
    status.config(text="clicked File|New")

def handleOpenFile():
    status.config(text="clicked File|Open")

def handleExit():
    status.config(text="So long..")
    print("clicked menu File|Exit")
    win.destroy()

def handleHelpAbout():
    status.config(text="clicked Help|About")

# basic window with title and standard controls
win = Tk.Tk() 

# just some buttons in a frame parked at the top, for a toolbar
# instead of text=".." can use image= for which you can load
# an image from disk using PhotoImage constructor.
toolbar = Tk.Frame( win )
b = Tk.Button(toolbar, text="new", width=6, command=handleNewFile)
b.pack(side="left", padx=2, pady=2)

b = Tk.Button(toolbar, text="open", width=6, command=handleOpenFile)
b.pack(side="left", padx=2, pady=2)

toolbar.pack(side="top", fill="x")


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

# add a status line at bottom
status = Tk.Label(win, text="", bd=1, relief="sunken", anchor="w")
status.pack(side="bottom", fill="x")


win.mainloop()
#win.destroy()

