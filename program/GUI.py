print("-_____GUI start____-")
import sys
import os
import numpy as np
import matplotlib
import tkinter as tk
import tkinter.ttk as TTK #use for Combobox
from tkinter import scrolledtext   # use to display logger

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import configparser
import queue

print("-_____GUI imports_end____-")


import logging # DEBUG INFO WARNING ERROR 
from logging.handlers import QueueHandler
logging.basicConfig(filename="logging.log", level=logging.DEBUG, # <- set logging level
    format="%(asctime)s:%(levelname)s:%(message)s"  ) # set level
    
#log = logging.getLogger("log")

#log = logging.getLogger(__name__)  
#log.setLevel(logging.WARNING)
#file_handler = logging.FileHandler("logging.log")
#formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
#file_handler.setFormatter(formatter)
#log.addHandler(file_handler)

import logging # DEBUG INFO WARNING ERROR 
from logging.handlers import QueueHandler
loggerGUI = logging.getLogger(__name__)
loggerGUI.setLevel(logging.DEBUG) # <- set logging level
    
loggerGUI_handler = logging.FileHandler("log_GUI_file.log")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
loggerGUI_handler.setFormatter(formatter)
loggerGUI.addHandler(loggerGUI_handler)
    
loggerGUI.info("set upp logger in puls_win.py")



### own imports
from function import *

## windows
from win_main2 import *
#from puls_win import *
#from pre_expsetup import *
print("-_____GUI own imports_end____-")


###
# colour http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/700px-TkInterColorCharts.png

print("___start GUI analys")
### get size of screen
#window = tk.Tk()
#window.title("get Window size")
#window.geometry("400x400")
#screen_width = window.winfo_screenwidth()
#screen_height = window.winfo_screenheight()
#window.destroy()
#
#print(type(screen_width))
#text="breite: "+str(screen_width)+ " hoehe: "+str(screen_height)
#print(text)


## constant Variabels
    
    



## show window, wait for user imput
win_main = window_main()
win_main.mainloop()


## end
print("_____end from GUI_analyzer___")

