import os
import sys
import tkinter as tk
from tkinter import filedialog
import numpy as np
import scipy
import configparser
import logging


logger_win_variables = logging.getLogger('win_variables')
logger_win_variables.addHandler(logging.StreamHandler())
logger_win_variables.info("logging from win_variables start up")


class Value_Settings:

    def __init__(self):
        print("Value_Settings")
        self._freq_start = 00
        self._freq_end = 00
        self._freq_step = 00
        self._freq_repetitions = 00

        self._tunematch_tune = 00
        self._tunematch_match = 00
        self._tunematch_freq = 00
        self._tunematch_lut = 00

        self._load_sample = "tu-graz"
        self._load_experiment = "Bismut"
        self._load_data = "FID"

        # get size of screen
        window = tk.Tk()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.title("get Window size")
        # window.geometry("400x400")

        print(type(screen_width))
        text = "breite: "+str(screen_width) + " hoehe: "+str(screen_height)
        print(text)

        # https://www.shareicon.net/stethoscope-medical-kit-clinic-hospital-medical-tool-medical-777051
        try:
            # for linux
            self._log_path = "@/" + \
                os.path.abspath(os.path.dirname(
                    sys.argv[0])) + "/program/icon_logo.xbm"
            window.wm_iconbitmap(bitmap=self._log_path)
        except:
            # for windows
            self._log_path = os.path.abspath(os.path.dirname(
                sys.argv[0])) + "\program\icon_logo.xbm"
            window.wm_iconbitmap(bitmap=self._log_path)
        window.destroy()
        print("path of logo: ", self._log_path)

    @staticmethod
    def hallo_word():
        print("hallo from variables.py class Value_settings")

    @property
    def import_setting(self, path=os.path.dirname(sys.argv[0]), file="program/setting.cfg"):
        # read settings form setting.cfg file
        # path_settings = path+"/"+file
        print("@property import_settings")
        path_settings = str(os.path.dirname(
            sys.argv[0]))+"/"+"program/setting.cfg"
        print("setting file: ", path_settings)
        if not os.path.exists(path_settings):
            print("file Setting not found")
            logger_function.warning(
                "function.py, def load_setting, path_settings not found")
            # raise TypeError ("file dose not exist \n"+path_settings)

            # look fore settings.cfg
            path_settings = filedialog.askopenfilename(
                initialdir='/home/', title='select settings.cfg path')
            print("setting file: ", path_settings)

        configParser = configparser.ConfigParser()
        configParser.read(path_settings)
        setting_dict = {section: dict(configParser.items(section))
                        for section in configParser.sections()}

        #self._freq_start = 11
        #self._freq_end = 11
        #self._freq_step = 11
        #self._freq_repetitions = 11
        #
        #self._tunematch_tune = 11
        #self._tunematch_match = 11
        #self._tunematch_freq = 11
        #self._tunematch_lut = 11
        #
        #self._load_sample = "sam"
        #self._load_experiment = "exp"
        #self._load_data = "Ech"

        # logging.info("Values loaded from load_setting")
        self.import_values = {}
        self.import_values["freq"] = {"freq_start": self._freq_start, "freq_end": self._freq_end,
                                      "freq_step": self._freq_step, "freq_repetitions": self._freq_repetitions}
        self.import_values["tunematch"] = {}
        self.import_values["load"] = {}

        print("import_values", type(self.import_values))

        return self.import_values

    @import_setting.setter
    def set_freq(self, value):
        print("setter value define_frequency", type(value))
        self._freq_start = value[0]  # start
        self._freq_end = value[1]  # stop
        self._freq_step = value[2]  # step
        self._freq_repetitions = value[3]  # reps

    @import_setting.getter
    def get_freq(self):
        print("getter variables.py get_freq")
        return [self._freq_start, self._freq_end, self._freq_step, self._freq_repetitions]

    @import_setting.setter
    def set_tunematch(self, value):
        print("setter value define_frequency", value)
        self._tunematch_tune = value[0]
        self._tunematch_match = value[1]
        self._tunematch_freq = value[2]
        self._tunematch_lut = value[3]

    @import_setting.getter
    def get_tunematch(self):
        print("getter variables.py get_freq")
        return [self._tunematch_tune, self._tunematch_match, self._tunematch_freq, self._tunematch_lut]

    @import_setting.setter
    def set_load(self, value):
        print("setter value define_frequency", value)
        self._load_sample = value[0]
        self._load_experiment = value[1]
        self._load_data = value[2]

    @import_setting.getter
    def get_load(self):
        print("getter variables.py get_freq")
        return [self._load_sample, self._load_experiment, self._load_data]

    # logo path
    @import_setting.getter
    def logo_path(self):
        print(self._log_path, "\n")
        return self._log_path

    # read and save to settings.cfg
    @import_setting.setter
    def set_settings(self, path_settings):
        # def import_setting(self, path=os.path.dirname(sys.argv[0]), file="program/setting.cfg"):
        # read settings form setting.cfg file and set it ot ROM
        # path_settings = path+"/"+file
        logger_win_variables.debug(
            "logging from variable.py set settings start up")
        print("@property import_settings")
        print("setting file: ", path_settings)
        if not os.path.exists(path_settings):
            print("file Setting not found")
            logger_function.warning(
                "function.py, def load_setting, path_settings not found")
            # raise TypeError ("file dose not exist \n"+path_settings)

            # look fore settings.cfg
            path_settings = filedialog.askopenfilename(
                initialdir='/home/', title='select settings.cfg path')
            print("setting file: ", path_settings)

        self.path_settings = path_settings
        configParser = configparser.ConfigParser()
        configParser.read(path_settings)
        setting_dict = {section: dict(configParser.items(section))
                        for section in configParser.sections()}

        print((setting_dict.keys()))
        print((setting_dict["storage_defalt"]))

        self._freq_start = setting_dict["setting"]["freq_start"]
        self._freq_end = setting_dict["setting"]["freq_end"]
        self._freq_step = setting_dict["setting"]["freq_step"]
        self._freq_repetitions = setting_dict["setting"]["freq_repetitions"]

        self._tunematch_tune = setting_dict["TandM_settings"]["tune_value"]
        self._tunematch_match = setting_dict["TandM_settings"]["match_value"]
        self._tunematch_freq = setting_dict["TandM_settings"]["tm_step_value"]
        self._tunematch_lut = setting_dict["TandM_settings"]["tm_lut_value"]

        self._load_sample = setting_dict["storage_defalt"]["seq_data"]
        self._load_experiment = setting_dict["storage_defalt"]["seq_experiment"]
        self._load_data = setting_dict["storage_defalt"]["seq_cycle"]

        # logging.info("Values loaded from load_setting")
        self.import_values = {}
        self.import_values["freq"] = {"freq_start": self._freq_start, "freq_end": self._freq_end,
                                      "freq_step": self._freq_step, "freq_repetitions": self._freq_repetitions}
        self.import_values["tunematch"] = {}
        self.import_values["load"] = {}

        print("import_values", self.import_values)
        logger_win_variables.info("logging from win_variables start up")

        return self.import_values

    @import_setting.setter
    def save_settings(self, value):
        # save settings form ROM and save it to setting.cfg file
        print("save_settings variables.py\n\n", type(value), value)

        logger_win_variables.debug(
            "logging from variable.py save ro settings.cfg")
        print("@property import_settings")
        print("setting file: ", self.path_settings)

        path_settings = self.path_settings

        if not os.path.exists(path_settings):
            print("file Setting not found")
            logger_function.warning(
                "function.py, def load_setting, path_settings not found")
            # raise TypeError ("file dose not exist \n"+path_settings)

            # look fore settings.cfg
            path_settings = filedialog.askopenfilename(
                initialdir='/home/', title='select settings.cfg path')
            print("setting file: ", path_settings)

        configParser = configparser.ConfigParser()
        configParser.read(path_settings)

        config_section = configParser.sections()

        configParser["setting"]["freq_start"] = value["freq"]["freq_start"]
        configParser["setting"]["freq_end"] = value["freq"]["freq_end"]
        configParser["setting"]["freq_step"] = value["freq"]["freq_step"]
        configParser["setting"]["freq_repetitions"] = value["freq"]["freq_repetitions"]

        configParser["TandM_settings"]["tune_value"] = value["tunematch"]["tune"]
        configParser["TandM_settings"]["match_value"] = value["tunematch"]["match"]
        configParser["TandM_settings"]["tm_step_value"] = value["tunematch"]["step"]
        configParser["TandM_settings"]["tm_lut_value"] = value["tunematch"]["lut"]

        configParser["storage_defalt"]["seq_data"] = value["load"]["sample"]
        configParser["storage_defalt"]["seq_experiment"] = value["load"]["experiment"]
        configParser["storage_defalt"]["seq_cycle"] = value["load"]["data"]

        # setting_dict = {section: dict(configParser.items(section))
        #                for section in configParser.sections()}

        #import_values = {}
        # import_values["freq"] = {"freq_start": self._freq_start, "freq_end": self._freq_end,
        #                         "freq_step": self._freq_step, "freq_repetitions": self._freq_repetitions}
        #import_values["tunematch"] = {}
        #import_values["load"] = {}
        #
        #print("import_values", import_values)
        #logger_win_variables.info("logging from win_variables start up")

        # write to config.cfg
        # try:
        #    with open("config.cfg", "r") as configfile:
        #
        #    print("_____________________ TEST pre ______________________")
        #    print("types of sections avalibel ____ \n", config.sections())
        #    print("types of options avalibel of option ___ ",
        #          config.has_option(cfg_section, "file_path"))
        #    print("_____________________ TEST after ______________________")
        #
        #    # config.has_option(section, option)
        #    if configParser.has_section(cfg_section):
        #        print(".cfg section exist")
        #        configParser[cfg_section] = input_values
        #        #logging.info('Values were saved and overwritten')
        #    else:
        #        configParser.add_section(cfg_section)
        #        configParser[cfg_section] = input_values
        #        #logging.info('Values were saved and new written')
        # except IOError:
        #    print("generated new .cfg file")
        #    configParser[cfg_section] = input_values
        #    #logging.info('Values were saved and written to a new file')

        with open(path_settings, "w") as configfile:
            configParser.write(configfile)
        #logging.info('save_values end ')

        return value


