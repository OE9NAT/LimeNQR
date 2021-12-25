
import variables
import os
import sys
import configparser
import PIL.Image as image

import tkinter as tk
import tkinter.ttk as TTK  # use for Combobox
from tkinter import scrolledtext   # use for logger
from PIL import ImageTk, Image  # .jpg

import logging  # DEBUG INFO WARNING ERROR
from logging.handlers import QueueHandler

logger_seq = logging.getLogger('win_sequenz')
logger_seq.addHandler(logging.StreamHandler())
logger_seq.info("logging from winsow sequenz at start up")

value_set = variables.Value_Settings()
logo_path = value_set.logo_path


class Seq_values:
    print("class Sequenz values setup")


class Window_seq:
    print("class Sequenz Window setup")
    frame_boarder = 4

    def __init__(self, seq_type, value_settings):
        # tk.Tk.__init__(self, *args, **kwargs)
        print("type of sequenz: ", seq_type)
        print("settings variables: \n \n", value_settings)

        target_freq = 100  # in MHz

        Window_seq.window_sequenz(self, seq_type)

    @staticmethod
    def window_sequenz(self, seq_type):
        # open GUI window and Present settings
        # sequenz window
        logger_seq.info("start win_sequenz.py start class logger_seq init")
        win_seq = tk.Tk()
        win_seq.title("Magnetic Resonance Imaging - Sequenz Manager")
        # win_seq.wm_iconbitmap(bitmap=logo_path)

        win_seq.geometry("1000x800")  # "1000x750+400+100"
        win_seq.minsize(380, 400)  # (width_minsize=1200, height_minsize=800)
        win_seq.maxsize(1200, 850)

        # zeilen hoehe
        win_seq.grid_rowconfigure(0, weight=1, minsize=60)  # zeilen hoehe
        win_seq.grid_rowconfigure(1, weight=4, minsize=100)  # zeilen hoehe
        win_seq.grid_rowconfigure(2, weight=8, minsize=100)  # zeilen hoehe
        win_seq.grid_rowconfigure(3, weight=4, minsize=50)  # zeilen hoehe
        # win_seq.grid_rowconfigure(4, weight=4, minsize=50)  # zeilen hoehe

        # spalten breite
        win_seq.grid_columnconfigure(0, weight=1, minsize=280)
        win_seq.grid_columnconfigure(1, weight=4, minsize=300)
        win_seq.grid_columnconfigure(2, weight=4, minsize=280)

        # Titile
        frame_title = tk.Frame(win_seq, bg="grey")
        frame_title.grid(columnspan=3, row=0, column=0, padx=Window_seq.frame_boarder,
                         pady=Window_seq.frame_boarder, sticky="nsew")
        lable_text = tk.Label(frame_title, text="Set Sequenz ",
                              foreground="green", background="OliveDrab4", font=("Helvetica", 30))
        lable_text.pack(fill="x")

        # Info box experiment strukture

        # plot sequenz
        frame_plot = tk.Frame(win_seq, bg="grey")
        frame_plot.grid(columnspan=2, row=1, column=1, padx=Window_seq.frame_boarder,
                        pady=Window_seq.frame_boarder, sticky="nsew")

        if seq_type == "fid":
            img_path = "/program/sequenz/puls_seq.JPG"
        if seq_type == "spin":
            img_path = "/program/sequenz/spin_seq.JPG"
        if seq_type == "comp":
            img_path = "/program/sequenz/puls_seq.JPG"
        if seq_type == "spin_phase":
            img_path = "/program/sequenz/puls_seq.JPG"
        else:
            # own sequenz
            img_path = "/program/sequenz/own_seq.JPG"

        image_path = os.path.abspath(os.path.dirname(
            sys.argv[0])) + img_path
        #image_path = "/home/pi/Bach_arbeit/program/sequenz/puls_seq.JPG"
        image = Image.open(image_path)
        image_puls = image.resize((750, 300))
        image_puls = ImageTk.PhotoImage(image_puls, master=win_seq)
        #image_puls = ImageTk.PhotoImage(Image.open(image_path))
        pic_label = tk.Label(frame_plot, image=image_puls)
        pic_label.pack(fill="both", expand="yes")
        pic_label.image = image_puls
        # pic_label.grid(columnspan=2, row=1, column=1, padx=Window_seq.frame_boarder,
        #               pady=Window_seq.frame_boarder, sticky="nsew")
        image.close()

        # inputbox
        # Time of Puls
        frame_puls = tk.LabelFrame(win_seq, text="Timing of Puls", bg='grey')
        frame_puls.grid(row=2, column=0, padx=Window_seq.frame_boarder,
                        pady=Window_seq.frame_boarder, sticky="nsew")

        frame_puls.grid_columnconfigure(0, weight=1)
        frame_puls.grid_columnconfigure(1, weight=1)
        # frame_puls.grid_rowconfigure(0, weight=1)
        # frame_puls.grid_rowconfigure(1, weight=1)
        # frame_puls.grid_rowconfigure(2, weight=1)
        # frame_puls.grid_rowconfigure(3, weight=1)

        if seq_type == "fid":
            print("own", seq_type)

            lable_info_puls = tk.Label(
                frame_puls, text="FID sequenz", bg='grey')
            lable_info_puls.grid(row=1, column=0)

        if seq_type == "spin":
            print("spin Echo sequenz =", seq_type)

            lable_info_spin = tk.Label(
                frame_puls, text="spin sequenz input", bg='grey')
            lable_info_spin.grid(row=0, column=0, sticky="ew")

            lable_info_sdr = tk.Label(
                frame_puls, text="Puls 1", bg='grey')
            lable_info_sdr.grid(row=1, column=0)
            p1 = tk.Entry(frame_puls, fg="black", bg="white")
            p1.grid(row=1, column=1, sticky="ew")

            lable_info_sdr = tk.Label(
                frame_puls, text="Delay 1", bg='grey')
            lable_info_sdr.grid(row=2, column=0)
            tp1 = tk.Entry(frame_puls, fg="black", bg="white")
            tp1.grid(row=2, column=1, sticky="ew")

            lable_info_sdr = tk.Label(
                frame_puls, text="Puls 2", bg='grey')
            lable_info_sdr.grid(row=3, column=0)
            p2 = tk.Entry(frame_puls, fg="black", bg="white")
            p2.grid(row=3, column=1, sticky="ew")

            lable_info_sdr = tk.Label(
                frame_puls, text="Delay 2", bg='grey')
            lable_info_sdr.grid(row=4, column=0)
            tp2 = tk.Entry(frame_puls, fg="black", bg="white")
            tp2.grid(row=4, column=1, sticky="ew")

        if seq_type == "comp":
            print("Composite Pulse", seq_type)

            lable_info_puls = tk.Label(
                frame_puls, text="Composit Puls sequenz", bg='grey')
            lable_info_puls.grid(row=1, column=0)

        if seq_type == "spin_phase":
            print("own", seq_type)

            lable_info_puls = tk.Label(
                frame_puls, text="Spin Echo Phase sequenz", bg='grey')
            lable_info_puls.grid(row=1, column=0)

        if seq_type == "own":
            print("own", seq_type)

        frame_readout = tk.LabelFrame(win_seq, text="Readout", bg='grey')
        frame_readout.grid(row=2, column=1, padx=Window_seq.frame_boarder,
                           pady=Window_seq.frame_boarder, sticky="nsew")

        lable_info_sdr = tk.Label(
            frame_puls, text="Test info readout", bg='grey')
        # lable_info_sdr.grid(row=2, column=0)

        seq_type

        # Readout
        frame_sdr = tk.LabelFrame(win_seq, text="SDR Settings", bg='grey')
        frame_sdr.grid(row=2, column=2, padx=Window_seq.frame_boarder,
                       pady=Window_seq.frame_boarder, sticky="nsew")

        lable_info_sdr = tk.Label(frame_sdr, text="Repetition time", padx=Window_seq.frame_boarder,
                                  pady=Window_seq.frame_boarder, bg='grey')
        lable_info_sdr.pack()

        lable_info_sdr = tk.Label(frame_sdr, text="RX gain", padx=Window_seq.frame_boarder,
                                  pady=Window_seq.frame_boarder, bg='grey')
        lable_info_sdr.pack()

        lable_info_sdr = tk.Label(frame_sdr, text="TX gain", padx=Window_seq.frame_boarder,
                                  pady=Window_seq.frame_boarder, bg='grey')
        lable_info_sdr.pack()

        lable_info_sdr = tk.Label(frame_sdr, text="RX low-pass", padx=Window_seq.frame_boarder,
                                  pady=Window_seq.frame_boarder, bg='grey')
        lable_info_sdr.pack()

        lable_info_sdr = tk.Label(frame_sdr, text="TX low-pass", padx=Window_seq.frame_boarder,
                                  pady=Window_seq.frame_boarder, bg='grey')
        lable_info_sdr.pack()

        # infobox
        info_box = tk.LabelFrame(win_seq, text="info box", bg='grey')
        info_box.grid(row=1, column=0, padx=Window_seq.frame_boarder,
                      pady=Window_seq.frame_boarder, sticky="nsew")

        self.lable_info_experiment = tk.Label(
            info_box, text="Test info text", bg='grey')
        self.lable_info_experiment.pack()

        # Buttens
        frame_Buttens = tk.Frame(win_seq, bg='grey')
        frame_Buttens.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

        button_run = tk.Button(frame_Buttens, text="load",
                               command=lambda: load_seq("test"))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="save",
                               command=lambda: save_seq("test"))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="test",
                               command=lambda: print("test"))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="close",
                               command=lambda: print("test"))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="right")

    def save_seq(var):
        print("save all variabels from impout")

    def save2cfg(self, file_path=os.path.dirname(sys.argv[0]), file="program/setting_sequenz.cfg"):
        print("save settings to .cfg file")
        path_settings = os.path.join(file_path, file)
        if not os.path.exists(path_settings):
            print("file Setting not found", path_settings)
            # path_settings = filedialog.askopenfilename(
            #    initialdir='/home/', title='select settings.cfg path')
        print("setting file: ", path_settings)

    def load_seq(var):
        print("load all variabels from .cfg file")

    def read2cfg(self, file_path=os.path.dirname(sys.argv[0]), file="program/setting_sequenz.cfg"):
        " read .cfg file from file "
        if not os.path.exists(path_settings):
            print("file Setting not found", path_settings)

        configParser = configparser.ConfigParser()
        configParser.read(path_settings)
        setting_dict = {section: dict(configParser.items(section))
                        for section in configParser.sections()}


