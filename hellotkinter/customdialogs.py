# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
#
# I can run this program like this in a command window:
#
# C:\Users\Fazl\AppData\Local\Programs\Python\Python37\python.exe customdialogs.py
#

# Python2 has package Tkinter not tkinter
try:
    import tkinter as Tk  ## python3: tkinter 
except ImportError:
    import Tkinter as Tk  ## python2: tkinter 

# Try wrapping stuff into a class
class MyDialog:

    def print(self):     
        print( "howdie" )
    
    def printMsg(self, msg):     
        print( msg )
        
    def __init__(self,ownerWnd):
        self.printMsg("In MyDialog.ctor")  
       
        top = self.top = Tk.Toplevel(ownerWnd)
        # Pressing Enter key now like pressing OK button
        # Fixes Problem2
        top.bind("<Return>", self.ok) 
        # NB <Enter> means mouse enters widget area
        # and <Return> means enter keypress
        # <Enter> causes comedy at runtime !
        
        Tk.Label(top, text="Value").pack()
        
        self.e = Tk.Entry(top)
        self.e.pack(padx=5)
        
        b = Tk.Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    
    # Ooh can have arg defaults; limited overloading
    # Fixes Problem2
    def ok(self,event=None):
        print( "OK.. value is: '%s', destroying top" % self.e.get() )
        self.top.destroy()


def startWorkflow():
    d = MyDialog(win)
    
    # Give focus to the entry field so can type into it
    # Fixes Problem2
    d.e.focus_set()       

    #Fixes Problem1
    d.top.grab_set()


    #Problem 1: user can click main win and lose dialog
    #           or create multiple dialogs -> confusion
    #Problem 2: can't just type into edit field (Entry)
    #           user first must click the field
    #           (and must click button not press enter)
    win.wait_window(d.top)  #Must know internals of dialog ?
    
# script continues here
win = Tk.Tk()


b = Tk.Button(win, text="Start worflow", command=startWorkflow).pack()
win.update()

win.mainloop()


