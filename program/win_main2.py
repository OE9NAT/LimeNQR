import win_plot
import win_seq_own
import win_seq_spin
import win_seq_puls
from function import *
from tkinter import scrolledtext   # use for logger
import tkinter as tk
import PIL.Image as image

import tkinter.ttk as TTK  # use for Combobox
from PIL import ImageTk, Image  # .jpg

import logging  # DEBUG INFO WARNING ERROR
#from logging.handlers import QueueHandler
# logging.basicConfig(filename="../log/win_main_log.log",
#    level=logging.DEBUG, # <- set logging level
#    format="%(asctime)s - %(name)s : %(levelname)s : \n %(message)s") # set level


logger_win_main = logging.getLogger('win_main')
logger_win_main.addHandler(logging.StreamHandler())
logger_win_main.info("logging from win_main2 start up")


if 'setting_dict' not in locals():
    print("my setting_dict dose not exist")

    path_setting = os.path.abspath(os.path.dirname(sys.argv[0]))
    setting_dict = load_setting(path_setting, file="/program/setting.cfg")
    #setting_dict=load_setting (path_setting)

    print("\nsetting_dict:", *setting_dict.items(), sep="\n\n")
    freq_start = (setting_dict["setting"]["freq_start"])
    freq_end = (setting_dict["setting"]["freq_end"])
    #freq_step = tk.StringVar(setting_dict["setting"] ["freq_step"])
    #freq_average = tk.StringVar(setting_dict["setting"] ["freq_repetitions"])

    freq_start = "123"
    freq_end = "123"
    freq_step = "123"
    freq_average = "123"

    #freq_start = StringVar(window, value=freq_start)
freq_start_num = "123xxxx"


# read and save input vales from GUI and save it to config.cfg file
def save_values(cfg_section="pre_set_values"):
    global input_values
    input_values = {}
    print("save input_values to config.cfg file to: " + cfg_section)

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

    print("loadet all", input_values)

    # read and write to config.cfg
    config = configparser.ConfigParser()
    try:
        with open("config.cfg", "r") as configfile:
            print("####### ___ config.read")
            # config.read("config.cfg")

        print("_____________________ TEST pre ______________________")
        print("types of sections avalibel ____ \n", config.sections())
        print("types of options avalibel of option ___ ",
              config.has_option(cfg_section, "file_path"))
        print("_____________________ TEST after ______________________")

        if config.has_section(cfg_section):  # config.has_option(section, option)
            print(".cfg section exist")
            config[cfg_section] = input_values
            logging.info('Values were saved and overwritten')
        else:
            print(".cfg section dose not exist")
            config.add_section(cfg_section)
            config[cfg_section] = input_values
            logging.info('Values were saved and new written')

    except IOError:
        print("generated new .cfg file")
        config[cfg_section] = input_values
        logging.info('Values were saved and written to a new file')

    with open("config.cfg", "w") as configfile:
        config.write(configfile)
    logging.info('save_values end ')
    # return input_values


def load_values(path="config.cfg", section="pre_set_values"):
    #configParser = configparser.ConfigParser()
    # configParser.read(path)
    # print(configParser.get(section,"freq_start"))
    # print(configParser.items(section))
    print("_____________loaded all data in "+path+section)
    #
    # freq_start_input.delete(0,tk.END)
    # freq_start_input.insert(1,configParser.get(section,"freq_start"))
    # freq_end_input.delete(0,tk.END)
    # freq_end_input.insert(1,configParser.get(section,"freq_end"))
    # freq_step_input.delete(0,tk.END)
    # freq_step_input.insert(1,configParser.get(section,"freq_step"))
    # average_input.delete(0,tk.END)
    # average_input.insert(1,configParser.get(section,"average"))
    # Tune_U_max_input.delete(0,tk.END)
    # Tune_U_max_input.insert(1,configParser.get(section,"Tune_U_max"))
    # Match_U_max_input.delete(0,tk.END)
    # Match_U_max_input.insert(1,configParser.get(section,"Match_U_max"))
    # V_step_input.delete(0,tk.END)
    # V_step_input.insert(1,configParser.get(section,"V_step"))
    # puls_input.delete(0,tk.END)
    # puls_input.insert(1,configParser.get(section,"puls"))
    # Dwell_t_input.delete(0,tk.END)
    # Dwell_t_input.insert(1,configParser.get(section,"Dwell_t"))
    # seq_steps_input.delete(0,tk.END)
    # seq_steps_input.insert(1,configParser.get(section,"seq_steps"))
    # source_pw_input.delete(0,tk.END)
    # source_pw_input.insert(1,configParser.get(section,"source_pw"))
    # file_path_input.delete(0,tk.END)
    # file_path_input.insert(1,configParser.get(section,"file_path"))

    logging.info('Values were correktly imported')


