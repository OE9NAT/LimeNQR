import logging  # DEBUG INFO WARNING ERROR
import csv
import win_plot
import win_seq_own
import win_seq_spin
import win_seq_puls
from function import *
from tkinter import scrolledtext   # use for logger
from tkinter import filedialog
import tkinter as tk
import PIL.Image as image

import tkinter.ttk as TTK  # use for Combobox
from PIL import ImageTk, Image  # .jpg

import variables
value_set = variables.Value_Settings()
print(value_set._freq_start)
logo_path = value_set.logo_path
# logo_path = "program/icon_logo.xbm"

# read from settings.cfg
var_setting = value_set.import_setting
# # setter
# value_set.set_freq = (22, 22, 22, 22)
# print("get start", value_set._freq_start)
# # getter
# print("getter", value_set.get_freq)

# Dokumentation of experiment
file_set = variables.File_Settings()
file_setting = file_set.save_experiment

##############

handler = logging.FileHandler("log/Value_log.log")
# handler = logging.handlers.RotatingFileHandler("log/Value_log.log")
formatter = logging.Formatter(
    "____ %(name)s ____  %(asctime)s : %(levelname)s : \n %(message)s")
handler.setFormatter(formatter)


logger_win_main = logging.getLogger('win_main')
logger_win_main.addHandler(logging.StreamHandler())
logger_win_main.info("logging from win_main2 start up")

logger_value = logging.getLogger("value")
logger_value.setLevel(logging.DEBUG)
logger_value.addHandler(handler)
# logger_value.addHandler(logging.StreamHandler())

logger_value.debug('This is an error message')
logger_value.info("start value logger")
logger_value.warning("start value logger")
logger_value.error('This is an error message')
logger_value.critical('This is an error message')


logger_setting = logging.getLogger("settings")
logger_setting.setLevel(logging.DEBUG)
logger_setting.addHandler(handler)
# logger_setting.addHandler(logging.StreamHandler())

logger_setting.info("start settings logger")


if 'setting_dict' not in locals():
    print("my setting_dict dose not exist")

    path_setting = os.path.abspath(os.path.dirname(sys.argv[0]))
    setting_dict = load_setting(path_setting, file="/program/setting.cfg")
    # setting_dict=load_setting (path_setting)

    print("\nsetting_dict:", *setting_dict.items(), sep="\n\n")
    freq_start = setting_dict["setting"]["freq_start"]
    freq_end = (setting_dict["setting"]["freq_end"])
    # freq_step = tk.StringVar(setting_dict["setting"] ["freq_step"])
    # freq_average = tk.StringVar(setting_dict["setting"] ["freq_repetitions"])

    freq_start = "123"
    freq_end = "123"
    freq_step = "123"
    freq_average = "123"

    # freq_start = StringVar(window, value=freq_start)
freq_start_num = "123xxxx"


def load_values(path="config.cfg", section="pre_set_values"):
    # configParser = configparser.ConfigParser()
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