class Seq_FID:
    def __init__(self, P1="10", TP1="20", TE1="30", TA="40"):  # **kwargs
        self.puls_1 = P1
        self.pulspause_1 = TP1
        self.echo_1 = TE1
        self.acquire = TA
        self.nr_puls = 1

        print("\n duration of 1st puls ", P1)
        print("\n duration of 1st puls pause ", TP1)
        print("\n duration of 1st Echo ", TE1)
        print("\n ___ \n time of Acquire ", TA)

    def add_puls(P, TP, TE):
        print("add puls to sequenz")

### save new experiment ###


def save_file(path, experiment="test_experiment_1", cycle="test_cycle_11"):
    print("def save")
    print("experiment" + experiment + "cycle" + cycle)

    cycle = path+"/"+experiment+"/"+cycle

    try:
        # os.mkdir(experiment)
        os.makedirs(cycle)
    except OSError as error:
        print("error file1 Experiment olready exists")
        logger_seq.error('error message')

    return "testing save"

# read and save input vales from GUI and save it to config.cfg file


def save_values(path="test_data", experiment="test_experiment", cycle="test_cycle"):
    cfg_section = "puls_sequenz"
    input_values = {}
    print("save to cfg_section: " + cfg_section)

    input_values["P_1"] = globals()["P_1_input"].get()
    input_values["TP_1"] = globals()["TP_1_input"].get()
    input_values["TA"] = globals()["TA_input"].get()

    path_lable.config(text="Seq. for data: "+path)
    experiment_lable.config(text="Seq. for experiment: "+experiment)
    cycle_lable.config(text="Seq. for cycle: "+cycle)

    logger_seq.info('load inputs from save_valsues ')
    print("loadet all in save_values", input_values)

    # read and write to config.cfg
    config = configparser.ConfigParser()

    # generate files
    save_file(path, experiment, cycle)
    config["filepath"] = {"path": path,
                          "experiment": experiment, "cycle": cycle}

    # save sequenz file
    cycle = path+"/"+experiment+"/"+"config.cfg"
    try:
        with open(cycle, "r") as configfile:
            print("####### ___"+cycle)
            # config.read("config.cfg")

        print("_____________________ TEST pre ______________________")
        print("available of file_path ___ ",
              config.has_option(cfg_section, "file_path"))
        print("available of puls_sequenz ___ ",
              config.has_option(cfg_section, "puls_sequenz"))
        print("types of sections avalibel ____ ", config.sections())
        # print("types of options avalibel of option ___ ", config.has_option(cfg_section, "file_path"))
        print("_____________________ TEST after ______________________")

        if config.has_section(cfg_section):  # config.has_option(section, option)
            print(".cfg section exist ", cycle)
            config[cfg_section] = input_values
            logger_seq.info('Values were saved and overwritten')
        else:
            print(".cfg section dose not exist")
            config.add_section(cfg_section)
            config[cfg_section] = input_values
            logger_seq.info('Values were saved and new written')

    except IOError:
        print("generated new .cfg file ", cycle)
        config[cfg_section] = input_values
        logger_seq.info('Values were saved and written to a new file')

    with open(cycle, "w") as configfile:
        print("## save .cfg to __", cycle)
        config.write(configfile)
    logger_seq.info('save_values end ')