# def puls_sequenz():
#    file_path=file_path_input.get()
#    experiment_path=experiment_path_input.get()
#    cycle_path=cycle_path_input.get()
#
#    windows_file(file_path,experiment_path,cycle_path)

def test():
    loglevel_console.set("INFO")
    print(loglevel_console.get())
    log_text = "text to be instertet in scolbar"+"\n"+loglevel_console.get() + \
        " \n"
    logtext_area.insert(tk.INSERT, log_text)


# def window_main():
class window_main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # main window
        logger_win_main.info("start__ win_main2 start class window_main init")
        #self = tk.Tk()
        self.title(
            "Magnetic Resonance Imaging - Contrast Agent Analyser Controller - Main")
        # self.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
        log_path = "@/" + \
            os.path.abspath(os.path.dirname(
                sys.argv[0])) + "/program/stethoskop.xbm"
        # linux
        log_path = os.path.abspath(os.path.dirname(
            sys.argv[0])) + "/program/stethoskop.xbm"
        self.wm_iconbitmap(bitmap=log_path)
        # Fensterbreite,hoehe, on secreen offset x, on screen offset y
        self.geometry("1000x750+100+10")
        self.option_add("Helvetica", '10')  # Frischart und groesse
        # self.resizable(width=False, height=False) #  False = no resize

        self.minsize(380, 380)  # (width_minsize=1200, height_minsize=800)
        self.maxsize(1200, 850)

        self.update()
        # self.update_idletasks()
        logger_win_main.info("win_main2 start class window_main init")

        #######----- Pull-down-Menu ------##########

        menuleiste = tk.Menu(self)

        datei_menu = tk.Menu(menuleiste, tearoff=0)
        datei_menu.add_command(label="Save", command=save_values)
        datei_menu.add_command(label="Save all", command=print(
            "test save all"))  # save_all)
        datei_menu.add_command(label="Close all", command=save_quit_all)
        datei_menu.add_separator()  # Trennlinie
        datei_menu.add_command(label="load values", command=load_values)
        datei_menu.add_command(
            label="spacer_1", command=print("test space_1"))  # save_all)
        datei_menu.add_command(
            label="spacer_2", command=print("test space_2"))  # save_all)
        # Drop-down generieren
        menuleiste.add_cascade(label="Datei", menu=datei_menu)

        help_menu = tk.Menu(menuleiste, tearoff=0)
        help_menu.add_command(label="Info!", command=get_info_dialog)
        help_menu.add_command(label="Error message !", command=error_window)
        help_menu.add_command(label="Error value !",
                              command=lambda:  error_window(" max feq"))
        help_menu.add_command(label="test loglevel", command=test)
        # Drop-down generieren
        menuleiste.add_cascade(label="Help", menu=help_menu)

        seq_menu = tk.Menu(menuleiste, tearoff=1)
        seq_menu.add_command(
            label="seq spin", command=win_seq_puls.windows_file)
        seq_menu.add_command(
            label="seq puls", command=lambda: logger.info("dropdown sequenz puls"))
        seq_menu.add_command(label="seq own", command=win_seq_own.windows_file)
        # Drop-down generieren
        menuleiste.add_cascade(label="Sequenz", menu=seq_menu)

        self.config(menu=menuleiste)  # Menueleiste an Fenster uebergeben
        self.update()
        logger_win_main.info("win_main2 start class window_main menuleiste")

        frame_boarder = 4

        ######----- Measurement Settings ------######
        # frame_measure = tk.Frame(self, bg='grey') # width=100, height=300)
        # width=100, height=300)
        frame_measure = tk.LabelFrame(
            self, text="Measurment Settings", bg='grey')
        frame_measure.grid(row=0, column=0, padx=frame_boarder,
                           pady=frame_boarder, sticky="nsew")
        self.grid_rowconfigure(0, weight=1, minsize=240)  # splaten hoehe
        self.grid_columnconfigure(0, weight=1, minsize=280)  # spalten breite

        # start frequency
        #freq_start = tk.StringVar(self, value=freq_start_num)

        self.freq_start_lable = tk.Label(
            frame_measure, text="START frequency: ", background="green4")
        self.freq_start_lable.grid(row=1, column=0, padx=5, pady=5)
        # simple_label("MHz",270,100)

        self.freq_start_input = tk.Entry(
            frame_measure, textvariable=freq_start, justify="right", fg="black", bg="white", width=10)
        self.freq_start_input.grid(
            row=1, column=1, sticky="ew", padx=5, pady=5)
        self.freq_start_input.insert(0, "000")
        tk.Label(frame_measure, text="MHz").grid(row=1, column=2)
        self.freq_start_input.focus()

        # end frequency
        self.freq_end_lable = tk.Label(
            frame_measure, text="END frequency: ", background="red4")
        self.freq_end_lable.grid(row=2, column=0, padx=5, pady=5)
        # simple_label("MHz",270,150)

        self.freq_end_input = tk.Entry(
            frame_measure, justify="right", fg="black", bg="white", width=10)
        self.freq_end_input.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.freq_end_input.insert(0, "000")
        tk.Label(frame_measure, text="MHz").grid(row=2, column=2, padx=3)

        # freq Steps
        self.freq_step_lable = tk.Label(
            frame_measure, text="frequency steps: ", background="dark goldenrod")
        self.freq_step_lable.grid(row=3, column=0, padx=5, pady=5)
        # simple_label("steps",270,200)
        tk.Label(frame_measure, text="step").grid(row=3, column=2, padx=3)

        self.freq_step_input = tk.Entry(
            frame_measure, justify="right", fg="black", bg="white", width=10)
        self.freq_step_input.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # average
        self.average_lable = tk.Label(
            frame_measure, text="average: ", background="dark goldenrod")
        self.average_lable.grid(row=4, column=0, padx=5, pady=5)
        tk.Label(frame_measure, text="step").grid(row=4, column=2, padx=3)

        self.average_input = tk.Entry(
            frame_measure, justify="right", fg="black", bg="white", width=10)
        self.average_input.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # Butten RUN measurement
        self.button_run = tk.Button(
            frame_measure, text="RUN measurment", command=self.set_measur, foreground="green")
        self.button_run.grid(row=5, column=0, rowspan=3,
                             padx=5, pady=5, columnspan=2)

        ######----- Tune&Match Settings ------######
        frame_tm = tk.LabelFrame(self, text="Tune&Match Settings", bg='grey')
        frame_tm.grid(row=0, column=1, padx=frame_boarder,
                      pady=frame_boarder, sticky="nsew")
        self.grid_rowconfigure(1, weight=1, minsize=240)
        self.grid_columnconfigure(1, weight=1, minsize=280)

        # Tune U_max
        self.Tune_U_max_lable = tk.Label(frame_tm, text="Tune U_max: ")
        self.Tune_U_max_lable.grid(row=0, column=0, padx=5, pady=5)
        # simple_label("V",620,100)
        tk.Label(frame_tm, text="V").grid(row=0, column=0, padx=3)

        self.Tune_U_max_input = tk.Entry(
            frame_tm, fg="black", bg="white", width=10)
        self.Tune_U_max_input.grid(row=0, column=1, padx=5, pady=5)

        # Match U_max
        self.Match_U_max_lable = tk.Label(frame_tm, text="Match U_max  : ")
        self.Match_U_max_lable.grid(row=1, column=0, padx=5, pady=5)

        self.Match_U_max_input = tk.Entry(
            frame_tm, fg="black", bg="white", width=10)
        self.Match_U_max_input.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_tm, text="V").grid(row=1, column=2, padx=3)

        # Voltage steps
        self.V_step_lable = tk.Label(frame_tm, text="Number of freq. : ")
        self.V_step_lable.grid(row=2, column=0, padx=5, pady=5)

        self.V_step_input = tk.Entry(
            frame_tm, fg="black", bg="white", width=10)
        self.V_step_input.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_tm, text="V").grid(row=2, column=2, padx=3)

        # LUT Size
        self.LUT_lable = tk.Label(frame_tm, text="LUT Size :")
        self.LUT_lable.grid(row=3, column=0, padx=5, pady=5)

        self.LUT_input = tk.Entry(frame_tm, fg="black", bg="white", width=10)
        self.LUT_input.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_tm, text="step").grid(row=3, column=2, padx=3)

        # Buttens
        self.send_TMfile = tk.Button(
            frame_tm, text="Read TM-file", command=RUN, foreground="red4")
        self.send_TMfile.grid(row=4, column=0, padx=5, pady=5)

        self.send_TMfile = tk.Button(
            frame_tm, text="Send to Arduino", command=RUN, foreground="green")
        self.send_TMfile.grid(row=4, column=1, padx=5, pady=5, columnspan=1)

        ######----- load sequence  ------######
        frame_seq = tk.LabelFrame(self, text="load sequence", bg='grey')
        frame_seq.grid(row=0, column=2, padx=frame_boarder,
                       pady=frame_boarder, sticky="nsew")
        self.grid_rowconfigure(2, weight=1, minsize=240)
        self.grid_columnconfigure(2, weight=1, minsize=280)

        # Filepath for Storage for loading data
        file_path_lable = tk.Label(frame_seq, text="path: ")
        file_path_lable.grid(row=0, column=0, padx=5, pady=5)

        file_path_input = tk.Entry(frame_seq, fg="black", bg="white", width=10)
        file_path_input.grid(row=0, column=1, padx=5, pady=5)

        # Filepath for Storage for loading data
        experiment_path_lable = tk.Label(frame_seq, text="experiment: ")
        experiment_path_lable.grid(row=1, column=0, padx=5, pady=5)

        experiment_path_input = tk.Entry(
            frame_seq, fg="black", bg="white", width=10)
        experiment_path_input.grid(row=1, column=1, padx=5, pady=5)

        # Filepath for Storage for loading data
        cycle_path_lable = tk.Label(frame_seq, text="cycle: ")
        cycle_path_lable.grid(row=2, column=0, padx=5, pady=5)

        cycle_path_input = tk.Entry(
            frame_seq, fg="black", bg="white", width=10)
        cycle_path_input.grid(row=2, column=1, padx=5, pady=5)

        puls_button = tk.Button(frame_seq, text="set Puls sequenz",
                                command=win_seq_puls.windows_file)  # windows_file)
        puls_button.grid(row=3, column=0, columnspan=2, padx=2, pady=2)

        spin_button = tk.Button(frame_seq, text="set Spin sequenz",
                                command=win_seq_spin.windows_file)  # windows_file)
        spin_button.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

        own_button = tk.Button(frame_seq, text="set own sequenz",
                               command=win_seq_own.windows_file)  # windows_file)
        own_button.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

        self.update()
        logger_win_main.info(
            "win_main2 start class window_main lable and button")

        ######----- Plotter  ------######
        #btn = tk.Label(self, text='A simple plot', foreground="green",background="white", font=("Arial Bold", 15))
        #btn.place(x = 10, y = 350, width=200, height=30)
        frame_plot = tk.Frame(self, bg='grey')  # , width=100, height=300, )
        frame_plot.grid(row=1, column=1, sticky="nsew",
                        columnspan=2, rowspan=2, padx=2, pady=2)

        plot_text = tk.Label(frame_plot, text="Results of last run",
                             foreground="green", background="white", font=("Arial Bold", 10))
        plot_text.grid(row=0, sticky="ew")

        print("start ploting")
        # t = np.arange(0.0, 2.0, 0.01)
        # s1 = np.sin(2*np.pi*t)
        # s2 = np.sin(4*np.pi*t)
        #
        # #fig = plt.figure(figsize=(1, 2))
        # fig = plt.figure()
        # fig.set_size_inches(6, 4.0, forward=True)
        # #fig.savefig('test2png.png', dpi=100)
        # # set the spacing between subplots
        # plt.subplots_adjust(left=0.07,bottom=0.06,right=0.99,top=0.9,wspace=0.4,hspace=0.4)
        #
        #
        # time_plot=plt.subplot(211)
        # plt.plot(t, s1)
        # time_plot.title.set_text("Time")
        # plt.grid()
        #
        #
        # feq_plot=plt.subplot(212)
        # plt.plot(t, 2*s1)
        # feq_plot.title.set_text("Frequency")
        # plt.grid()

        # specify the window as master
        canvas = FigureCanvasTkAgg(self.plot_live(), master=frame_plot)
        canvas.get_tk_widget().grid(row=1, padx=2, pady=2)  # ,columnspan=3,rowspan=20)
        canvas.draw()
        #canvas.get_tk_widget().place(x = 10, y = 360, width=500, height=400)
        # canvas.get_tk_widget().grid(row=1, column=0)#,columnspan=2)

        # navigation toolbar for the Plot
        toolbarFrame = tk.Frame(master=frame_plot)
        toolbarFrame.grid(row=2, padx=2, pady=2)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

        #toolbarFrame = tk.Frame(master=frame_plot)
        #toolbarFrame.place(x = 50, y = 760, width=450, height=35)

        #toolbar = NavigationToolbar2Tk(canvas, master=frame_plot)
        #toolbarFrame.grid(row=2, column=0,sticky="ew")

        logger_win_main.info("win_main2 start class window_main plot update")

        # return
        ######----- Logger  ------######
        frame_logger = tk.Frame(self, bg='grey')
        frame_logger.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        file_path_lable = tk.Label(
            frame_logger, text="debug logger: ", foreground="green", background="black")
        file_path_lable.grid(row=0, column=0)

        # Create a combobbox to select the logging level
        loglevel_console = tk.StringVar()
        loglevel_console.set("DEBUG")
        #loglevel = tk.StringVar(self,'DEBUG')
        combobox = TTK.Combobox(frame_logger, width=35, textvariable=loglevel_console, values=[
                                'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        #textvariable=level ,state='readonly'
        combobox.current(0)
        combobox.grid(row=1, column=0, sticky="ew")

        logtext_area = tk.scrolledtext.ScrolledText(
            frame_logger, width=30, height=8, font=("Times New Roman", 10))
        #scrollbar = Scrollbar(self,width = 30, height = 8,font = ("Times New Roman",15))
        #logtext_area = Listbox(self, yscrollcommand = scrollbar.set )
        logtext_area.grid(row=2, column=0, sticky="nsew")

        #text_handler = TextHandler(logtext_area)
        # Add the handler to logger
        #logger = logging.getLogger()
        # logger.addHandler(text_handler)

        logger_win_main.info("win_main2 start class window_main logger")

        ######----- Buttens  ------######
        frame_Buttens = tk.Frame(self, bg='grey')
        frame_Buttens.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")
        butons_y = 700  # hight of buttens

        button_run = tk.Button(frame_Buttens, text="RUN",
                               command=load_values(), background="chartreuse4")
        button_run.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        close_button = tk.Button(
            frame_Buttens, text="Test", background="SkyBlue4", command=lambda: print("hi"))
        close_button.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        plot_button = tk.Button(
            frame_Buttens, text="ploter", command=win_plot.win_plot)  # windows_file)
        plot_button.grid(row=2, column=0, padx=2, pady=2, sticky="ew")

        exit_button = tk.Button(
            frame_Buttens, text="Close", background="tomato4", command=self.destroy)
        # exit_button = tk.Button(self, text="Beenden", command=self.quit)#.destroy) #self.quit
        exit_button.grid(row=3, column=0, padx=2, pady=2, sticky="ew")

        ### ----- final settings --####
        # self.average_input.focus() #where curser should be set for the uer

        print('end of window_main init')
        logger_win_main.info("__ END win_main2 start class window_main ")
        self.update_idletasks()
        # return self

    def set_measur(self, start="10000", stop="20000", step="1000", average="100"):
        self.freq_start_input.delete("0", "end")
        self.freq_start_input.insert(0, start)
        self.freq_end_input.delete("0", "end")
        self.freq_end_input.insert(0, str(stop))
        self.freq_step_input.delete("0", "end")
        self.freq_step_input.insert(0, str(step))
        self.average_input.delete("0", "end")
        self.average_input.insert(0, str(average))

    def plot_live(self, s1="", t1="", s2="", t2=""):
        t = np.arange(0.0, 2.0, 0.01)
        s1 = np.sin(2*np.pi*t)
        s2 = np.sin(4*np.pi*t)

        #fig = plt.figure(figsize=(1, 2))
        fig = plt.figure()
        fig.set_size_inches(6, 4.0, forward=True)
        #fig.savefig('test2png.png', dpi=100)
        fig.set_canvas(self)

        # set the spacing between subplots
        plt.subplots_adjust(left=0.07, bottom=0.06, right=0.99,
                            top=0.9, wspace=0.4, hspace=0.4)

        time_plot = plt.subplot(211)
        plt.plot(t, s1)
        time_plot.title.set_text("Time")
        plt.grid()

        feq_plot = plt.subplot(212)
        plt.plot(t, 2*s1)
        feq_plot.title.set_text("Frequency")
        plt.grid()

        #file = filedialog.askopenfilename(initialdir='/home/',title='select .h5 file to plot')
        file = "/home/pi/Bach_arbeit/signals_TEST/live_scan_data.csv"

        csv = np.genfromtxt(file, delimiter=",")
        print("csv file", csv)

        import csv
        with open(file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        # with open(file,'r') as dest_f:
            print("test")
            # data_iter = csv.reader(dest_f,delimiter=' ')#,quotechar = '"')
            data = [data for data in spamreader]
        print("data .csv/n", *data)

        return fig

    def close():
        print("save and close all windows")
        self.destroy()


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
    # logging.config.fileConfig(filename="../log/win_main_log.log", level=logging.DEBUG, # <- set logging level
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