# def window_main():
class window_main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # main window
        logger_win_main.info("start__ win_main2 start class window_main init")
        # self = tk.Tk()
        self.title(
            "Magnetic Resonance Imaging - Contrast Agent Analyse Controller - Main")
        # self.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
        self.wm_iconbitmap(bitmap=logo_path)
        # try:
        #     # for linux
        #     log_path = "@/" + \
        #         os.path.abspath(os.path.dirname(
        #             sys.argv[0])) + "/program/stethoskop.xbm"
        #     self.wm_iconbitmap(bitmap=log_path)
        # except:
        #     # for windows
        #     log_path = os.path.abspath(os.path.dirname(
        #         sys.argv[0])) + "/program/stethoskop.xbm"
        #     self.wm_iconbitmap(bitmap=log_path)
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
        datei_menu.add_command(label="Save", command=self.get_values)
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
        help_menu.add_command(label="test loglevel",
                              command=lambda: self.debug_logtext())
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

        ######----- contant ------######
        frame_boarder = 4

        ######----- Measurement Settings ------######
        # self.frame_measure = tk.Frame(self, bg='grey') # width=100, height=300)
        # width=100, height=300)
        self.frame_measure = tk.LabelFrame(
            self, text="Measurment Settings", bg='grey')
        self.frame_measure.grid(row=0, column=0, padx=frame_boarder,
                                pady=frame_boarder, sticky="nsew")
        self.grid_rowconfigure(0, weight=1, minsize=240)  # splaten hoehe
        self.grid_columnconfigure(0, weight=1, minsize=280)  # spalten breite

        # start frequency
        # freq_start = tk.StringVar(self, value=freq_start_num)

        self.freq_start_lable = tk.Label(
            self.frame_measure, text="START frequency: ")
        self.freq_start_lable.grid(row=1, column=0, padx=5, pady=5)
        # simple_label("MHz",270,100)

        self.freq_start_input = tk.Entry(
            self.frame_measure, textvariable=freq_start, justify="right", fg="black", bg="white", width=10)
        self.freq_start_input.grid(
            row=1, column=1, sticky="ew", padx=5, pady=5)
        self.freq_start_input.insert(0, "000")
        tk.Label(self.frame_measure, text="MHz").grid(row=1, column=2)
        self.freq_start_input.focus()

        # end frequency
        self.freq_end_lable = tk.Label(
            self.frame_measure, text="END frequency: ")
        self.freq_end_lable.grid(row=2, column=0, padx=5, pady=5)
        # simple_label("MHz",270,150)

        self.freq_end_input = tk.Entry(
            self.frame_measure, justify="right", fg="black", bg="white", width=10)
        self.freq_end_input.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.freq_end_input.insert(0, "000")
        tk.Label(self.frame_measure, text="MHz").grid(row=2, column=2, padx=3)

        # freq Steps
        self.freq_step_lable = tk.Label(
            self.frame_measure, text="frequency steps: ")
        self.freq_step_lable.grid(row=3, column=0, padx=5, pady=5)
        # simple_label("steps",270,200)
        tk.Label(self.frame_measure, text="step").grid(row=3, column=2, padx=3)

        self.freq_step_input = tk.Entry(
            self.frame_measure, justify="right", fg="black", bg="white", width=10)
        self.freq_step_input.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # average
        self.average_lable = tk.Label(
            self.frame_measure, text="average: ")
        self.average_lable.grid(row=4, column=0, padx=5, pady=5)
        tk.Label(self.frame_measure, text="step").grid(row=4, column=2, padx=3)

        self.average_input = tk.Entry(
            self.frame_measure, justify="right", fg="black", bg="white", width=10)
        self.average_input.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # Butten save settings to settings.cfg
        self.button_run = tk.Button(
            self.frame_measure, text="save settings", command=self.save_measurment, foreground="green")
        self.button_run.grid(row=5, column=0, rowspan=1,
                             padx=5, pady=5, sticky="ew")

        # Butten load settings from settings.cfg
        self.button_last_run = tk.Button(
            self.frame_measure, text="load settings", command=self.load_settings)
        self.button_last_run.grid(row=7, column=0,
                                  padx=5, pady=5, sticky="ew")

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
        tk.Label(frame_tm, text="V").grid(row=0, column=2, padx=3)

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
            frame_tm, text="Read TM-file", command=lambda: self.read_tm(), foreground="red4")
        self.send_TMfile.grid(row=4, column=0, padx=5, pady=5)

        self.send_TMfile = tk.Button(
            frame_tm, text="Send to Arduino", command=self.send_arduino, foreground="green")
        self.send_TMfile.grid(row=4, column=1, padx=5, pady=5, columnspan=1)

        ######----- load sequence  ------######
        frame_seq = tk.LabelFrame(self, text="load sequence", bg='grey')
        frame_seq.grid(row=0, column=2, padx=frame_boarder,
                       pady=frame_boarder, sticky="nsew")
        self.grid_rowconfigure(2, weight=1, minsize=240)
        self.grid_columnconfigure(2, weight=1, minsize=280)

        # Filepath for Storage for loading data
        self.file_path_lable = tk.Label(frame_seq, text="path: ")
        self.file_path_lable.grid(row=0, column=0, padx=5, pady=5)

        self.file_path_input = tk.Entry(
            frame_seq, fg="black", bg="white", width=10)
        self.file_path_input.grid(row=0, column=1, padx=5, pady=5)

        # Filepath for Storage for loading data
        experiment_path_lable = tk.Label(frame_seq, text="experiment: ")
        experiment_path_lable.grid(row=1, column=0, padx=5, pady=5)

        self.experiment_path_input = tk.Entry(
            frame_seq, fg="black", bg="white", width=10)
        self.experiment_path_input.grid(row=1, column=1, padx=5, pady=5)

        # Filepath for Storage for loading data
        cycle_path_lable = tk.Label(frame_seq, text="cycle: ")
        cycle_path_lable.grid(row=2, column=0, padx=5, pady=5)

        self.cycle_path_input = tk.Entry(
            frame_seq, fg="black", bg="white", width=10)
        self.cycle_path_input.grid(row=2, column=1, padx=5, pady=5)

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
        # btn = tk.Label(self, text='A simple plot', foreground="green",background="white", font=("Arial Bold", 15))
        # btn.place(x = 10, y = 350, width=200, height=30)
        frame_plot = tk.Frame(self, bg='grey')  # , width=100, height=300, )
        frame_plot.grid(row=1, column=1, sticky="nsew",
                        columnspan=2, rowspan=2, padx=2, pady=2)

        plot_text = tk.Label(frame_plot, text="Results of last run",
                             foreground="green", background="white", font=("Arial Bold", 10))
        plot_text.grid(row=0, column=0, columnspan=2, sticky="ew")

        print("start ploting")

        # specify the window as master
        self.canvas = FigureCanvasTkAgg(self.plot_live(), master=frame_plot)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=2, pady=2, sticky="nsew",
                                         columnspan=2)  # ,columnspan=3,rowspan=20)
        self.canvas.draw()
        # canvas.get_tk_widget().place(x = 10, y = 360, width=500, height=400)
        # canvas.get_tk_widget().grid(row=1, column=0)#,columnspan=2)

        # navigation toolbar for the Plot
        toolbarFrame = tk.Frame(master=frame_plot)
        toolbarFrame.grid(row=2, column=0, padx=2, pady=2)  # ,sticky="ew")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)

        button_reload = tk.Button(frame_plot, text="Reload plot",
                                  command=self.plot_update, background="chartreuse4")
        button_reload.grid(row=2, column=1, padx=2, pady=2, sticky="ew")

        logger_win_main.info("win_main2 start class window_main plot update")

        # return
        ######----- Logger  ------######
        frame_logger = tk.Frame(self, bg='grey')
        frame_logger.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        file_path_lable = tk.Label(
            frame_logger, text="debug logger: ", foreground="green", background="black")
        # .grid(row=0, column=0)
        file_path_lable.pack(fill="x", padx=2, pady=2)

        # Create a combobbox to select the logging level
        self.loglevel_console = tk.StringVar()
        self.loglevel_console.set("DEBUG")
        # loglevel = tk.StringVar(self,'DEBUG')
        combobox = TTK.Combobox(frame_logger, width=35, textvariable=self.loglevel_console, values=[
                                'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        # textvariable=level ,state='readonly'
        combobox.current(0)
        combobox.pack(fill="x", padx=2, pady=2)  # .grid(row=1 sticky="ew")

        self.logtext_area = tk.scrolledtext.ScrolledText(
            frame_logger, width=30, height=12, font=("Times New Roman", 10))
        # scrollbar = Scrollbar(self,width = 30, height = 8,font = ("Times New Roman",15))
        # logtext_area = Listbox(self, yscrollcommand = scrollbar.set )
        # .grid(row=2)#, sticky="nsew")
        self.logtext_area.pack(fill="x", padx=2, pady=2)

        # text_handler = TextHandler(logtext_area)
        # Add the handler to logger
        # logger = logging.getLogger()
        # logger.addHandler(text_handler)

        logger_win_main.info("win_main2 start class window_main logger")

        ######----- Buttens  ------######
        frame_Buttens = tk.Frame(self, bg='grey')
        frame_Buttens.grid(row=1, padx=2, pady=2, sticky="nsew")

        button_run = tk.Button(frame_Buttens, text="Load last run",
                               command=load_values())
        button_run.pack(fill="x", padx=2, pady=2)

        button_run = tk.Button(frame_Buttens, text="RUN ",
                               command=load_values())
        button_run.pack(fill="x", padx=2, pady=2)

        Filestrukture = tk.Button(
            frame_Buttens, text="Filestrukture", command=lambda: file_set.save_experiment())
        Filestrukture .pack(fill="x", padx=2, pady=2)

        plot_button = tk.Button(
            frame_Buttens, text="PLOT", command=win_plot.win_plot)
        plot_button.pack(fill="x", padx=2, pady=2)

        exit_button = tk.Button(
            frame_Buttens, text="Save & Close", command=save_quit_all)  # self.destroy)
        # exit_button = tk.Button(self, text="Beenden", command=self.quit)#.destroy) #self.quit
        # .grid(row=3,  padx=2, pady=2, sticky="ew")
        exit_button.pack(fill="x", padx=2, pady=2)

        Filestrukture = tk.Button(frame_Buttens, text="Test",
                                  background="SkyBlue4", activebackground="red", command=lambda: print("Filestrukture"))
        Filestrukture .pack(fill="x", padx=2, pady=2)

        ### ----- final settings --####
        # self.average_input.focus() #where curser should be set for the uer

        print('end of window_main init')
        logger_win_main.info("__ END win_main2 start class window_main ")
        self.update_idletasks()

        # write all files form settings.cfg to entery
        self.load_settings()
        self.update()
        # return self

    def save_measurment(self):
        print("save_measurment to settings.cfg")

        value_set.save_settings = self.get_values()

        self.saved_poup = tk.Label(
            self.frame_measure, text='settings saved', font=(7), background="chartreuse4")
        self.saved_poup.grid(row=5, column=1, padx=5,
                             pady=5, sticky="ew", rowspan=2)
        self.saved_poup.after(3000, lambda: self.saved_poup.grid_forget())

    def load_settings(self):

        path_setting = os.path.abspath(os.path.dirname(sys.argv[0]))
        # setting_dict = load_setting(path_setting, file="/program/setting.cfg") # from helper funktion OLD.
        value_set.set_settings = os.path.join(
            path_setting, "program", "setting.cfg")

        freq_start = value_set.get_freq[0]
        freq_end = value_set.get_freq[1]
        freq_step = value_set.get_freq[2]
        freq_average = value_set.get_freq[3]

        logger_value.info("freq_start" + str(freq_start))
        logger_value.info("freq_end" + str(freq_end))
        logger_value.info("freq_step" + str(freq_step))
        logger_value.info("freq_average" + str(freq_average))

        self.set_measur(freq_start, freq_end, freq_step, freq_average)
        # set with pre set values for tuen and match
        self.set_tm(value_set.get_tunematch[0], value_set.get_tunematch[1],
                    value_set.get_tunematch[2], value_set.get_tunematch[3])
        # load sequence storage paths
        self.set_storage(
            value_set.get_load[0], value_set.get_load[1], value_set.get_load[2])

        # popup for settings loaded
        self.load_poup = tk.Label(
            self.frame_measure, text='settings loaded', font=(7), background="chartreuse4")
        self.load_poup.grid(row=7, column=1, padx=5,
                            pady=5, sticky="ew", rowspan=2)
        self.load_poup.after(3000, lambda: self.load_poup.grid_forget())

        # logger
        log_text = "Measurment settig loadet from settings.cfg"+"\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        logger_value.info(log_text)

    def set_measur(self, start=11, stop=22, step=33, average=44):
        self.freq_start_input.delete("0", "end")
        self.freq_start_input.insert(0, start)
        self.freq_end_input.delete("0", "end")
        self.freq_end_input.insert(0, str(stop))
        self.freq_step_input.delete("0", "end")
        self.freq_step_input.insert(0, str(step))
        self.average_input.delete("0", "end")
        self.average_input.insert(0, str(average))

        # logger
        log_text = "Measurment settig loadet "+"\n"
        log_text = log_text + " freq_start " + str(start) + "\n"
        log_text = log_text + " freq_end " + str(stop) + "\n"
        log_text = log_text + " freq_step " + str(step) + "\n"
        log_text = log_text + " freq_average " + str(average) + "\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        logger_value.info(log_text)

    def plot_live(self, s1="", t1="", s2="", t2=""):
        t = np.arange(0.0, 2.0, 0.01)
        s1 = np.sin(20*np.pi*t)
        s2 = np.sin(40*np.pi*t)

        # file = filedialog.askopenfilename(initialdir='/home/',title='select .h5 file to plot')
        # file = "/home/pi/Bach_arbeit/signals_TEST/live_scan_data.csv"

        file = "signals_TEST/live_scan_data.csv"
        # file_name = os.path.join(folder_signal, file)

        with open(file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            data = [data for data in spamreader]
        # print("data .csv\n", *data)

        # print("data firt list ", data[0])
        del data[0]  # ['frequency', 'amplitude'] remove description from colems

        data_fequency = [float(data[i][0]) for i, val in enumerate(data)]
        data_amplitude = [float(data[i][1]) for i, val in enumerate(data)]
        # print("data_feq", *data_fequency, sep="\n")
        # print("data_fequency",type(data_fequen[0])
        # print("data_amplitude",data_amplitude)

        # fig = plt.figure(figsize=(1, 2))
        self.fig = plt.figure()
        self.fig.set_size_inches(6, 4.0, forward=True)
        # fig.savefig('test2png.png', dpi=100)
        self.fig.set_canvas(self)

        # set the spacing between subplots
        plt.subplots_adjust(left=0.1, bottom=0.12, right=0.99,
                            top=0.9, wspace=0.4, hspace=0.6)

        self.time_plot = plt.subplot(211)
        self.time_line = self.time_plot.plot(t, s1)
        self.time_plot.title.set_text("Time")
        self.time_plot.set_xlabel('time [s]')
        self.time_plot.set_ylabel('Amplituden [V]')
        self.time_plot.grid()

        self.feq_plot = plt.subplot(212)
        self.feq_plot.plot(data_fequency, data_amplitude)
        self.feq_plot.title.set_text("Frequency")
        self.feq_plot.set_xlabel('Frequency [kHz]')
        self.feq_plot.set_ylabel('Amplituden [V]')
        self.feq_plot.grid()

        return self.fig

    def plot_update(self, file="signals_TEST/live_scan_data.csv"):
        print("update plot")
        logger_win_main.info("update plot from main")

        # for testing
        iterate_plot = np.random.uniform(low=1, high=10)
        print("iterate_plot ", iterate_plot)
        t = np.arange(0.0, 2.0, 0.01)
        s1 = np.sin(iterate_plot*10*np.pi*t)
        freq = np.arange(0, 100, 10)
        s2 = np.zeros(10)
        s2[int(iterate_plot)] = 20

        # call the clear method on your axes
        self.time_plot.clear()
        self.feq_plot.clear()

        # plot the new data
        self.time_plot.plot(t, s1)
        self.time_plot.title.set_text(
            "Time of new data ferq:" + str(iterate_plot))
        self.time_plot.set_xlabel('time [s]')
        self.time_plot.set_ylabel('Amplituden [V]')
        self.time_plot.grid()

        self.feq_plot.plot(freq, s2)
        self.feq_plot.title.set_text("Frequency")
        self.feq_plot.set_xlabel('Frequency [kHz]')
        self.feq_plot.set_ylabel('Amplituden [V]')
        self.feq_plot.grid()

        # call the draw method on your canvas
        self.canvas.draw()

        log_text = "Updatet live Plot"+" \n"
        self.logtext_area.insert(tk.INSERT, log_text)

    def read_tm(self):
        print("def read_tm")
        self.logtext_area.insert(tk.INSERT, "read tm-file\n")
        file = filedialog.askopenfilename(
            title='select Tune and Match file')  # initialdir='/home/',

        print("file path for tune and match\n ", file)
        self.debug_logtext("read_tm file : "+file)
        logger_setting.info("read_tm file : "+file)

        tune_value = 3.3
        match_value = 3.3
        tm_step_value = 50
        tm_lut_value = 20

        self.set_tm(tune_value, match_value, tm_step_value, tm_lut_value)

        text = "tune_value" + str(tune_value)
        text = text+"\nmatch_value" + str(match_value)
        text = text+"\ntm_step_value"+str(tm_step_value)
        text = text+"\ntm_lut_value"+str(tm_lut_value)
        text = text + "\nfiel path: "+file

        logger_value.info("tune_value" + str(tune_value))
        logger_value.info("match_value" + str(match_value))
        logger_value.info("tm_step_value" + str(tm_step_value))
        logger_value.info("tm_lut_value" + str(tm_lut_value))

        logger_win_main.info("def read_tm "+text)

    def set_tm(self, tune=5, match=100, tm_step=100, lut=10):
        self.Tune_U_max_input.delete("0", "end")
        self.Tune_U_max_input.insert(0, tune)
        self.Match_U_max_input.delete("0", "end")
        self.Match_U_max_input.insert(0, match)
        self.V_step_input.delete("0", "end")
        self.V_step_input.insert(0, tm_step)
        self.LUT_input.delete("0", "end")
        self.LUT_input.insert(0, lut)

        # logger
        log_text = "Tune and Match settings set "+"\n"
        log_text = log_text + " tune " + str(tune) + "\n"
        log_text = log_text + " match " + str(match) + "\n"
        log_text = log_text + " tm_step " + str(tm_step) + "\n"
        log_text = log_text + " lut " + str(lut) + "\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        logger_value.info(log_text)

    def send_arduino(self):
        print("def send arduino")
        tune_value = self.Tune_U_max_input.get()
        match_value = self.Match_U_max_input.get()
        tm_step_value = self.V_step_input.get()
        tm_lut_value = self.LUT_input.get()
        # print("Tune_value ",Tune_value)

        # logger
        log_text = "send to Arduino "+"\n"
        log_text = log_text + " tune_value " + str(tune_value) + "\n"
        log_text = log_text + " match_value " + str(match_value) + "\n"
        log_text = log_text + " tm_step_value " + str(tm_step_value) + "\n"
        log_text = log_text + " tm_lut_value " + str(tm_lut_value) + "\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        logger_value.info(log_text)

        logger_win_main.info("def send_arduino ")

    # read and save input vales from GUI and save it to config.cfg file
    def get_values(self):
        print("TEST get_values")

        print("get input_values from win_main ")

        self.import_values = {}
        self.import_values["freq"] = {"freq_start": self.freq_start_input.get(), "freq_end": self.freq_end_input.get(),
                                      "freq_step": self.freq_step_input.get(), "freq_repetitions": self.average_input.get()}
        self.import_values["tunematch"] = {"tune": self.Tune_U_max_input.get(
        ), "match": self. Match_U_max_input.get(), "step": self.V_step_input.get(), "lut": self.V_step_input.get()}
        self.import_values["load"] = {"sample": self.file_path_input.get(
        ), "experiment": self.experiment_path_input.get(), "data": self.experiment_path_input.get()}

        self.experiment_path_input

        print("loadet all", self.import_values.keys())
        print("loadet all", self.import_values)

        return self.import_values

    def set_storage(self, path="test_path", experiment="test_exper", cycle="test_cycle"):
        self.file_path_input.delete("0", "end")
        self.file_path_input.insert(0, path)
        self.experiment_path_input.delete("0", "end")
        self.experiment_path_input.insert(0, experiment)
        self.cycle_path_input.delete("0", "end")
        self.cycle_path_input.insert(0, cycle)

        # logger
        log_text = "set storage "+"\n"
        log_text = log_text + " path " + path + "\n"
        log_text = log_text + " experiment " + experiment + "\n"
        log_text = log_text + " cycle " + cycle + "\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        logger_value.info(log_text)

    def debug_logtext(self, text="test"):
        # self.loglevel_console.set("INFO from debug_logtext")
        print(self.loglevel_console.get())
        if text == "test":
            log_text = "test loglevel_console: "+self.loglevel_console.get() + " \n"
        else:
            log_text = text + "\n"
        self.logtext_area.insert(tk.INSERT, log_text)
        self.logtext_area.see(tk.END)

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

    # script_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    win_main = window_main()
    win_main.mainloop()

print("-_____END layout____-")
