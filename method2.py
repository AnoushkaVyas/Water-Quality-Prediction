import numpy as np 
import csv 
from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename 
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Water Pollution Estimation")
root.configure(background="light blue") 
equation = StringVar()

expression_field = Entry(root, textvariable=equation) 

val = []
num = 0

Infilename_var=Tk.StringVar()
Outfilename_var=Tk.StringVar()

parameters = {}
Pollution_index = {}
Rivername = ""
Stationnumber = 0
Stationcode = []
River_long=0
River_lat=0
Latitude = []
Longitude = []
  
def open_file(): 
    global val
    global num
    file = askopenfilename()
    Infilename_var.set(file)
    

def writeFile(file_name, data):
    file = open(file_name,'a+')

    fields = ["Station Code", "OIP", "Class"]
    rows = []
    for i in range(0,Stationnumber):
        row = []
        row.append(Stationcode[i])
        row.append(data[0][i])
        row.append(data[1][i])
        rows.append(row)

    with open(file_name, 'w') as file:
        csvwriter = csv.writer(file) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows) 
    
    file.close()


def read_input():
    global Rivername
    global Stationnumber
    global Stationcode
    global Latitude
    global Longitude

    filename = Infilename_var.get()
    fields = [] 
    rows = []
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile) 
        
        fields = next(csvreader) 
        Rivername = fields[1]
        River_lat=fields[2]
        River_long=fields[3]
        
        fields = next(csvreader) 
        Stationcode = [code for code in fields[1:]]

        fields = next(csvreader) 
        Latitude = [float(code) for code in fields[1:]]

        fields = next(csvreader) 
        Longitude = [float(code) for code in fields[1:]]

        for row in csvreader: 
            rows.append(row)

        Stationnumber = len(rows[0])-1
        
    for row in rows:
        values = []
        for col in row[1:]:
            if col:
                values.append(float(col))
            else:
                values.append("")

        parameters[row[0]] = values

    return Stationcode,River_lat,River_long

def Turbidity(y):
    if y <= 5:
        x=1
    if y>5 and y <= 10:
        x = y/5 
    if y>10 and y <= 500:
        x = (y+43.9)/34.5

    return x

def pH(y):
    if y == 7:
        x = 1
    if y > 7:
        x = np.exp((y-7.0)/1.082)
    if y < 7:
        x = np.exp((7-y)/1.082)
    return x

def Color(y):
    if y >10 and y<=150:
        x = (y+130)/140
    if y>150 and y<=1200:
        x = y/75
    return x

def DO(y):
    if y<=50:
        x = np.exp(-(y-98.33)/36.067)
    if y>=50 and y<100:
        x = (y-107.58)/14.667
    if y>=100:
        x = (y-79.543)/19.054
    return x

def BOD(y):
    if y<2:
        x = 1
    if y>=2 and y<30:
        x = y/1.5
    return x

def TDS(y):
    if y<= 500:
        x = 1
    if y>500 and y<=1500:
        x = np.exp((y-500)/721.5)
    if y>1500 and y<=3000:
        x = (y-1000)/125
    if y>3000 and y<=6000:
        x = y/375
    return x

def Hardness(y):
    if y<=75:
        x = 1
    if y>75 and y<=500:
        x = np.exp(y + 42.5)/205.58
    if y>500:
        x = (y + 500)/125
    return x

def CL(y):
    if y <= 150:
        x=1
    if y > 150 and y <= 250:
        x=np.exp((y/50)-3)/1.4427
    if y>250:
        x= np.exp((y/50)+10.167)/10.82
    return x

def NO3(y):
    if y <= 20:
        x=1
    if y > 20 and y <= 50:
        x=np.exp(y-145.16)/76.28
    if y > 50 and y <= 200:
        x= y/65
    return x

def SO4(y):
    if y <= 150:
        x=1
    if y > 150 and y <= 2000:
        x= ((y/50)+0.375)/2.5121
    return x

def Coli(y):
    if y <= 50:
        x=1
    if y > 50 and y <= 5000:
        x= (y/50)**0.3010
    if y > 5000 and y <= 15000:
        x= ((y/50)-50)/16.071
    if y>15000:
        x=(y/15000)+16
    return x

def As(y):
    if y <= 0.005:
        x=1
    if y > 0.005 and y <= 0.01:
        x=y/0.005
    if y > 0.01 and y <= 0.1:
        x= (y+0.015)/0.0146
    if y>0.1 and y<=1.3:
        x=(y+1.1)/0.15
    return x

def F(y):
    if y>0 and y <= 1.2:
        x=1
    if y>1.2 and y<=10:
        x= ((y/1.2)-0.3819)/0.5083
    return x

