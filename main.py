from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename 
import os

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Water Quality Index")
root.configure(background="light blue") 
equation = StringVar()

expression_field = Entry(root, textvariable=equation) 

def call_method1():
    os.system('python3  ./method1.py')

def call_method2():
    os.system('python3  ./method2.py')

def call_method3():
    os.system('python3  ./method3.py')

label = Tk.Label(root, text = 'Water Quality Estimation Methods',font=('calibre',10, 'bold')) 
label.grid(row=0,column=450) 

method1 = Button(root, text ='Method 1', command = lambda:call_method1()) 
method1.grid(row=450,column=450) 

method2 = Button(root, text ='Method 2', command = lambda:call_method2()) 
method2.grid(row=451,column=450) 


method3 = Button(root, text ='Method 3', command = lambda:call_method3()) 
method3.grid(row=452,column=450) 

def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.grid(row=455,column=450)

Tk.mainloop()


