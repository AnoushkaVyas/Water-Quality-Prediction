import matplotlib 
matplotlib.use('TkAgg')
from tkinter import * 
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile 
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import pickle
from tkinter import messagebox
from pandastable import Table, TableModel



import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Water Quality Index Estimation")
root.configure(background="light blue") 

pkl_filename = 'pickle_model.pkl'
equation = StringVar()

expression_field = Entry(root, textvariable=equation) 

data = ""
var = ""
date = ""
wqi = []
X = []
label = []
df = {}
val = ""
f = ""
canvas = ""
pred = ""
toolbar = ""

with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

def open_file(): 
    global data,var,date,X,label,df,pred,wqi
    data = ""
    var = ""
    date = ""
    wqi = []
    X = []
    label = []
    df = {}
    val = ""
    f = ""
    canvas = ""
    pred = ""
    toolbar = ""

    file = askopenfile(mode ='r', filetypes =[('Csv Files', '*.csv')])

    if file is not None: 
        data = pd.read_csv(file.name)
        date = data['Date']

        if 'WQI' in data.keys():
        	wqi = data['WQI']
        
        if len(wqi) != 0:
        	var = data.drop(['Date','WQI'],axis = 1)
        else:
        	var = data.drop(['Date'],axis = 1)


        for i in var.index:
        	X.append(normalize_q(var['pH'][i],var['TEMP'][i],var['TURB'][i],var['NO3N'][i],var['TP'][i],var['FECALCOLI'][i]))
        X = np.array(X)
        pred = model.predict(X)

        for x in pred:
        	label.append(WQC(x))

        df['Predicted WQI'] = pred
        df['Predicted WQC'] = label 
        if len(wqi) != 0:
        	df['Actual WQI Value'] = wqi
        df['Date'] = data['Date']

        if len(wqi) != 0:
        	df = pd.DataFrame(df,columns = ['Date','Actual WQI Value','Predicted WQI','Predicted WQC'])
        else:
        	df = pd.DataFrame(df,columns = ['Date','Predicted WQI','Predicted WQC'])

    else:
    	messagebox.showerror("File Not Found","File Doesnot Exist")

    	    
    
