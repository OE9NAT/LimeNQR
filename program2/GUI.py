import logging  # DEBUG INFO WARNING ERROR
import tkinter.ttk as TTK  # use for Combobox
from win_main2 import *
from function import *
from logging.handlers import QueueHandler
import queue
import configparser
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from tkinter import scrolledtext   # use to display logger
import tkinter as tk
import matplotlib
import numpy as np
import os
import sys
print("-_____GUI start____-")


logging.basicConfig(filename="logging.log", level=logging.DEBUG,  # <- set logging level
                    format="%(asctime)s:%(levelname)s:%(message)s")  # set level


logger_gui = logging.getLogger('GUI')
logger_gui.addHandler(logging.StreamHandler())
logger_gui.info("logging from GUI start up")


# own imports

# windows
#from puls_win import *
#from pre_expsetup import *
print("-_____GUI own imports_end____-")

# check if foler exist
if not os.path.exists("log"):
    os.mkdir("log")
if not os.path.exists("data"):
    os.mkdir("data")


###
# colour http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/700px-TkInterColorCharts.png

print("___start GUI analys")
# get size of screen
#window = tk.Tk()
#window.title("get Window size")
# window.geometry("400x400")
#screen_width = window.winfo_screenwidth()
#screen_height = window.winfo_screenheight()
# window.destroy()
#
# print(type(screen_width))
#text="breite: "+str(screen_width)+ " hoehe: "+str(screen_height)
# print(text)


# constant Variabels


# show window, wait for user imput
win_main = window_main()
win_main.mainloop()


# end
print("_____end from GUI_analyzer___")
