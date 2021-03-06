import logging  # DEBUG INFO WARNING ERROR
import tkinter.ttk as TTK  # use for Combobox
import win_main2
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


def GUI_start():
    """This will initialise the loggers
    After all imports it will start the main window 
    """
    print("-_____GUI start____-")

    logging.basicConfig(filename="logging.log", level=logging.DEBUG,  # <- set logging level
                        format="%(asctime)s:%(levelname)s:%(message)s")  # set level

    # Set up multpiple Log handler

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

    # windows
    # from puls_win import *
    # from pre_expsetup import *
    print("-_____GUI init of logging end____-")

    print("___start GUI analys")
    # show window, wait for user imput
    win_main = win_main2.window_main()
    win_main.mainloop()

    # end
    print("_____end from GUI_analyzer___")
