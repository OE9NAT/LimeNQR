import sys
import numpy as np
import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
FigureCanvasTkAgg, NavigationToolbar2Tk)
import configparser
print("-_____start function____-")



def RUN():
    print("new window from def click_run")
    lable_text = tk.Label(text="RUN  ",foreground="green",background="black", font=("Arial Bold", 20))
    lable_text.grid(row=10, column=2 )
    
    window2 = tk.Tk()
    window2.title("Run in a Box")
    window2.geometry("100x600")
    window2.option_add("Helvetica", '10')
    
    window2.mainloop()
    
    window2_text = tk.Label(text="RUN Input: ",foreground="green")#,background="black")
    window2_text.grid(row=0, column=0)#, padx=50, pady=50)
    
    
def quit():
    print("quit() funktion closes all windows")
    sys.exit()
    


def variable_input_windows():
    window_var = tk.Tk()
    window_var.title("Input of measurment settings")
    
    exit = tk.Button(window_var, text="Close", command=window_var.quit)
    #exit.pack#(side=RIGHT) #TOP (default), BOTTOM, LEFT, or RIGHT.
    exit.grid(row=1, column=1)
    
    
    
    #window.mainloop()
    
def Varify_meas_set(variable="hallo"):
    print("test")
    config = configparser.ConfigParser()
    variable=config.read("config.cfg")
    
    print(type(variable[0]))

    
def simple_label(text_unit,column,row):
    lable_text = tk.Label(text=text_unit)
    lable_text.place(x = column, y = row, width=50, height=30)
    return lable_text
    
def action_get_info_dialog():
	  m_text = "\
    ************************\n\
    Autor: Philipp MALIN\n\
    Date: 01.07.2021\n\
    Version: 0.02\n\
    Description: Program to control THE machine\n\
    ************************"
	  messagebox.showinfo(message=m_text, title = "Infos")

    
if __name__ == "__main__":
    print("import of package")
    