# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-hello-again.htm
#
# I can run this program like this in a command window:
#
# C:\Users\Fazl\AppData\Local\Programs\Python\Python37\python.exe helloapp.py
#

# Python2 has package Tkinter not tkinter
# There is great value in consistency :(
# (Anyway it gives me a chance to look at exceptions
# From: https://stackoverflow.com/a/25905642)
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 

# Try wrapping stuff into a class
class App:
    # Hmm python methods need explicit 'this' arg ?
    #
    def printMsg(self):     
        print( "howdie" )
        
    def printMsg(self, msg):     
        print( msg )
        
    # Constructors are called __init__
    def __init__(self,ownerWnd):
        #python must be told which printMsg..
        self.printMsg("In App.ctor")  
        
        

# root widget Tk is like a Swing JFrame, i.e. a
# basic window with title and standard controls
win = Tk.Tk()
app = App(win)

# Label whose parent is the root window
# Can also show image instead of text..
label = Tk.Label(win, text="Hello, Tkinter!")
label.pack()

#Add more controls, aiming to encapsulate into a class later
frame = Tk.Frame(win)
frame.pack()

btnQuit = Tk.Button(frame, text="Quit", fg="red", command=frame.quit)
btnQuit.pack(side="left")

btnHello = Tk.Button(frame, text="Print hi..", command=app.printMsg)
btnHello.pack(side="right")

# Swing has pack() and setVisible()..
win.mainloop()


