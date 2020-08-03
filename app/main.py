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
        ttk.Label(controls_frame, text = '(YYYY-MM-DD HH:MM:SS)', font='Courier 12').grid(row=1, column=0, padx=50, sticky='s')
        self.start = StringVar()
        ttk.Entry(controls_frame, width = 19, textvariable=self.start, font='Courier 12').grid(row=2, column=0, sticky='n')
        self.start.set(str(num2date(self.datetime_array[0]))[0:19])
        
        ttk.Label(controls_frame, text = 'End', font='Arial 18 bold').grid(row=0, column=1, pady=5)
        ttk.Label(controls_frame, text = '(YYYY-MM-DD HH:MM:SS)', font='Courier 12').grid(row=1, column=1, padx=50, sticky='s')
        self.ebd = StringVar
        ttk.Entry(controls_frame, width = 19, textvariable = self.end, font='Courier 12').grid(row=2, column=1, sticky='n')
        self.end.set(str(num2date(self.datetime_array[-1]))[0:19])
        
        ttk.Button(controls_frame, text="Update", command=self._update).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Style().configure('TButton', font='Arial 18 bold')
        
        self._update()
        
    def _update(self):
        # get user input
        try:
            start_num = date2num(datetime(*list(map(int, re.findall(r'[\d]{1,4}', self.start.get())))))
            end_num = date2num(datetime(*list(map(int, re.findall(r'[\d]{1,4}', self.end.get())))))
        except Exception as e:
            messagebox.showerror(title='Invalid Input VAlues', message=e)
            return
        start_idx = np.searchsorted(self.datetime_array, start_num)
        end_idx = np.searchsorted(self.datetime_array, end_num)
        
        if end_idx <= start_idx:
            messagebox.showerror(title='Invalid Input Values',
                                 message = 'End Date must be after Start Date')
            return

        # calculate slope value
        dy = self.barpress_array[end_idx] - self.barpress_array[start_idx]
        dt = self.datetime_array[end_idx] - self.datetime_array[start_idx]
        slope = dy/dt
        
        # plot data and slope line
        self.a.clear()
        self.a.plot_date(self.datetime_array[start_idx:end_idx],
                         self.barpress_array[start_idx:end_idx], linewidth=2)
        self.a.plot([self.datetime_array[start_idx], self.datetime_array[end_idx]],
                    [self.barpress_array[start_idx], self.barpress_array[end_idx]],
                    color='k', linestyle = '-', linewidth = 2)
        self.a.set_ylabel('Barometric Pressure (inHg)')
        self.a.set_xlabel('Date')
        
        # add colored slope value to figure
        
    def main():
        root = Tk()
        app = WeatherStatistics(root)
        root.mainloop()
    
    if __name__ == "__main__": main()