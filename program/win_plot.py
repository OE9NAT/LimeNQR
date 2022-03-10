import data2plot
import configparser
import os
import sys
from tkinter import filedialog
from tkinter import scrolledtext   # use for logger
import tkinter as tk
import PIL.Image as image

import tkinter.ttk as TTK  # use for Combobox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image  # .jpg


import logging  # DEBUG INFO WARNING ERROR

import variables
value_set = variables.Value_Settings()
logo_path = value_set.logo_path


logger_win_main = logging.getLogger('win_main')
logger_win_main.addHandler(logging.StreamHandler())
logger_win_main.info("logging from win_main2 start up")


def open_file():
    file = filedialog.askopenfilename(initialdir='/home/', title='philipp')
    print("\n selected file: \n", file)
    return file


def open_folder():
    folder = filedialog.askdirectory(initialdir='/home/', title='philipp')
    print("\n selected folder: \n", folder)
    return folder


def win_plot():
    print("win_plot")
    ######----- Setup of gui ------######
    window_plot = tk.Tk()
    window_plot.title(
        "Magnetic Resonance Imaging - Contrast Agent Analyse Controller - win_plot")

    window_plot.wm_iconbitmap(bitmap=logo_path)

    # window_main.wm_iconbitmap(bitmap="@/home/pi/Desktop/Bach_arbeit/stethoskop.xbm")
    # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_plot.geometry("1200x1000+200+100")
    window_plot.option_add("Helvetica", '10')  # Frischart und groesse
    # window_main.resizable(width=False, height=False) #  False = no resize

    window_plot.minsize(380, 380)  # (width_minsize=1200, height_minsize=800)
    #window_plot.maxsize(1200, 1100)

    window_plot.grid_columnconfigure(0, weight=1, minsize=300)
    window_plot.grid_columnconfigure(1, weight=1, minsize=300)
    window_plot.grid_rowconfigure(0, weight=1, minsize=50)
    window_plot.grid_rowconfigure(1, weight=1, minsize=10)

    #######----- Title, Outlines, Shape ------##########

    # Title
    frame_title = tk.Frame(window_plot, bg='grey')
    frame_title.grid(row=0, column=0, sticky="nsew",
                     padx=2, pady=2, columnspan=1)

    #"red" "orange" "yellow" "green" "blue" "purple" "white" "black"
    lable_text = tk.Label(frame_title, text="Re-Evaluate & Visualisation",
                          foreground="green", background="black", font=("Helvetica", 30))
    lable_text.pack(fill="x", padx=2, pady=2)

    # Pull-down-Menu
    menuleiste = tk.Menu(window_plot)

    datei_menu = tk.Menu(menuleiste, tearoff=0)
    datei_menu.add_command(label="Save", command=print("test save"))
    datei_menu.add_command(label="Save all", command=print(
        "test save all"))  # save_all)
    datei_menu.add_command(label="Close all", command=quit)
    datei_menu.add_separator()  # Trennlinie
    datei_menu.add_command(label="load values", command=print("load_values"))
    datei_menu.add_command(
        label="spacer_1", command=print("test space_1"))  # save_all)
    datei_menu.add_command(
        label="spacer_2", command=print("test space_2"))  # save_all)
    # Drop-down generieren
    menuleiste.add_cascade(label="Datei", menu=datei_menu)

    help_menu = tk.Menu(menuleiste, tearoff=0)
    help_menu.add_command(label="Info!", command=print("get_info_dialog"))
    help_menu.add_command(label="Error message !",
                          command=print("error_window"))
    #help_menu.add_command(label="Error value !", command=lambda:  error_window (" max feq"))
    help_menu.add_command(label="test loglevel", command=print("ERROR"))
    # Drop-down generieren
    menuleiste.add_cascade(label="Help", menu=help_menu)

    window_plot.config(menu=menuleiste)  # Menueleiste an Fenster uebergeben

    ######----- Plotter  ------######
    frame_plot = tk.Frame(window_plot, bg='grey')
    frame_plot.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
    frame_plot.grid_rowconfigure(1, weight=1, minsize=10)
    frame_plot.grid_columnconfigure(1, weight=1, minsize=300)

    #t = np.arange(0.0, 2.0, 0.01)
    #s1 = np.sin(2*np.pi*t)
    #s2 = np.sin(4*np.pi*t)
