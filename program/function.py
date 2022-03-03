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


def load_setting(path="/home/pi/Bach_arbeit/program", file="setting.cfg"):
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
            initialdir='/home/', title='select settings.cfg path')
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


def variable_input_windows():
    window_var = tk.Tk()
    window_var.title("Input of measurment settings")

    exit = tk.Button(window_var, text="Close", command=window_var.quit)
    # exit.pack#(side=RIGHT) #TOP (default), BOTTOM, LEFT, or RIGHT.
    exit.grid(row=1, column=1)

    # window.mainloop()


def Varify_meas_set(variable="hallo"):
    # print("Varify_meas_set")
    logger_function.debug("Varify_meas_set from logging.debug")
    logger_function.warning("Varify_meas_set from logging.debug")
    #config = configparser.ConfigParser()
    # variable=config.read("config.cfg")

    # print(type(variable[0]))


def simple_label(text_unit, column, row):
    lable_text = tk.Label(text=text_unit)
    lable_text.place(x=column, y=row, width=40, height=30)
    return lable_text


def get_info_dialog():
    m_text = "\
    ************************\n\
    Autor: Philipp MALIN\n\
    Date: 01.07.2021\n\
    Version: 0.02\n\
    Description: Program to control \n\
    ************************"
    tk.messagebox.showinfo(message=m_text, title="Info")


def error_window(text="TEST"):
    m_tesxt = " \n ! ! ! ! ! ! ! ! ! !\n\
    wrong input of value\n\
    value should be \n \n"
    m_tesxt = m_tesxt + text

    tk.messagebox.showerror(message=m_tesxt, title="Error")


def error_type_window(input_var, type_should=str, variable_name="", message_example="none"):
    m_tesxt = " \n Wrong input type \n"
    m_tesxt += variable_name+" input: " + \
        input_var + " is type: " + str(type(input_var)) + "\n"
    m_tesxt += "It should be: " + str(type_should) + "\n"
    m_tesxt += "correct input and retry \n \n"
    m_tesxt += "example: "+message_example

    tk.messagebox.showerror(message=m_tesxt, title="input type Error")


def round_rectangle(x1, y1, x2, y2, radius=25):
    # draw a box

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    #my_rectangle = round_rectangle(600, 600, 800, 800, radius=5)
    #canvas.create_polygon(my_rectangle, smooth=True,fill="blue")

    # return canvas.create_polygon(points, **kwargs, smooth=True)
    return points

# class TextHandler(logging.Handler):
#    print("TextHandler")
#    """This class logs to a Tkinter Text or ScrolledText widget"""
#    def __init__(self, text):
#        # run the regular Handler __init__
#        logging.Handler.__init__(self)
#        # Store a reference to the Text it will log to
#        self.text = text
#
#    def emit(self, record):
#        msg = self.format(record)
#        def append():
#            self.text.configure(state='normal')
#            self.text.insert(tk.END, msg + '\n')
#            self.text.configure(state='disabled')
#            # Autoscroll to the bottom
#            self.text.yview(tk.END)
#        # This is necessary because we can't modify the Text from other threads
#        self.text.after(0, append)
#    #https://gist.github.com/moshekaplan/c425f861de7bbf28ef06


if __name__ == "__main__":
    print("import of package")
    # Add the handler to logger