### loading data from past experiments ####
def load_file(path="data", experiment="test_experiment", cycle="test_cycle"):
    print("load")
    print("path"+path+"experiment" + experiment + "cycle" + cycle)

    import tkinter as tk
    # import tkinter.ttk as TTK #use for Combobox

    ######----- Setup of gui ------######
    window_experiment = tk.Tk()
    window_experiment.title("load experiment")
    # window_experiment.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
    window_experiment.wm_iconbitmap(bitmap=logo_path)
    # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_experiment.geometry("600x520")
    window_experiment.option_add("Helvetica", '10')  # Frischart und groesse
    window_experiment.resizable(width=False, height=False)  # False = no resize
    text_input_height = 30

    def save_experiment():
        print("save all parameters to .cfg file")
        status_lable = tk.Label(window_experiment, text="updated sequenz !!")
        status_lable.place(x=10, y=250, width=500, height=text_input_height)

        # global experiment = {}
        experiment_dict["data"] = data.get()
        experiment_dict["experiment"] = experiment.get()
        experiment_dict["cycle"] = cycle.get()

        print(experiment_dict)

        path_lable.config(text="Seq. for data: "+experiment_dict["data"])
        experiment_lable.config(
            text="Seq. for experiment: "+experiment_dict["experiment"])
        cycle_lable.config(text="Seq. for cycle: "+experiment_dict["cycle"])

        save_values(
            experiment_dict["data"], experiment_dict["experiment"], experiment_dict["cycle"])
        print("end of save_experiment")

    # Title
    lable_text = tk.Label(window_experiment, text="Set Experiment strukture ",
                          foreground="green", background="OliveDrab4", font=("Helvetica", 30))
    lable_text.place(x=50, y=10, width=500, height=50)

    # Set parameters
    text_input_height = 40
    path_text = "Seq. for data: "+path
    path_lable = tk.Label(
        window_experiment, text=path_text, background="gray50")
    path_lable.place(x=50, y=100, width=500, height=text_input_height)

    experiment_text = "Seq. for experiment: "+experiment
    experiment_lable = tk.Label(
        window_experiment, text=experiment_text, background="gray50")
    experiment_lable.place(x=50, y=150, width=500, height=text_input_height)

    cycle_text = "Seq. for cycle: "+cycle
    cycle_lable = tk.Label(
        window_experiment, text=cycle_text, background="gray50")
    cycle_lable.place(x=50, y=200, width=500, height=text_input_height)

    # Experiment
    gray_light = "gray70"
    path_lable_input = tk.Label(
        window_experiment, text="Set Seq. data: ", background=gray_light)
    path_lable_input.place(x=50, y=300, width=300, height=40)
    data = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    data.place(x=350, y=300, width=200, height=40)

    experiment_lable_input = tk.Label(
        window_experiment, text="Set Seq. experiment: ", background=gray_light)
    experiment_lable_input.place(x=50, y=350, width=300, height=40)
    experiment = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    experiment.place(x=350, y=350, width=200, height=40)

    cycle_lable_input = tk.Label(
        window_experiment, text="Set Seq. cycle: ", background=gray_light)
    cycle_lable_input.place(x=50, y=400, width=300, height=40)
    cycle = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    cycle.place(x=350, y=400, width=200, height=40)

    # Buttons
    save_button = tk.Button(window_experiment, text="Save",
                            background="SkyBlue4", command=lambda:  save_experiment())
    save_button.place(x=50, y=450, width=140, height=50)

    save_button = tk.Button(window_experiment, text="load",
                            command=lambda: print("butten load"))
    save_button.place(x=230, y=450, width=140, height=50)

    close_button = tk.Button(window_experiment, text="Close",
                             background="tomato4", command=window_experiment.destroy)
    close_button.place(x=410, y=450, width=140, height=50)

    return print("closing load file")


