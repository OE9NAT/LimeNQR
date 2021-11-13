print("-_____start main_win____-")

import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
FigureCanvasTkAgg, NavigationToolbar2Tk)
import PIL.Image as image
#from pre_file import *

#from function import *
#from puls_win import *


import tkinter as tk
import tkinter.ttk as TTK #use for Combobox
from tkinter import scrolledtext   # use for logger
from PIL import ImageTk, Image  #.jpg

import logging # DEBUG INFO WARNING ERROR 
#from logging.handlers import QueueHandler
#logging.basicConfig(filename="../log/win_main_log.log", 
#    level=logging.DEBUG, # <- set logging level
#    format="%(asctime)s - %(name)s : %(levelname)s : \n %(message)s") # set level
    

logger_win_main = logging.getLogger('win_main')
logger_win_main.addHandler(logging.StreamHandler())    
logger_win_main.info("logging from start up")

from function import *

if 'setting_dict' not in locals():
    print("my setting_dict dose not exist")

    path_setting=os.path.abspath(os.path.dirname(sys.argv[0]))
    setting_dict=load_setting (path_setting ,file="/program/setting.cfg")
    #setting_dict=load_setting (path_setting)
    
    print("\nsetting_dict:", *setting_dict.items(), sep="\n\n")
    freq_start =(setting_dict["setting"] ["freq_start"])
    freq_end = (setting_dict["setting"] ["freq_end"])
    #freq_step = tk.StringVar(setting_dict["setting"] ["freq_step"])
    #freq_average = tk.StringVar(setting_dict["setting"] ["freq_repetitions"])
    
    freq_start = "123"
    freq_end =  "123"
    freq_step =  "123"
    freq_average = "123"

    #freq_start = StringVar(window, value=freq_start)
freq_start_num = "123xxxx"

import win_seq_puls
import win_seq_spin
import win_seq_own
import win_plot


# read and save input vales from GUI and save it to config.cfg file
def save_values(cfg_section="pre_set_values"): 
    global input_values
    input_values={}
    print("save input_values to config.cfg file to: "+ cfg_section)
    
    input_values["freq_start"] = freq_start_input.get()
    input_values["freq_end"] = freq_end_input.get()
    input_values["freq_step"] = freq_step_input.get()
    input_values["average"] = average_input.get()
    input_values["Tune_U_max"] = Tune_U_max_input.get()
    input_values["Match_U_max"] = Match_U_max_input.get()
    input_values["V_step"] = V_step_input.get()
    input_values["puls"] = puls_input.get()
    input_values["Dwell_t"] = Dwell_t_input.get()
    input_values["seq_steps"] = seq_steps_input.get()
    input_values["source_pw"] = source_pw_input.get()
    input_values["file_path"] = file_path_input.get()
    

    print("loadet all",input_values)
    
    #read and write to config.cfg
    config = configparser.ConfigParser()
    try:
        with open("config.cfg", "r") as configfile:
            print("####### ___ config.read")
            #config.read("config.cfg")        
        
        print("_____________________ TEST pre ______________________")
        print("types of sections avalibel ____ \n",config.sections())
        print("types of options avalibel of option ___ ", config.has_option(cfg_section, "file_path"))
        print("_____________________ TEST after ______________________")
        
        if config.has_section(cfg_section): #config.has_option(section, option)
            print(".cfg section exist")     
            config[cfg_section]=input_values
            logging.info('Values were saved and overwritten')
        else:
            print(".cfg section dose not exist")
            config.add_section(cfg_section)
            config[cfg_section]=input_values
            logging.info('Values were saved and new written')
        
    except IOError:
        print("generated new .cfg file")
        config[cfg_section]=input_values
        logging.info('Values were saved and written to a new file')
        
    with open("config.cfg", "w") as configfile:
        config.write(configfile)
    logging.info('save_values end ')
    #return input_values
    
