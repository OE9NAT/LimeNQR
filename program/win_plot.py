print("-_____start win_plot_____-")

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
FigureCanvasTkAgg, NavigationToolbar2Tk)
import PIL.Image as image

import tkinter as tk
import tkinter.ttk as TTK #use for Combobox
from tkinter import scrolledtext   # use for logger
from PIL import ImageTk, Image  #.jpg

from tkinter import filedialog

import logging # DEBUG INFO WARNING ERROR 
#from logging.handlers import QueueHandler
#logging.basicConfig(filename="../log/win_main_log.log", 
#    level=logging.DEBUG, # <- set logging level
#    format="%(asctime)s - %(name)s : %(levelname)s : \n %(message)s") # set level
    

logger_win_main = logging.getLogger('win_main')
logger_win_main.addHandler(logging.StreamHandler())    
logger_win_main.info("logging from win_main2 start up")


import os
import configparser
import PIL.Image as image
from data_read_2 import *

def open_file():
    file = filedialog.askopenfilename(initialdir='/home/',title='philipp')
    print("\n selected file: \n",file)
    return file
    
def open_folder():
    folder = filedialog.askdirectory(initialdir='/home/',title='philipp')
    print("\n selected folder: \n",folder)
    return folder
    
        

def win_plot ():
    print("win_plot")
    ######----- Setup of gui ------###### 
    window_plot = tk.Tk()
    window_plot.title("GUI for bach")
    #window_main.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
    #window_main.wm_iconbitmap(bitmap="@/home/pi/Desktop/Bach_arbeit/stethoskop.xbm")
    window_plot.geometry("1200x1000+200+100") # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_plot.option_add("Helvetica", '10') # Frischart und groesse
    #window_main.resizable(width=False, height=False) #  False = no resize
    
    #window_main.minsize(380, 380) #(width_minsize=1200, height_minsize=800) 
    #window_main.maxsize(1200, 1100)
    
    #######----- Title, Outlines, Shape ------##########
    canvas = tk.Canvas(window_plot)
    canvas.pack()
    
    #Title
    #"red" "orange" "yellow" "green" "blue" "purple" "white" "black"
    lable_text = tk.Label(window_plot,text="Projekt Title ",foreground="green",background="black", font=("Helvetica", 30))
    lable_text.place(x = 450, y = 5, width=400, height=50)
    
    #Pull-down-Menu
    menuleiste = tk.Menu(window_plot)
    
    datei_menu = tk.Menu(menuleiste, tearoff=0)
    datei_menu.add_command(label="Save", command=print("test save"))
    datei_menu.add_command(label="Save all", command=print("test save all"))#save_all) 
    datei_menu.add_command(label="Close all", command=quit)
    datei_menu.add_separator() # Trennlinie 
    datei_menu.add_command(label="load values", command=print("load_values"))
    datei_menu.add_command(label="spacer_1", command=print("test space_1"))#save_all)
    datei_menu.add_command(label="spacer_2", command=print("test space_2"))#save_all)
    menuleiste.add_cascade(label="Datei", menu=datei_menu) #Drop-down generieren
    
    help_menu = tk.Menu(menuleiste, tearoff=0)
    help_menu.add_command(label="Info!", command=print("get_info_dialog"))
    help_menu.add_command(label="Error message !", command=print("error_window"))
    #help_menu.add_command(label="Error value !", command=lambda:  error_window (" max feq"))
    help_menu.add_command(label="test loglevel", command= print("ERROR"))
    menuleiste.add_cascade(label="Help", menu=help_menu) #Drop-down generieren
    
    
    window_plot.config(menu=menuleiste)     #Menueleiste an Fenster uebergeben
    
    
    ######----- Plotter  ------######
    #btn = tk.Label(window_main, text='A simple plot', foreground="green",background="white", font=("Arial Bold", 15))
    #btn.place(x = 10, y = 350, width=200, height=30)
    
    
    t = np.arange(0.0, 2.0, 0.01)
    s1 = np.sin(2*np.pi*t)
    s2 = np.sin(4*np.pi*t)
    
    plt.figure()
    fig = plt.figure(figsize=(1, 2))
    #fig = plt.figure()
    # set the spacing between subplots
    plt.subplots_adjust(left=0.07,bottom=0.06,right=0.99,top=0.9,wspace=0.4,hspace=0.4)
    
    
    time_plot=plt.subplot(211)
    plt.plot(t, s1)
    time_plot.title.set_text("Time")
    plt.grid()
    
    
    feq_plot=plt.subplot(212)
    plt.plot(t, 2*s1)
    feq_plot.title.set_text("Frequency")
    plt.grid()
    
    
    files= []
    #folder_signal = "D:/UNI/Bacharbeit/lukas_bararbeit/signals"
    folder_signal = "/home/pi/lukas_bararbeit/signals/"
    
    for file in os.listdir(folder_signal):
        if file.endswith(".h5"):
            file_name= os.path.join(folder_signal, file)
            #print(file_name,"\n")
            files.append(file_name)
            
    for file in files:
        print("\n \n lopp test  \n \n ")
        print (file)
        fig = plot (file)
        break
    
    ## specify the window as master
    canvas = FigureCanvasTkAgg(fig, master=window_plot)
    canvas.draw()
    canvas.get_tk_widget().place(x = 20, y = 60, width=800, height=800)
    
    ## navigation toolbar for the Plot
    toolbarFrame = tk.Frame(master=window_plot)
    toolbarFrame.place(x = 50, y = 820, width=450, height=35)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
    
    ######----- Buttens  ------######
    butons_X = 1000 # hight of buttens
    
    
    button_val = tk.Button(window_plot, text = "select file",background="SkyBlue4", command =lambda:  open_file())#,foreground="red")
    button_val.place(x = butons_X, y = 200, width=150, height=50)
    
    close_button = tk.Button(window_plot, text = "select folder",background="SkyBlue4", command =lambda:  open_folder())
    close_button.place(x = butons_X, y = 300, width=150, height=50)
    
    button_run = tk.Button(window_plot, text = "Plot data", command = lambda:  print("run"),background="chartreuse4")
    button_run.place(x = butons_X, y = 400, width=150, height=50)
    
    
    exit_button = tk.Button(window_plot, text="Close",background="tomato4", command=window_plot.destroy)
    #exit_button = tk.Button(window_main, text="Beenden", command=window_main.quit)#.destroy) #window_main.quit
    exit_button.place(x = butons_X, y = 500, width=150, height=50)
    
    return window_plot
    

# show window, wait for user imput
if __name__ == "__main__":
    import sys
    import numpy as np
    import matplotlib
    import tkinter as tk
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    

    #from pre_file import *
    
    import os
    import configparser
    import PIL.Image as image
    

    #from function import *
    from data_read_2 import *

    window_main = win_plot()
    window_main.mainloop()

print("-_____END layout____-")