def getg():
	global wqi,date,pred,canvas,toolbar,f

	if canvas != "":
		canvas.get_tk_widget().pack_forget()
	if toolbar != "":
		toolbar.pack_forget()
	if f != "":
		f.destroy()

	fig = Figure(figsize=(5, 4), dpi=100)
	a = fig.add_subplot(111)

	if len(wqi) != 0:
		a.plot(np.array(date),np.array(wqi),'r-^',label = 'Actual WQI Value')
	a.plot(np.array(date),np.array(pred),'b-*',label = 'Predicted WQI Value')
	a.legend()
	a.set_xlabel('Dates')
	a.set_ylabel('WQI Values')

	canvas = FigureCanvasTkAgg(fig, master=root)
	canvas.draw()
	canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

	toolbar = NavigationToolbar2Tk(canvas, root)
	toolbar.update()
	canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def normalize_q(q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli):

    q_norm_ph = 0
    q_norm_temp = 0
    q_norm_turb = 0
    q_norm_nitrates = 0
    q_norm_phosphate = 0
    q_norm_coli = 0

    if (q_ph >= 0 and q_ph < 2) or (q_ph > 12 and q_ph <= 14):
        q_norm_ph = 0
    elif (q_ph >= 2 and q_ph < 3) or (q_ph > 11 and q_ph <= 12):
        q_norm_ph = 2
    elif (q_ph >= 3 and q_ph < 4):
        q_norm_ph = 4
    elif (q_ph >= 4 and q_ph < 5):
        q_norm_ph = 8
    elif (q_ph >= 4 and q_ph < 5):
        q_norm_ph = 24
    elif (q_ph >= 5 and q_ph < 6):
        q_norm_ph = 55
    elif (q_ph >= 6 and q_ph < 7):
        q_norm_ph = 90
    elif (q_ph >= 7 and q_ph < 7.2):
        q_norm_ph = 92
    elif (q_ph >= 7.2 and q_ph < 7.5):
        q_norm_ph = 93
    elif (q_ph >= 7.5 and q_ph < 7.7):
        q_norm_ph = 90
    elif (q_ph >= 7.7 and q_ph < 8):
        q_norm_ph = 82
    elif (q_ph >= 8 and q_ph < 8.5):
        q_norm_ph = 67
    elif (q_ph >= 8.5 and q_ph < 9):
        q_norm_ph = 47
    elif (q_ph >= 9 and q_ph < 10):
        q_norm_ph = 19
    elif (q_ph >= 10 and q_ph < 11):
        q_norm_ph = 7

    if (q_temp < -10):
        q_norm_temp = 56
    elif (q_temp >= -10 and q_temp < -7.5):
        q_norm_temp = 63
    elif (q_temp >= -7.5 and q_temp < -5):
        q_norm_temp = 73
    elif (q_temp >= -5 and q_temp < -2.5):
        q_norm_temp = 85
    elif (q_temp >= -2.5 and q_temp < -1):
        q_norm_temp = 90
    elif (q_temp >= -1 and q_temp < 0):
        q_norm_temp = 93
    elif (q_temp >= 0 and q_temp < 1):
        q_norm_temp = 89
    elif (q_temp >= 1 and q_temp < 2.5):
        q_norm_temp = 85
    elif (q_temp >= 2.5 and q_temp < 5):
        q_norm_temp = 72
    elif (q_temp >= 5 and q_temp < 7.5):
        q_norm_temp = 57
    elif (q_temp >= 7.5 and q_temp < 10):
        q_norm_temp = 44
    elif (q_temp >= 10 and q_temp < 12.5):
        q_norm_temp = 36
    elif (q_temp >= 12.5 and q_temp < 15):
        q_norm_temp = 28
    elif (q_temp >= 15 and q_temp < 17.5):
        q_norm_temp = 23
    elif (q_temp >= 17.5 and q_temp < 20):
        q_norm_temp = 21
    elif (q_temp >= 20 and q_temp < 22.5):
        q_norm_temp = 18
    elif (q_temp >= 22.5 and q_temp < 25):
        q_norm_temp = 15
    elif (q_temp >= 25 and q_temp < 27.5):
        q_norm_temp = 12
    elif (q_temp >= 27.5 and q_temp < 30):
        q_norm_temp = 10

    if q_turb < 0:
        q_norm_turb = 97
    elif (q_turb >= 0 and q_turb < 5):
        q_norm_turb = 84
    elif (q_turb >= 5 and q_turb < 10):
        q_norm_turb = 76
    elif (q_turb >= 10 and q_turb < 15):
        q_norm_turb = 68
    elif (q_turb >= 15 and q_turb < 20):
        q_norm_turb = 62
    elif (q_turb >= 20 and q_turb < 25):
        q_norm_turb = 57
    elif (q_turb >= 25 and q_turb < 30):
        q_norm_turb = 53
    elif (q_turb >= 30 and q_turb < 35):
        q_norm_turb = 48
    elif (q_turb >= 35 and q_turb < 40):
        q_norm_turb = 45
    elif (q_turb >= 40 and q_turb < 50):
        q_norm_turb = 39
    elif (q_turb >= 50 and q_turb < 60):
        q_norm_turb = 34
    elif (q_turb >= 60 and q_turb < 70):
        q_norm_turb = 28
    elif (q_turb >= 70 and q_turb < 80):
        q_norm_turb = 25
    elif (q_turb >= 80 and q_turb < 90):
        q_norm_turb = 22
    elif (q_turb >= 90 and q_turb < 100):
        q_norm_turb = 17
    elif q_turb >= 100:
        q_norm_turb = 5

    if q_nitrates < 0:
        q_norm_nitrates = 98
    elif (q_nitrates >= 0 and q_nitrates < 0.25):
        q_norm_nitrates = 97
    elif (q_nitrates >= 0.25 and q_nitrates < 0.5):
        q_norm_nitrates = 96
    elif (q_nitrates >= 0.5 and q_nitrates < 0.75):
        q_norm_nitrates = 95
    elif (q_nitrates >= 0.75 and q_nitrates < 1):
        q_norm_nitrates = 94
    elif (q_nitrates >= 1 and q_nitrates < 1.5):
        q_norm_nitrates = 92
    elif (q_nitrates >= 1.5 and q_nitrates < 2):
        q_norm_nitrates = 90
    elif (q_nitrates >= 2 and q_nitrates < 3):
        q_norm_nitrates = 85
    elif (q_nitrates >= 3 and q_nitrates < 4):
        q_norm_nitrates = 70
    elif (q_nitrates >= 4 and q_nitrates < 5):
        q_norm_nitrates = 65
    elif (q_nitrates >= 5 and q_nitrates < 10):
        q_norm_nitrates = 51
    elif (q_nitrates >= 10 and q_nitrates < 15):
        q_norm_nitrates = 43
    elif (q_nitrates >= 15 and q_nitrates < 20):
        q_norm_nitrates = 37
    elif (q_nitrates >= 20 and q_nitrates < 30):
        q_norm_nitrates = 24
    elif (q_nitrates >= 30 and q_nitrates < 40):
        q_norm_nitrates = 17
    elif (q_nitrates >= 40 and q_nitrates < 50):
        q_norm_nitrates = 7
    elif (q_nitrates >= 50 and q_nitrates < 60):
        q_norm_nitrates = 5
    elif (q_nitrates >= 60 and q_nitrates < 70):
        q_norm_nitrates = 4
    elif (q_nitrates >= 70 and q_nitrates < 80):
        q_norm_nitrates = 3
    elif (q_nitrates >= 80 and q_nitrates < 90):
        q_norm_nitrates = 2
    elif q_nitrates >= 90:
        q_norm_nitrates = 1
    
    if q_phosphate < 0:
        q_norm_phosphate = 99
    elif (q_phosphate >= 0 and q_phosphate < 0.05):
        q_norm_phosphate = 98
    elif (q_phosphate >= 0.05 and q_phosphate < 0.1):
        q_norm_phosphate = 97
    elif (q_phosphate >= 0.1 and q_phosphate < 0.2):
        q_norm_phosphate = 95
    elif (q_phosphate >= 0.2 and q_phosphate < 0.3):
        q_norm_phosphate = 90
    elif (q_phosphate >= 0.3 and q_phosphate < 0.4):
        q_norm_phosphate = 78
    elif (q_phosphate >= 0.4 and q_phosphate < 0.5):
        q_norm_phosphate = 60
    elif (q_phosphate >= 0.5 and q_phosphate < 0.75):
        q_norm_phosphate = 50
    elif (q_phosphate >= 0.75 and q_phosphate < 1):
        q_norm_phosphate = 39
    elif (q_phosphate >= 1 and q_phosphate < 1.5):
        q_norm_phosphate = 30
    elif (q_phosphate >= 1.5 and q_phosphate < 2):
        q_norm_phosphate = 26
    elif (q_phosphate >= 2 and q_phosphate < 3):
        q_norm_phosphate = 21
    elif (q_phosphate >= 3 and q_phosphate < 4):
        q_norm_phosphate = 16
    elif (q_phosphate >= 4 and q_phosphate < 5):
        q_norm_phosphate = 12
    elif (q_phosphate >= 5 and q_phosphate < 6):
        q_norm_phosphate = 10
    elif (q_phosphate >= 6 and q_phosphate < 7):
        q_norm_phosphate = 8
    elif (q_phosphate >= 7 and q_phosphate < 8):
        q_norm_phosphate = 7
    elif (q_phosphate >= 8 and q_phosphate < 9):
        q_norm_phosphate = 6
    elif (q_phosphate >= 9 and q_phosphate < 10):
        q_norm_phosphate = 5
    elif q_phosphate >= 10:
        q_norm_phosphate = 2

    if (q_coli >= 0 and q_coli < 1):
        q_norm_coli = 98
    elif (q_coli >= 1 and q_coli < 2):
        q_norm_coli = 89
    elif (q_coli >= 2 and q_coli < 5):
        q_norm_coli = 80
    elif (q_coli >= 5 and q_coli < 10):
        q_norm_coli = 71
    elif (q_coli >= 10 and q_coli < 20):
        q_norm_coli = 63
    elif (q_coli >= 20 and q_coli < 50):
        q_norm_coli = 53
    elif (q_coli >= 50 and q_coli < 100):
        q_norm_coli = 45
    elif (q_coli >= 100 and q_coli < 200):
        q_norm_coli = 37
    elif (q_coli >= 200 and q_coli < 500):
        q_norm_coli = 27
    elif (q_coli >= 500 and q_coli < 1000):
        q_norm_coli = 22
    elif (q_coli >= 1000 and q_coli < 2000):
        q_norm_coli = 18
    elif (q_coli >= 2000 and q_coli < 5000):
        q_norm_coli = 13
    elif (q_coli >= 5000 and q_coli < 10000):
        q_norm_coli = 10
    elif (q_coli >= 10000 and q_coli < 20000):
        q_norm_coli = 8
    elif (q_coli >= 20000 and q_coli < 50000):
        q_norm_coli = 5
    elif (q_coli >= 50000 and q_coli < 100000):
        q_norm_coli = 3
    elif q_coli >= 100000:
        q_norm_coli = 2

    return [q_norm_temp, q_norm_ph, q_norm_turb, q_norm_coli,q_norm_nitrates, q_norm_phosphate]


