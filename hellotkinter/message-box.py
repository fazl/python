# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

# For Python2 need uppercase T i.e. Tkinter 
#
try:
    import tkinter as Tk  ## python3: tkinter 
    import tkinter.messagebox as messagebox    # stackoverflow.com/a/38181986
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 
    import tkMessageBox as messagebox


# This creates an extra root window ! wtf
#if messagebox.askokcancel("Quit", "Really quit?"):
#    print ("Pressed OK")
#else:
#    print ("Canceled")
 

# basic window with title and standard controls
# won't accept args width=200, height=200 
win = Tk.Tk() 
label = Tk.Label( win, text="Try closing to see dialog" )


# click event handler
def confirmExit():
    if messagebox.askokcancel("Quit", "Really quit?"):
        win.destroy()

win.protocol("WM_DELETE_WINDOW", confirmExit)
label.pack()
win.mainloop()
#win.destroy()