#
    # plt.figure()
    #fig = plt.figure(figsize=(1, 2))
    ##fig = plt.figure()
    # set the spacing between subplots
    # plt.subplots_adjust(left=0.07, bottom=0.06, right=0.99,
    #                    top=0.9, wspace=0.4, hspace=0.4)
    #
    #time_plot = plt.subplot(211)
    #plt.plot(t, s1)
    # time_plot.title.set_text("Time")
    # plt.grid()
    #
    #feq_plot = plt.subplot(212)
    #plt.plot(t, 2*s1)
    # feq_plot.title.set_text("Frequency")
    # plt.grid()
    #
    #files = []
    ##folder_signal = "D:/UNI/Bacharbeit/lukas_bararbeit/signals"
    #folder_signal = "/home/pi/lukas_bararbeit/signals/"
    #
    # plot al data to file
    #plot_all = False
    # if plot_all:
    #    for file in os.listdir(folder_signal):
    #        if file.endswith(".h5"):
    #            file_name = os.path.join(folder_signal, file)
    #            # print(file_name,"\n")
    #            files.append(file_name)
    #
    #    for file in files:
    #        print("\n \n lopp test  \n \n ")
    #        print(file)
    #        fig = plot(file)

    # plotr on screen
    file = filedialog.askopenfilename(
        title='select signal .h5 file')  # initialdir='/home/'
    fig = data2plot.plot(file)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill="x", padx=2, pady=2)
    canvas.draw()

    def update_plot(canvas):

        file = filedialog.askopenfilename(
            title='select signal .h5 file')  # initialdir='/home/'

        for item in canvas.get_tk_widget().find_all():
            canvas.get_tk_widget().delete(item)

        print("test1 ____________________________________________")
        fig2 = data2plot.plot(file)

        canvas = FigureCanvasTkAgg(fig2, master=frame_plot)
        canvas.get_tk_widget().pack(fill="x", padx=2, pady=2)
        canvas.draw()
        print("test2 ____________________________________________")

    # navigation toolbar for the Plot
    toolbarFrame = tk.Frame(master=frame_plot)
    toolbarFrame.pack(fill="x", padx=2, pady=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    ######----- Buttens  ------######
    frame_butten = tk.Frame(window_plot, bg='grey')
    frame_butten.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
    frame_butten.grid_rowconfigure(1, weight=1, minsize=10)
    frame_butten.grid_columnconfigure(1, weight=1, minsize=300)
    butons_X = 1000  # hight of buttens

    button_val = tk.Button(frame_butten, text="select file", background="SkyBlue4",
                           command=lambda:  open_file())  # ,foreground="red")
    button_val.pack(fill="x", padx=2, pady=2)

    close_button = tk.Button(frame_butten, text="select folder",
                             background="SkyBlue4", command=lambda:  open_folder())
    close_button.pack(fill="x", padx=2, pady=2)

    button_run = tk.Button(frame_butten, text="Plot data",
                           command=lambda: update_plot(canvas), background="chartreuse4")
    button_run.pack(fill="x", padx=2, pady=2)

    exit_button = tk.Button(frame_butten, text="Close",
                            background="tomato4", command=window_plot.destroy)
    # exit_button = tk.Button(window_main, text="Beenden", command=window_main.quit)#.destroy) #window_main.quit
    exit_button.pack(fill="x", padx=2, pady=2)

    return window_plot


# show window, wait for user imput
if __name__ == "__main__":
    import sys
    import numpy as np
    import matplotlib
    import tkinter as tk
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)

    #from pre_file import *

    import os
    import configparser
    import PIL.Image as image

    #from function import *
    from data_read_2 import *

    window_main = win_plot()
    window_main.mainloop()

print("-_____END layout____-")