class Pulse_Settings:

    def __init__(self):
        print("Pulse_Settings")
        self._puls_start = 00
        self._puls_length = 00
        self._puls_hight = 00

        self.signal_shape = ["squaer", "pulse", "triang", "trapets"]

    @staticmethod
    def parameter2Vektor(start, stop, shape="squaer", number=100):
        t = np.linspcae(start, stop, number)
        if shape == "squaer":
            signale = scipy.signal.square(t, duty=1)

        elif shape == "pulse":
            signalse = scipy.signal.square(t, duty=1)

        elif shape == "triang":
            signalse = scipy.signal.square(t, duty=1)

        elif shape == "trapets":
            signalse = scipy.signal.square(t, duty=1)

        else:
            print("shape not implemented")
            signalse = np.linspcae(start, stop, number)

        print(shape, " signale \n", signale)
        return[t, signale]


class File_Settings:

    def __init__(self):
        print("File_Settings")
        self._absolute_path = os.path.dirname(sys.argv[0])
        self._path = "Test_Sample"
        self._experiment = "Test_experiment"
        self._data = "Sorage_vault"

    @staticmethod
    def generate_folder(self, sample="pre_Sample", experiment="pre_Experiment", data="pre_Data"):
        """ test """

        # create file struckter if not exist as given
        absolute = os.path.dirname(__file__)

        # main folder for all Data
        file_doc = os.path.join(absolute, '..', self._data)
        if not os.path.exists(file_doc):
            os.makedirs(file_doc)

        # folder for samples
        file_doc = os.path.join(file_doc, sample)
        if not os.path.exists(file_doc):
            os.makedirs(file_doc)

        # folder for experiment
        file_doc = os.path.join(file_doc, experiment)
        if not os.path.exists(file_doc):
            os.makedirs(file_doc)

        # folder for data
        file_doc = os.path.join(file_doc, data)
        if not os.path.exists(file_doc):
            os.makedirs(file_doc)

        print("storage path: ", file_doc)
        logger_win_variables.info("storage path: " + file_doc)

        return file_doc

    @staticmethod
    def load_folder(self):
        file_doc = os.path.join(os.path.dirname(__file__), '..', self._data)

        file = filedialog.askopenfilename(
            title='select settings.cfg file from Experimnet', initialdir=file_doc)

        print(file)

    @property
    def save_experiment(self, path="pre_Sample", experiment="pre_Experiment", data="pre_Data"):
        print("save_experiment from variables.py")
        print("path: "+str(path)+"\nexperiment: " +
              str(experiment) + "\nData: " + str(data))

        # ----- Setup of gui ------######l
        window_experiment = tk.Tk()
        window_experiment.title("Experiment Filehandler")
        # window_experiment.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
        # window_experiment.wm_iconbitmap(bitmap=logo_path)
        # Fensterbreite,hoehe, on secreen offset x, on screen offset y
        window_experiment.geometry("800x750")
        window_experiment.option_add(
            "Helvetica", '10')  # Frischart und groesse
        window_experiment.resizable(
            width=False, height=False)  # False = no resize
        text_input_height = 30

        def save_experiment():
            print("save all parameters to .cfg file")
            status_lable = tk.Label(
                window_experiment, text="updated sequenz !!")
            status_lable.place(x=10, y=250, width=500,
                               height=text_input_height)
            return

            # global experiment = {}

            experiment_dict["data"] = data.get()
            experiment_dict["experiment"] = experiment.get()
            experiment_dict["cycle"] = cycle.get()

            print(experiment_dict)

            path_lable.config(text="Seq. for data: "+experiment_dict["data"])
            experiment_lable.config(
                text="Seq. for experiment: "+experiment_dict["experiment"])
            cycle_lable.config(text="Seq. for cycle: " +
                               experiment_dict["cycle"])

            save_values(
                experiment_dict["data"], experiment_dict["experiment"], experiment_dict["cycle"])
            print("end of save_experiment")

        # Title
        lable_text = tk.Label(window_experiment, text="Set Experiment strukture ",
                              foreground="green", background="OliveDrab4", font=("Helvetica", 30))
        lable_text.place(x=50, y=10, width=500, height=50)

        # Set parameters
        text_input_height = 40
        path_text = "Seq. for data: "+str(path)
        path_lable = tk.Label(
            window_experiment, text=path_text, background="gray50")
        path_lable.place(x=50, y=100, width=500, height=text_input_height)

        experiment_text = "Seq. for experiment: "+experiment
        experiment_lable = tk.Label(
            window_experiment, text=experiment_text, background="gray50")
        experiment_lable.place(x=50, y=150, width=500,
                               height=text_input_height)

        cycle_text = "Seq. for data: "+data
        cycle_lable = tk.Label(
            window_experiment, text=cycle_text, background="gray50")
        cycle_lable.place(x=50, y=200, width=500, height=text_input_height)

        # Experiment
        gray_light = "gray70"
        path_lable_input = tk.Label(
            window_experiment, text="Set Sample: \n Ex: TuGraz", background=gray_light)
        path_lable_input.place(x=50, y=300, width=300, height=40)
        self.sample = tk.Entry(window_experiment, fg="black",
                               bg="white", width=40)
        self.sample.place(x=350, y=300, width=200, height=40)

        experiment_lable_input = tk.Label(
            window_experiment, text="Set Seq. experiment: \n Ex: Bismut", background=gray_light)
        experiment_lable_input.place(x=50, y=350, width=300, height=40)
        self.experiment = tk.Entry(
            window_experiment, fg="black", bg="white", width=40)
        self.experiment.place(x=350, y=350, width=200, height=40)

        cycle_lable_input = tk.Label(
            window_experiment, text="Set Seq. cycle: \n Ex: FID, Spin-Echo,", background=gray_light)
        cycle_lable_input.place(x=50, y=400, width=300, height=40)
        self.data = tk.Entry(
            window_experiment, fg="black", bg="white", width=40)
        self.data.place(x=350, y=400, width=200, height=40)

        # Buttons
        save_button = tk.Button(window_experiment, text="Save",
                                background="SkyBlue4", command=lambda: File_Settings.generate_folder(self, sample=self.sample.get(), experiment=self.experiment.get(), data=self.data.get()))
        save_button.place(x=50, y=450, width=140, height=50)

        save_button = tk.Button(window_experiment, text="load",
                                command=lambda:  File_Settings.load_folder(self))
        save_button.place(x=230, y=450, width=140, height=50)

        close_button = tk.Button(window_experiment, text="Close",
                                 background="tomato4", command=window_experiment.destroy)
        close_button.place(x=410, y=450, width=140, height=50)

        # kommentare
        kommentar = tk.Label(
            window_experiment, text="kommentar ", background=gray_light)
        kommentar.place(x=550, y=50, width=300, height=40)

        txt_experiment = tk.Entry(
            window_experiment, fg="black", bg="white", width=40)
        txt_experiment.place(x=550, y=150, width=200, height=40)

        txt_cycle = tk.Entry(window_experiment, fg="black",
                             bg="white", width=40)
        txt_cycle.place(x=550, y=200, width=200, height=40)

        return print("closing load file")