def load_values(path="config.cfg",section="pre_set_values"):
    #configParser = configparser.ConfigParser()
    #configParser.read(path)
    #print(configParser.get(section,"freq_start"))
    #print(configParser.items(section))
    print("_____________loaded all data in "+path+section)
    #
    #freq_start_input.delete(0,tk.END)
    #freq_start_input.insert(1,configParser.get(section,"freq_start"))
    #freq_end_input.delete(0,tk.END)
    #freq_end_input.insert(1,configParser.get(section,"freq_end"))
    #freq_step_input.delete(0,tk.END)
    #freq_step_input.insert(1,configParser.get(section,"freq_step"))
    #average_input.delete(0,tk.END)
    #average_input.insert(1,configParser.get(section,"average"))
    #Tune_U_max_input.delete(0,tk.END)
    #Tune_U_max_input.insert(1,configParser.get(section,"Tune_U_max"))
    #Match_U_max_input.delete(0,tk.END)
    #Match_U_max_input.insert(1,configParser.get(section,"Match_U_max"))
    #V_step_input.delete(0,tk.END)
    #V_step_input.insert(1,configParser.get(section,"V_step"))
    #puls_input.delete(0,tk.END)
    #puls_input.insert(1,configParser.get(section,"puls"))
    #Dwell_t_input.delete(0,tk.END)
    #Dwell_t_input.insert(1,configParser.get(section,"Dwell_t"))
    #seq_steps_input.delete(0,tk.END)
    #seq_steps_input.insert(1,configParser.get(section,"seq_steps"))
    #source_pw_input.delete(0,tk.END)
    #source_pw_input.insert(1,configParser.get(section,"source_pw"))
    #file_path_input.delete(0,tk.END)
    #file_path_input.insert(1,configParser.get(section,"file_path"))
    
    logging.info('Values were correktly imported')
    
    
def set_measurment(start="111",stop="222",step="333",average="444"):
    print("set_measurment", start, stop, step, average)
    #window_main.update_idletasks()
    
    print('test2')
    freq_start_input.delete(0, END)
    freq_start_input.insert(0,"1234")
    #freq_end_input.insert(0,str(stop))
    #freq_step_lable.insert(0,str(step))
    #average_input.insert(0,str(average))
    
    #freq_start.set(str(start))
    #freq_end.set(str(stop))
    #freq_step.set(str(step))
    #average.set(str(average))
    print('end funktion set_measurment')


#def puls_sequenz():
#    file_path=file_path_input.get()
#    experiment_path=experiment_path_input.get()
#    cycle_path=cycle_path_input.get()
#
#    windows_file(file_path,experiment_path,cycle_path)
    
def test():
  loglevel_console.set("INFO")
  print(loglevel_console.get())
  log_text = "text to be instertet in scolbar"+"\n"+loglevel_console.get() +" \n"
  logtext_area.insert(tk.INSERT,log_text)
  
  
