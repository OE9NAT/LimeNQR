import logging
import sys
import numpy as np
import matplotlib
import tkinter as tk
import os
from tkinter import filedialog
# import tkinter.ttk as TTK #use for Combobox
# from tkinter import scrolledtext   # use for logger

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import configparser

print("-_____start function____-")

# import logging # DEBUG INFO WARNING ERROR
##from logging.handlers import QueueHandler
# logging.basicConfig(filename="logging.log", level=logging.DEBUG, # <- set logging level
#    format="%(asctime)s:%(levelname)s:%(message)s"  ) # set level

logging.info("logger import function")

logger_function = logging.getLogger('win_main')
logger_function.addHandler(logging.StreamHandler())
logger_function.info("logging from start up")

#import queue


def save_all():
    print("save all was clicked")
    print("test!! not implemented")


def load_setting(path="/home/pi/Bach_arbeit/program", file="setting_last_run.cfg"):
    """ load the settings file with all its variables for the experiment into a dictonary

    :param path: abolute path of the file with the settings *.cfg, defaults to "/home/pi/Bach_arbeit/program"
    :type path: str, optional
    :param file: file with the saved settings, defaults to "setting_last_run.cfg"
    :type file: str, optional
    :return: Values from loaded fils settings
    :rtype: dict
    """
    # read settings form cfg file
    path_settings = path+"/"+file
    print("setting file: ", path_settings)
    if not os.path.exists(path_settings):
        print("file Setting not found")
        logger_function.warning(
            "function.py, def load_setting, path_settings not found")
        #raise TypeError ("file dose not exist \n"+path_settings)

        # look fore settings.cfg
        path_settings = filedialog.askopenfilename(
            initialdir='/home/', title='select settings *.cfg path')
        print("setting file: ", path_settings)

    configParser = configparser.ConfigParser()
    configParser.read(path_settings)
    setting_dict = {section: dict(configParser.items(section))
                    for section in configParser.sections()}

    #print("sections: \n",configParser.sections())
    #print("\nsetting_dict:", *setting_dict.items(), sep="\n\n")

    # freq_start_input.delete(0,tk.END)
    # freq_start_input.insert(1,configParser.get(section,"freq_start"))

    logging.info("Values loaded from load_setting")
    return setting_dict


def RUN():

    print("new window from def click_run")
    lable_text = tk.Label(text="RUN  ", foreground="green",
                          background="black", font=("Arial Bold", 20))
    lable_text.place(x=600, y=700)

    window2 = tk.Tk()
    window2.title("Run in a Box")
    window2.geometry("300x200")
    window2.option_add("Helvetica", '10')

    window2_text = tk.Label(window2, text="RUN Input: ",
                            foreground="green")  # ,background="black")
    window2_text.place(x=5, y=10, width=160, height=50)

    freq_end_lable = tk.Label(window2, text="Frequenz: ", background="red")
    freq_end_lable.place(x=5, y=110, width=160, height=50)

    # Log some messages
    logger_function.debug('debug message')
    logger_function.info('info message')
    logger_function.warn('warn message')
    logger_function.error('error message')
    logger_function.critical('critical message')

    window2.mainloop()


def simple_label(text_unit, column, row):
    lable_text = tk.Label(text=text_unit)
    lable_text.place(x=column, y=row, width=40, height=30)
    return lable_text


def get_info_dialog():
    m_text = "\
    ************************\n\
    Autor: Philipp MALIN\n\
    Date: 01.07.2021\n\
    Version: 1.0\n\
    Description: Grapical user interface to control SDR\n\
                 for Nuclear Quadrupole Resonance spectroscopy.\n\
    ************************"
    tk.messagebox.showinfo(message=m_text, title="Info")


def error_window(text="TEST"):
    """rais a window for presenting an info or error message to the user

    :param text: Error message , defaults to "TEST"
    :type text: str, optional
    """
    m_tesxt = " \n ! ! ! ! ! ! ! ! ! !\n\
    wrong input of value\n\
    value should be \n \n"
    m_tesxt = m_tesxt + text

    tk.messagebox.showerror(message=m_tesxt, title="Error")


def error_type_window(input_var, type_should=str, variable_name="", message_example="none"):
    """rais a window for presenting an error message to the user with additional option

    :param input_var: what parameter we are talking about
    :type input_var: str
    :param type_should: expected type for the varialbe, defaults to str
    :type type_should: type , optional
    :param variable_name: additonal description of the variable , defaults to ""
    :type variable_name: str, optional
    :param message_example: a message for a example for solving type colission , defaults to "none"
    :type message_example: str, optional
    """
    m_tesxt = " \n Wrong input type \n"
    m_tesxt += variable_name+" input: " + \
        input_var + " is type: " + str(type(input_var)) + "\n"
    m_tesxt += "It should be: " + str(type_should) + "\n"
    m_tesxt += "correct input and retry \n \n"
    m_tesxt += "example: "+message_example

    tk.messagebox.showerror(message=m_tesxt, title="input type Error")


if __name__ == "__main__":
    print("import of package")
    # Add the handler to logger
