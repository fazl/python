# Loosely following tuturial at
# http://effbot.org/tkinterbook/tkinter-hello-tkinter.htm

# For Python2 need uppercase T i.e. Tkinter 
# There is great value in consistency :(
#
import tkinter as Tk  


# root widget like a Swing JFrame
# basic window with title and standard controls
# (there must be a way to set title)
root = Tk.Tk()
#root.title="boo" #No error but doesn't work

# Label whose parent is the root window
# Can either show text or image
# We use simple text..
w = Tk.Label(root, text="Hello, Tkinter!")

# Swing has pack() and setVisible()..
w.pack()
root.mainloop()

