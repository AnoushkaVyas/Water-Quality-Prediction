import matplotlib 
matplotlib.use('TkAgg')
from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.geometry('900x900')
root.wm_title("Water Quality Index")
root.configure(background="light blue") 

file_xlsx = 'metadata_method1.xlsx'
df_xlsx = pandas.read_excel(file_xlsx, usecols=['GEMS Station Number', 'Station Identifier', 'Water Type', 'Latitude', 'Longitude'])

file_csv = 'samples_method1.csv'
df_csv = pandas.read_csv(file_csv, sep= ';', usecols=['GEMS Station Number', 'Sample Date', 'Parameter Code', 'Value'])

def getWQ(q_norm_ph, q_norm_temp, q_norm_turb, q_norm_nitrates, q_norm_phosphate, q_norm_coli):
    w_ph = 0.11
    w_temp = 0.10
    w_turb = 0.08
    w_nitrates = 0.10
    w_phosphate = 0.07
    w_coli = 0.16

    WQI_N = (q_norm_ph*w_ph) + (q_norm_temp*w_temp) + (q_norm_turb*w_turb) + (q_norm_nitrates*w_nitrates) + (q_norm_phosphate*w_phosphate) + (q_norm_coli*w_coli)
    WQI_D = w_ph + w_temp + w_turb + w_nitrates + w_phosphate + w_coli

    WQI = WQI_N/WQI_D

    if (WQI >= 0 and WQI < 25):
        WQC = "Very Bad"
    elif (WQI >= 25 and WQI < 50):
        WQC = "Bad"
    elif (WQI >= 50 and WQI < 70):
        WQC = "Medium"
    elif (WQI >= 70 and WQI < 90):
        WQC = "Good"
    elif (WQI >= 90 and WQI < 100):
        WQC = "Excellent"

    return WQI, WQC

def normalize_q(q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli):
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

    return q_norm_ph, q_norm_temp, q_norm_turb, q_norm_nitrates, q_norm_phosphate, q_norm_coli

def search_samples(station_number):
    q_ph = ""
    q_temp = ""
    q_turb = ""
    q_nitrate = ""
    q_phosphate = ""
    q_coli = ""
    sample_date = 0

    for i in df_csv.index:
        data_station_number = df_csv['GEMS Station Number'][i]

        if station_number == data_station_number:
            i_sample_date = int(str(df_csv['Sample Date'][i]).replace("-", ""))
            if sample_date <= i_sample_date:
                sample_date = i_sample_date

                parameter_code = str(df_csv['Parameter Code'][i])
                if parameter_code == 'pH':
                    q_ph = float(df_csv['Value'][i])
                if parameter_code == 'TEMP':
                    q_temp = float(df_csv['Value'][i])
                if parameter_code == 'TURB':
                    q_turb = float(df_csv['Value'][i])
                if parameter_code == 'NO3N':
                    q_nitrate = float(df_csv['Value'][i])
                if parameter_code == 'TP':
                    q_phosphate = float(df_csv['Value'][i])
                if parameter_code == 'FECALCOLI':
                    q_coli = float(df_csv['Value'][i])

    return q_ph, q_temp, q_turb, q_nitrate, q_phosphate, q_coli

def search_loc(latitude, longitude):
    for i in df_xlsx.index:
        data_latitude, data_longitude = str(df_xlsx['Latitude'][i]), str(df_xlsx['Longitude'][i])
        
        if latitude == data_latitude and longitude == data_longitude:
            station_number = str(df_xlsx['GEMS Station Number'][i])
            station_name = str(df_xlsx['Station Identifier'][i])
            water_type = str(df_xlsx['Water Type'][i])

            q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli = search_samples(station_number)
            q_norm_ph, q_norm_temp, q_norm_turb, q_norm_nitrates, q_norm_phosphate, q_norm_coli = normalize_q(q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli)
            WQI, WQC = getWQ(q_norm_ph, q_norm_temp, q_norm_turb, q_norm_nitrates, q_norm_phosphate, q_norm_coli)

            return station_number, station_name, water_type, q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli, WQI, WQC

def on_click():
    station_number, station_name, water_type, q_ph, q_temp, q_turb, q_nitrates, q_phosphate, q_coli, WQI, WQC = search_loc(latitude.get(), longitude.get())
    
    station_number_label = Label(root, text="Station Number: " + station_number)
    station_name_label = Label(root, text="Station Name: " + station_name)
    water_type_label = Label(root, text="Water Type: " + water_type)
    q_ph_label = Label(root, text="q(pH): " + str(q_ph))
    q_temp_label = Label(root, text="q(temperature): " + str(q_temp))
    q_turb_label = Label(root, text="q(turbidity): " + str(q_turb))
    q_nitrates_label = Label(root, text="q(nitrates): " + str(q_nitrates))
    q_phosphate_label = Label(root, text="q(phosphates): " + str(q_phosphate))
    q_coli_label = Label(root, text="q(fecalcoli): " + str(q_coli))
    WQI_label = Label(root, text="WQI: " + str(WQI))
    WQC_label = Label(root, text="WQC: " + str(WQC))

    station_number_label.pack()
    station_name_label.pack()
    water_type_label.pack()
    q_ph_label.pack()
    q_temp_label.pack()
    q_turb_label.pack()
    q_nitrates_label.pack()
    q_phosphate_label.pack()
    q_coli_label.pack()
    WQI_label.pack()
    WQC_label.pack()

latitude = Entry(root, width=50)
latitude.insert(END, "Enter Latitude: ")
latitude.pack()

longitude = Entry(root, width=50)
longitude.insert(END, "Enter Longitude: ")
longitude.pack()

btn = Button(root, text ='Get WQI', command = on_click) 
btn.pack(side = TOP, pady = 10)

def _quit():
    root.quit()     
    root.destroy()

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