def compute_pollution_index():
    if "Turbidity" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["Turbidity"]:
            if value:
                temp_pollution_index.append(Turbidity(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["Turbidity"] = temp_pollution_index
    
    if "pH" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["pH"]:
            if value:
                temp_pollution_index.append(pH(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["pH"] = temp_pollution_index

    if "Color" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["Color"]:
            if value:
                temp_pollution_index.append(Color(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["Color"] = temp_pollution_index

    if "DO" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["DO"]:
            if value:
                temp_pollution_index.append(DO(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["DO"] = temp_pollution_index
        
    if "BOD" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["BOD"]:
            if value:
                temp_pollution_index.append(BOD(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["BOD"] = temp_pollution_index
        
    if "TDS" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["TDS"]:
            if value:
                temp_pollution_index.append(TDS(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["TDS"] = temp_pollution_index
        
    if "Hardness" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["Hardness"]:
            if value:
                temp_pollution_index.append(Hardness(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["Hardness"] = temp_pollution_index
        
    if "CL" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["CL"]:
            if value:
                temp_pollution_index.append(CL(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["CL"] = temp_pollution_index
        
    if "NO3" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["NO3"]:
            if value:
                temp_pollution_index.append(NO3(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["NO3"] = temp_pollution_index
        
    if "SO4" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["SO4"]:
            if value:
                temp_pollution_index.append(SO4(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["SO4"] = temp_pollution_index
        
    if "Coli" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["Coli"]:
            if value:
                temp_pollution_index.append(Coli(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["Coli"] = temp_pollution_index
        
    if "As" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["As"]:
            if value:
                temp_pollution_index.append(As(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["As"] = temp_pollution_index
        
    if "F" in parameters.keys():
        temp_pollution_index = []
        for value in parameters["F"]:
            if value:
                temp_pollution_index.append(F(float(value)))
            else:
                temp_pollution_index.append(0)

        Pollution_index["F"] = temp_pollution_index

    show_OIP()

def show_OIP():
    OIP = []
    OIP_num=[]
    Class = []
    for num in range(0,Stationnumber):
        temp_oip = 0
        count = 0
        for key in Pollution_index:
            temp_oip += Pollution_index[key][num]
            count += 1

        if(temp_oip/count >0 and temp_oip/count<=1):
            Class.append("C1")
        elif(temp_oip/count >1 and temp_oip/count<=2):
            Class.append("C2")
        elif(temp_oip/count >2 and temp_oip/count<=4):
            Class.append("C3")
        elif(temp_oip/count >4 and temp_oip/count<=8):
            Class.append("C4")
        elif(temp_oip/count >8 and temp_oip/count<=16):
            Class.append("C5")
        OIP.append(str(temp_oip/count))
        OIP_num.append(temp_oip/count)


    t = Table(root, OIP, Class)
    writeFile(Outfilename_var.get(), [OIP, Class])
    return OIP_num,Class

class Table: 
      
    def __init__(self,root, OIP, Class): 
        self.e = Entry(root, width=20) 
        self.e.grid(row=5, column=0) 
        self.e.insert(END, "Station Code")

        self.e = Entry(root, width=20) 
        self.e.grid(row=5, column=1) 
        self.e.insert(END, "OIP")

        self.e = Entry(root, width=20) 
        self.e.grid(row=5, column=2) 
        self.e.insert(END, "Class")

        for i in range(0,Stationnumber):
            self.e = Entry(root, width=20) 
            self.e.grid(row=6+i, column=0) 
            self.e.insert(END, Stationcode[i])

            self.e = Entry(root, width=20) 
            self.e.grid(row=6+i, column=1) 
            self.e.insert(END, OIP[i])

            self.e = Entry(root, width=20) 
            self.e.grid(row=6+i, column=2) 
            self.e.insert(END, Class[i]) 

def riverstretch():
    fig = plt.figure(figsize=(8, 8))
    plt.title(Rivername)
    Stationcode ,River_lat,River_long=read_input()
    m = Basemap(projection='lcc', resolution='f', lat_0=River_lat, lon_0=River_long,width=1E6, height=1E6)
    m.shadedrelief()
    m.drawrivers(color='blue')
    m.drawstates(color='gray')

    OIP_num,Class=show_OIP()
    for i in range(len(Latitude)):
        if Class[i]=='C1':
            marker='o'
        if Class[i]=='C2':
            marker='V'
        if Class[i]=='C3':
            marker='^'
        if Class[i]=='C4':
            marker='s'
        if Class[i]=='C5':
            marker='d'
        m.scatter(Longitude[i],Latitude[i], latlon=True,c=OIP_num[i], cmap='RdBu_r', marker=marker,alpha=0.5,label=[Stationcode[i],Class[i]])

    plt.colorbar(label=r'$OIP$')
    plt.clim(-7, 7)
    plt.legend()
    plt.savefig(str(Rivername)+'.png')
    plt.show()


inputfile_label = Tk.Label(root, text = 'Input File',font=('calibre',10, 'bold')) 
inputfile_entry = Tk.Entry(root,textvariable = Infilename_var,font=('calibre',10,'normal'))
btn = Button(root, text ='Open', command = lambda:open_file()) 

inputfile_label.grid(row=0, column=0)
inputfile_entry.grid(row=0, column=1)
btn.grid(row=0, column=2)

outputfile_label = Tk.Label(root, text = 'Output File',font=('calibre',10, 'bold')) 
outputfile_entry = Tk.Entry(root,textvariable = Outfilename_var,font=('calibre',10,'normal'))

outputfile_label.grid(row=1, column=0)
outputfile_entry.grid(row=1, column=1)

Readbtn = Button(root, text ='Read File', command = lambda:read_input()) 
Readbtn.grid(row=2,column=1) 

Computebtn = Button(root, text ='Compute OIP', command = lambda:compute_pollution_index()) 
Computebtn.grid(row=3,column=1) 

Plotbtn = Button(root, text ='River Stretch', command = lambda:riverstretch()) 
Plotbtn.grid(row=4,column=1) 

def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.grid(row=20,column=1)

Tk.mainloop()