def window_main():

    def set_measur(start="10000",stop="20000",step="1000",average="100"):
        freq_start_input.delete(0, "END")
        freq_start_input.insert(0,"1234")
        #freq_start_input.insert(0,str(start))
        #freq_end_input.insert(0,str(stop))
        #freq_step_input.insert(0,str(step))
        #average_input.insert(0,str(average))
       
    ## main window
    window_main = tk.Tk()
    window_main.title("Magnetic Resonance Imaging - Contrast Agent Analyser Controller")
    #window_main.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
    log_path = "@/"+os.path.abspath(os.path.dirname(sys.argv[0])) + "/program/stethoskop.xbm"
    window_main.wm_iconbitmap(bitmap=log_path) 
    window_main.geometry("1000x750+100+10") # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_main.option_add("Helvetica", '10') # Frischart und groesse
    #window_main.resizable(width=False, height=False) #  False = no resize
    
    window_main.minsize(380, 380) #(width_minsize=1200, height_minsize=800) 
    window_main.maxsize(1200, 850)
    
    window_main.update()
    #window_main.update_idletasks()
    
    #######----- Title, Outlines, Shape ------##########
    
    #Title
    #"red" "orange" "yellow" "green" "blue" "purple" "white" "black"
    lable_text = tk.Label(text="Main settings MRI CA-analyser ",foreground="green4",background="gray20", font=("Helvetica", 28))
    lable_text.place(x = 100, y = 5, width=800, height=50)
    
    #Pull-down-Menu
    menuleiste = tk.Menu(window_main)
    
    
    datei_menu = tk.Menu(menuleiste, tearoff=0)
    datei_menu.add_command(label="Save", command=save_values)
    datei_menu.add_command(label="Save all", command=print("test save all"))#save_all) 
    datei_menu.add_command(label="Close all", command=save_quit_all)
    datei_menu.add_separator() # Trennlinie 
    datei_menu.add_command(label="load values", command=load_values)
    datei_menu.add_command(label="spacer_1", command=print("test space_1"))#save_all)
    datei_menu.add_command(label="spacer_2", command=print("test space_2"))#save_all)
    menuleiste.add_cascade(label="Datei", menu=datei_menu) #Drop-down generieren
    
    help_menu = tk.Menu(menuleiste, tearoff=0)
    help_menu.add_command(label="Info!", command=get_info_dialog)
    help_menu.add_command(label="Error message !", command=error_window)
    help_menu.add_command(label="Error value !", command=lambda:  error_window (" max feq"))
    help_menu.add_command(label="test loglevel", command= test)
    menuleiste.add_cascade(label="Help", menu=help_menu) #Drop-down generieren
    
    
    seq_menu = tk.Menu(menuleiste, tearoff=1)
    seq_menu.add_command(label="seq spin", command=win_seq_puls.windows_file)
    seq_menu.add_command(label="seq puls", command=lambda: logger.info("dropdown sequenz puls"))
    seq_menu.add_command(label="seq own", command=win_seq_own.windows_file)
    menuleiste.add_cascade(label="Sequenz", menu=seq_menu) #Drop-down generieren
    
    window_main.config(menu=menuleiste)     #Menueleiste an Fenster uebergeben
    window_main.update()
    
    
    ######----- Measurement Settings ------######
    input_width=100
    text_input_height=30
    
    lable_text = tk.Label(window_main,text="Measurment Settings ",foreground="green",background="white", font=("Helvetica", 15))
    lable_text.place(x = 5, y = 60, width=300, height=30)
    
    
    # start frequency
    freq_start = tk.StringVar(window_main, value=freq_start_num)
    
    freq_start_lable = tk.Label(window_main,text="START frequency: ",background="green4")
    freq_start_lable.place(x = 5, y = 100, width=140, height=text_input_height)  
    simple_label("MHz",270,100)
    
    freq_start_input = tk.Entry(window_main,textvariable=freq_start,justify="right",fg="black", bg="white", width=40) #textvariable=freq_start
    freq_start_input.place(x = 170, y = 100, width=input_width, height=text_input_height)
    #freq_start_input.insert(0,"999")
    freq_start_input.focus()
    
    
    # end frequency
    freq_end_lable = tk.Label(window_main,text="END frequency: ",background="red4")
    freq_end_lable.place(x = 5, y = 150, width=140, height=text_input_height) 
    simple_label("MHz",270,150)
    
    freq_end_input = tk.Entry(window_main,justify="right",fg="black", bg="white", width=40)
    freq_end_input.place(x = 170, y = 150, width=input_width, height=text_input_height)
    freq_end_input.insert(0,"999")
    
    
    # freq Steps
    freq_step_lable = tk.Label(window_main,text="frequency steps: ",background="dark goldenrod")
    freq_step_lable.place(x = 5, y = 200, width=140, height=text_input_height) 
    simple_label("steps",270,200)
    
    freq_step_input = tk.Entry(window_main,justify="right",fg="black", bg="white", width=40)
    freq_step_input.place(x = 170, y = 200, width=input_width, height=text_input_height)
    
    # average
    average_lable = tk.Label(window_main,text="average: ",background="dark goldenrod")
    average_lable.place(x = 5, y = 250, width=140, height=text_input_height) 
    simple_label("steps",270,250)
    
    average_input = tk.Entry(window_main,justify="right",fg="black", bg="white", width=40)
    average_input.place(x = 170, y = 250, width=input_width, height=text_input_height)
    
    button_run = tk.Button(window_main, text = "RUN measurment", command = set_measur,foreground="green")
    button_run.place(x = 50, y = 300, width=200, height=50)
    
    ######----- Tune&Match Settings ------######
    lable_text = tk.Label(window_main, text="Tune&Match Settings",foreground="green",background="white", font=("Arial Bold", 15))
    lable_text.place(x = 355, y = 60, width=300, height=30)
    
    # Tune U_max
    Tune_U_max_lable = tk.Label(window_main, text="Tune U_max: ")
    Tune_U_max_lable.place(x = 360, y = 100, width=140, height=text_input_height) 
    simple_label("V",620,100)
    
    Tune_U_max_input = tk.Entry(window_main, fg="black", bg="white", width=40)
    Tune_U_max_input.place(x = 520, y = 100, width=input_width, height=text_input_height)
    
    
    # Match U_max 
    Match_U_max_lable = tk.Label(window_main, text="Match U_max  : ")
    Match_U_max_lable.place(x = 360, y = 150, width=140, height=text_input_height) 
    simple_label("V",620,150)
    
    Match_U_max_input = tk.Entry(window_main, fg="black", bg="white", width=40)
    Match_U_max_input.place(x = 520, y = 150, width=input_width, height=text_input_height)
    
    # Voltage steps
    V_step_lable = tk.Label(window_main,text="Number of freq. : ")
    V_step_lable.place(x = 360, y = 200, width=140, height=text_input_height) 
    simple_label("steps",620,200)
    
    V_step_input= tk.Entry(window_main,fg="black", bg="white", width=40)
    V_step_input.place(x = 520, y = 200, width=input_width, height=text_input_height)
    
    # LUT Size
    LUT_lable = tk.Label(window_main,text="LUT Size :")
    LUT_lable.place(x = 360, y = 250, width=140, height=text_input_height) 
    simple_label("steps",620,250)
    
    LUT_input= tk.Entry(window_main,fg="black", bg="white", width=40)
    LUT_input.place(x = 520, y = 250, width=input_width, height=text_input_height)
    
    #Buttens
    send_TMfile = tk.Button(window_main, text = "Read TM-file", command = RUN,foreground="red4")
    send_TMfile.place(x = 360, y = 300, width=140, height=50)
    
    send_TMfile = tk.Button(window_main, text = "Send to Arduino", command = RUN,foreground="green")
    send_TMfile.place(x = 510, y = 300, width=140, height=50)
    
    
    ## ????? canvas.create_line(0, 50, 600, 1000)#, dash=(4, 2))
    
    # ######----- Sequence  ------######
    # lable_text = tk.Label(text="Sequence Settings",foreground="green",background="white", font=("Arial Bold", 15))
    # lable_text.place(x = 800, y = 60, width=300, height=30)
    # 
    # # Pulse
    # 
    # pulse_lable = tk.Label(text="Pulse: ")
    # pulse_lable.place(x = 800, y = 100, width=160, height=text_input_height) 
    # puls_input = tk.Entry(fg="black", bg="white", width=40)
    # puls_input.place(x = 1000, y = 100, width=input_width, height=text_input_height)
    # 
    # # Dwell time
    # Dwell_t_lable = tk.Label(text="Dwell time: ")
    # Dwell_t_lable.place(x = 800, y = 150, width=160, height=text_input_height) 
    # 
    # Dwell_t_input = tk.Entry(fg="black", bg="white", width=40)
    # Dwell_t_input.place(x = 1000, y = 150, width=input_width, height=text_input_height)
    # 
    # # Nr. of Points
    # seq_steps_lable = tk.Label(text="Nr. of steps: ")
    # seq_steps_lable.place(x = 800, y = 200, width=160, height=text_input_height) 
    # simple_label("steps",1100,250)
    # 
    # seq_steps_input = tk.Entry(fg="black", bg="white", width=40)
    # seq_steps_input.place(x = 1000, y = 200, width=input_width, height=text_input_height)
    # 
    # # Source PW
    # source_pw_lable = tk.Label(text="Source PW: ")
    # source_pw_lable.place(x = 800, y = 250, width=160, height=text_input_height) 
    # 
    # source_pw_input = tk.Entry(fg="black", bg="white", width=40)
    # source_pw_input.place(x = 1000, y = 250, width=input_width, height=text_input_height)
    # simple_label("%",1100,250)
    

    ######----- load sequence  ------######
    #path="test_data", experiment="test_experiment_3",cycle="test_cycle_3"
    
    lable_text = tk.Label(window_main, text="File Settings",foreground="green",background="white", font=("Arial Bold", 15))
    lable_text.place(x = 695, y = 60, width=300, height=30)
    
    # Filepath for Storage for loading data
    file_path_lable = tk.Label(window_main, text="path: ")
    file_path_lable.place(x = 700, y = 100, width=140, height=text_input_height) 
    
    file_path_input = tk.Entry(window_main, fg="black", bg="white", width=40)
    file_path_input.place(x = 860, y = 100, width=130, height=text_input_height)
    
    
    # Filepath for Storage for loading data
    experiment_path_lable = tk.Label(window_main, text="experiment: ")
    experiment_path_lable.place(x = 700, y = 150, width=140, height=text_input_height) 
    
    experiment_path_input = tk.Entry(window_main, fg="black", bg="white", width=40)
    experiment_path_input.place(x = 860, y = 150, width=130, height=text_input_height)
    
    # Filepath for Storage for loading data
    cycle_path_lable = tk.Label(window_main, text="cycle: ")
    cycle_path_lable.place(x = 700, y = 200, width=140, height=text_input_height) 
    
    cycle_path_input = tk.Entry(window_main, fg="black", bg="white", width=40)
    cycle_path_input.place(x = 860, y = 200, width=130, height=text_input_height)
    
    
    puls_button = tk.Button(window_main, text="set Puls sequenz", command=win_seq_puls.windows_file)#windows_file) 
    puls_button.place(x = 800, y = 250, width=150, height=50)
    
    spin_button = tk.Button(window_main, text="set Spin sequenz", command=win_seq_spin.windows_file)#windows_file) 
    spin_button.place(x = 800, y = 300, width=150, height=50)
    
    own_button = tk.Button(window_main, text="set own sequenz", command=win_seq_own.windows_file)#windows_file) 
    own_button.place(x = 800, y = 350, width=150, height=50)
    
    plot_button = tk.Button(window_main, text="Plotter", command=win_plot.win_plot)#windows_file) 
    plot_button.place(x = 800, y = 400, width=150, height=50)
    
   
    ######----- Plotter  ------######
    #btn = tk.Label(window_main, text='A simple plot', foreground="green",background="white", font=("Arial Bold", 15))
    #btn.place(x = 10, y = 350, width=200, height=30)
    
    
    t = np.arange(0.0, 2.0, 0.01)
    s1 = np.sin(2*np.pi*t)
    s2 = np.sin(4*np.pi*t)
    
    #fig = plt.figure(figsize=(1, 2))
    fig = plt.figure()
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
    
 
    ## specify the window as master
    canvas = FigureCanvasTkAgg(fig, master=window_main)
    canvas.draw()
    canvas.get_tk_widget().place(x = 10, y = 360, width=500, height=400)
    
    ## navigation toolbar for the Plot
    toolbarFrame = tk.Frame(master=window_main)
    toolbarFrame.place(x = 50, y = 760, width=450, height=35)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    
    ######----- Logger  ------######
    
    file_path_lable = tk.Label(window_main,text="Logger: ",foreground="green",background="black")
    file_path_lable.place(x = 600, y = 450, width=100, height=text_input_height) 
    
    # Create a combobbox to select the logging level
    loglevel_console = tk.StringVar()
    loglevel_console.set("DEBUG")
    #loglevel = tk.StringVar(window_main,'DEBUG')
    combobox = TTK.Combobox(window_main,width=25,textvariable=loglevel_console,values=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']) 
    #textvariable=level ,state='readonly'
    combobox.current(0)
    combobox.place(x=700, y=450, width=100, height=text_input_height)
    
    logtext_area = tk.scrolledtext.ScrolledText(window_main,width = 30, height = 8,font = ("Times New Roman",10))
    #scrollbar = Scrollbar(window_main,width = 30, height = 8,font = ("Times New Roman",15))
    #logtext_area = Listbox(window_main, yscrollcommand = scrollbar.set )
    logtext_area.place(x=600, y=500, width=300, height=230)
    
    
    #text_handler = TextHandler(logtext_area)
    # Add the handler to logger
    #logger = logging.getLogger()
    #logger.addHandler(text_handler)
    
    ######----- Buttens  ------######
    butons_y = 700 # hight of buttens
    
    button_run = tk.Button(window_main, text = "RUN", command = load_values(),background="chartreuse4")
    button_run.place(x = 550, y = butons_y, width=150, height=50)
       
    close_button = tk.Button(window_main, text = "Test",background="SkyBlue4", command =lambda:  print("hi"))
    close_button.place(x = 700, y = butons_y, width=150, height=50)
    
    exit_button = tk.Button(window_main, text="Close",background="tomato4", command=window_main.destroy)
    #exit_button = tk.Button(window_main, text="Beenden", command=window_main.quit)#.destroy) #window_main.quit
    exit_button.place(x = 850, y = butons_y, width=150, height=50)
    
    ### ----- final settings --####
    average_input.focus() #where curser should be set for the uer
    
    
    print('test_1_end')
    window_main.update_idletasks()
    return window_main
  
    
    

# show window, wait for user imput
if __name__ == "__main__":
    import sys
    import numpy as np
    import matplotlib
    import tkinter as tk    
    import os
    import configparser
    import PIL.Image as image

    
    
#   from logging.handlers import QueueHandler
    #logging.config.fileConfig(filename="../log/win_main_log.log", level=logging.DEBUG, # <- set logging level
    #    format="%(name)s - %(asctime)s:%(levelname)s:%(message)s" , # set level
    #    disable_existing_loggers=False )
        

    
#    logging.basicConfig(filename="../log/win_main_log.log", 
#        level=logging.DEBUG, # <- set logging level
#        format="%(asctime)s - %(name)s : %(levelname)s : \n %(message)s") # set level
#        
#   
#    logger = logging.getLogger('win_main')
#    logger.addHandler(logging.StreamHandler())    
#    logger.info("logging from start up")
#    
#    from function import *
#    
#    if 'setting_dict' not in locals():
#        print("my setting_dict dose not exist")
#
#        path_setting=os.path.abspath(os.path.dirname(sys.argv[0]))
#        #setting_dict=load_setting (path_setting ,file="setting.cfg")
#        setting_dict=load_setting (path_setting)
#        #print("\nsetting_dict:", *setting_dict.items(), sep="\n\n")
#        
#        freq_start = setting_dict["setting"] ["freq_start"]
#        freq_end = setting_dict["setting"] ["freq_end"]
#        freq_step = setting_dict["setting"] ["freq_step"]
#        freq_repetitions = setting_dict["setting"] ["freq_repetitions"]
#    
#    
#    import win_seq_puls
#    import win_seq_spin
#    import win_seq_own
#    import win_plot
#
    
    if 'myVar' not in globals():
        print("my global Variable dose not exist")
        
    #script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
   
    
   

    win_main = window_main()
    win_main.mainloop()

print("-_____END layout____-")