def windows_file(path="test_data", experiment="test_experiment", cycle="test_cycle"):

    # helper function
    def simple_label(text_unit, column, row):
        lable_text = tk.Label(window_puls, text=text_unit)
        lable_text.place(x=column, y=row, width=50, height=30)
        return lable_text

    def nr_puls(cycle):
        print("number of cylce:", cycle)

        try:
            experiment_lable.destroy()
        except:
            print("no pulses")

        text_input_height = 30
        puls_y = 600

        pulses = list(range(1, cycle+1))

        x_min = 50
        x_max = 1000
        step = (x_max-x_min)/cycle

        for i, puls in enumerate(pulses):
            x_pos = (i*step)+x_min
            print(step, " x_pos ", x_pos)
            lable_puls = "puls "+str(puls)

            experiment_lable = tk.Label(
                window_puls, text=lable_puls, background="gray60")
            experiment_lable.place(
                x=x_pos, y=puls_y, width=50, height=text_input_height)

    # Parameters
    global experiment_dict
    experiment_dict = {}
    experiment_dict["data"] = path
    experiment_dict["experiment"] = experiment
    experiment_dict["cycle"] = cycle

    ######----- Setup of gui ------######
    window_puls = tk.Tk()
    window_puls.title("Set Puls")
    window_puls.wm_iconbitmap(bitmap=logo_path)
    # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_puls.geometry("1000x800+1000+100")
    window_puls.option_add("Helvetica", '10')  # Frischart und groesse
    window_puls.resizable(width=False, height=False)  # False = no resize

    # window_puls.minsize(380, 380) #(width_minsize=1200, height_minsize=800)
    # window_puls.maxsize(1200, 850)

    input_width = 100
    text_input_height = 30

    # Title
    lable_text = tk.Label(window_puls, text="Set Puls sequenz ",
                          foreground="green", background="gray70", font=("Helvetica", 30))
    lable_text.place(x=300, y=5, width=400, height=50)

    # Experiment
    path_text = "Seq. for data: "+path
    global path_lable
    path_lable = tk.Label(window_puls, text=path_text, background="gray60")
    path_lable.place(x=10, y=100, width=300, height=text_input_height)

    experiment_text = "Seq. for experiment: "+experiment
    global experiment_lable
    experiment_lable = tk.Label(
        window_puls, text=experiment_text, background="gray60")
    experiment_lable.place(x=340, y=100, width=300, height=text_input_height)

    cycle_text = "Seq. for cycle: "+cycle
    global cycle_lable
    cycle_lable = tk.Label(window_puls, text=cycle_text, background="gray60")
    cycle_lable.place(x=680, y=100, width=300, height=text_input_height)

    # numer of puls inputs
    cycle_lable = tk.Label(
        window_puls, text="set number \n of pulses: \n 1", background="gray60")
    cycle_lable.place(x=40, y=160, width=80, height=60)

    # picture

    image_path = os.path.abspath(os.path.dirname(
        sys.argv[0]))+"/program/sequenz/puls_seq.JPG"
    # image_path = "/home/pi/Bach_arbeit/program/sequenz/puls_seq.JPG"
    image = Image.open(image_path)
    image_puls = image.resize((750, 300))
    image_puls = ImageTk.PhotoImage(image_puls, master=window_puls)
    # image_puls = ImageTk.PhotoImage(Image.open(image_path))
    pic_label = tk.Label(window_puls, image=image_puls)
    pic_label.pack(fill="both", expand="yes")
    pic_label.image = image_puls
    pic_label.place(x=150, y=160)
    image.close()

    ### Input #
    unit_puls = "ms"

    # P_1
    P_1_lable = tk.Label(window_puls, text="P 1: ", background="gray50")
    P_1_lable.place(x=50, y=500, width=90, height=text_input_height)
    simple_label(unit_puls, 235, 500)

    globals()["P_1_input"] = tk.Entry(
        window_puls, fg="black", bg="white", width=40)
    P_1_input.place(x=150, y=500, width=input_width, height=text_input_height)

    # TP_1
    TP_1_lable = tk.Label(window_puls, text="TP 1: ", background="gray50")
    TP_1_lable.place(x=50, y=550, width=90, height=text_input_height)
    simple_label(unit_puls, 235, 550)

    globals()["TP_1_input"] = tk.Entry(
        window_puls, fg="black", bg="white", width=40)
    TP_1_input.place(x=150, y=550, width=input_width, height=text_input_height)

    # TA
    TA_lable = tk.Label(window_puls, text="TA: ", background="gray50")
    TA_lable.place(x=50, y=600, width=90, height=text_input_height)
    simple_label(unit_puls, 235, 600)

    globals()["TA_input"] = tk.Entry(
        window_puls, fg="black", bg="white", width=40)
    TA_input.place(x=150, y=600, width=input_width, height=text_input_height)

    ###_______ Buttens _________#
    butons_y = 700
    load_button = tk.Button(window_puls, text="Load sequenz", background="SkyBlue4",
                            command=lambda:  load_file(experiment_dict["data"], experiment_dict["experiment"], experiment_dict["cycle"]))
    load_button.place(x=50, y=butons_y, width=140, height=50)

    # save_button = tk.Button(window_puls, text="Save", background="SkyBlue4", command=lambda:  save_values(path,experiment,cycle))
    save_button = tk.Button(window_puls, text="Save", background="SkyBlue4",
                            command=lambda:  save_values(experiment_dict["data"], experiment_dict["experiment"], experiment_dict["cycle"]))

    save_button.place(x=210, y=butons_y, width=140, height=50)

    test_button = tk.Button(window_puls, text="test1", command=lambda: print(
        "test butten form Pulssequenz"))
    test_button.place(x=400, y=butons_y, width=150, height=50)

    test2_button = tk.Button(window_puls, text="test2",
                             command=window_puls.destroy)
    test2_button.place(x=600, y=butons_y, width=150, height=50)

    close_button = tk.Button(window_puls, text="Close",
                             background="tomato4", command=window_puls.destroy)  # quit)
    close_button.place(x=800, y=butons_y, width=150, height=50)

    # show window, wait for user imput
    # window_puls.mainloop()
    # return window_puls


