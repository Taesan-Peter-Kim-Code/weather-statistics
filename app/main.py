import re
from csv import DictReader
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

import numpy as np
import matplotlib
from matplotlib.dates import date2num, num2date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class WeatherStatistics:
    def __init__(self, master):
        # load data
        datetime_list, barpress_list = [], []
        datetime_re = re.compile(
            r"[\d]{2,4}"
        )  # regular expression to get datetime info
        for year in range(2012, 2016):
            fileName = "..\\resources\\Environmental_Data_Deep_Moor_{0}.txt".format(year)
            print("Loading {0}".format(fileName))
            for row in DictReader(open(fileName, "r"), delimiter="\t"):
                barpress_list.append(float(row["Barometric_Press"]))
                datetime_list.append(
                    date2num(
                        datetime(
                            # *(asterisk operator) used to unpack that list of arguments and pass them to the date time constructor
                            *list(
                                map(int, datetime_re.findall(row["date       time    "]))))))
        #convert those lists into NumPy arrays
        self.datetime_array = np.array(datetime_list) 
        self.barpress_array = np.array(barpress_list)

        # build the GUI
        master.title('Weather Statistics')
        master.resizable(True, True)
        master.state('zoomed')
        
        matplotlib.rc('font', size = 18)
        f = Figure()
        f.set_facecolor(0,0,0,0)
        self.a = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, master)
        self.canvase.draw()
        toolbar_frame = ttk.Frame(master) # needed to put navbar above plot
        toolbar = NavigationToolbar2TkAgg(self.canvase, toolbar_frame)
        toolbar.update()
        toolbar_frame.pack(side=TOP, fill=X, expand=0)
        self.canvas._tkcanvas.pack(fill=BOTH, expand=1)
        
        controls_frame = ttk.Frame(master)
        controls_frame.pack()
        
        ttk.Label(controls_frame, text = 'Start', font='Arial 28 bold').grid(row=0, column=0, pady=5)
        ttk.Label(controls_frame, text = '(YYYY-MM-DD HH:MM:SS', font='Courier 12').grid(row=1, column=0, padx=50, sticky='s')
        
    
    def main():
        root = Tk()
        app = WeatherStatistics(root)
        root.mainloop()
    
    if __name__ == "__main__": main()