def WQC(x):
  if x >= 0 and x <= 25:
    return "Very Bad"
  if x > 25 and x <= 50:
    return "Bad"
  if x > 50 and x <= 70:
    return "Medium"
  if x > 70 and x <= 90:
    return "Good"
  return "Excellent"

def exportCSV ():
    global df
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv (export_file_path, index = False, header=True)

def showTable():
	global df
	global f,canvas,toolbar

	if canvas != "":
		canvas.get_tk_widget().pack_forget()
	if toolbar != "":
		toolbar.pack_forget()
	if f != "":
		f.destroy()

	f = Frame(root)
	f.pack(side = Tk.TOP,fill=BOTH,expand = 1)
	pt = Table(f, dataframe=df, showstatusbar=True)
	pt.show()

def _clear():
	global f,canvas,toolbar
	if canvas != "":
		canvas.get_tk_widget().pack_forget()
	if toolbar != "":
		toolbar.pack_forget()
	if f != "":
		f.destroy()

	f = ""
	canvas = ""
	toolbar = ""



btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = Tk.TOP, pady = 10)  
btn = Button(root, text ='graph', command = lambda:getg()) 
btn.pack(side = Tk.TOP, pady = 10)  
btn = Button(text='Show Predictions', command=showTable)
btn.pack(side = Tk.TOP, pady = 10)  
btn = Button(text='Export CSV', command=exportCSV)
btn.pack(side = Tk.TOP, pady = 10) 
btn = Button(text='CLEAR', command=lambda:_clear())
btn.pack(side = Tk.TOP, pady = 10)  



def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()