# colour http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/700px-TkInterColorCharts.png
if __name__ == "__main__":
    # for testing
    print("-_____start import puls_win")
    import os
    import configparser
    import PIL.Image as image

    import logging  # DEBUG INFO WARNING ERROR
    from logging.handlers import QueueHandler
    # logger = logging.basicConfig(filename="logging.log", level=logging.DEBUG, # <- set logging level
    #          format="%(asctime)s:%(levelname)s:%(message)s"  ) # set level

    logger_seq = logging.getLogger(__name__)
    logger_seq.setLevel(logging.DEBUG)  # <- set logging level
    log_handler = logging.FileHandler("log_file.log")
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    log_handler.setFormatter(formatter)
    logger_seq.addHandler(log_handler)

    logger_seq.info("set upp logger in puls_win.py")

    import function

    print("-_____start puls_win")

    path = os.getcwd()
    print("The current working directory is %s" % path)

    print("__testrun_save_1__")

    testrun_save_1 = save_file("test__")
    print(testrun_save_1)

    print("__testrun_save_2__")
    testrun_save_2 = save_file("path__", "test_experiment_2", "test_cycle_2")
    print(testrun_save_2)

    print("__testrun_save_2__")
    # testrun_load_2 = load_file()
    # print(testrun_load_2)

    print("__testrun_save_2__")
    # testrun_load_2 = load_file("test_experiment_4","test_cycle_4")
    # print(testrun_load_2)

    print("test")
    win = windows_file(
        path="test_data", experiment="test_experiment_3", cycle="test_cycle_3")
    print("start")
    # win.mainloop()

    a, b, *c = (1, 2, 3, 4, 5)

    print("__ end pre_file.py__")
