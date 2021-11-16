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
import tkinter as tk
from tkinter import scrolledtext   # use to display logger
import matplotlib
import numpy as np
import os
import sys
print("-_____GUI start____-")


print("-_____GUI imports_end____-")


logging.basicConfig(filename="logging.log", level=logging.DEBUG,  # <- set logging level
                    format="%(asctime)s:%(levelname)s:%(message)s")  # set level

# log = logging.getLogger("log")

# log = logging.getLogger(__name__)
# log.setLevel(logging.WARNING)
# file_handler = logging.FileHandler("logging.log")
# formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler.setFormatter(formatter)
# log.addHandler(file_handler)

loggerGUI = logging.getLogger(__name__)
loggerGUI.setLevel(logging.DEBUG)  # <- set logging level

logging_handler = logging.FileHandler("log_GUI_file.log")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
logging_handler.setFormatter(formatter)

loggerGUI.addHandler(logging_handler)
loggerGUI.info("set upp logger in puls_win.py")

logger_gui = logging.getLogger('GUI')
logger_gui.addHandler(logging.StreamHandler())
logger_gui.info("logging from GUI start up")


# own imports

# windows
# from puls_win import *
# from pre_expsetup import *
print("-_____GUI own imports_end____-")


###
# colour http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/700px-TkInterColorCharts.png

print("___start GUI analys")


# constant Variabels


# show window, wait for user imput
win_main = window_main()
win_main.mainloop()


# end
print("_____end from GUI_analyzer___")
