import tkinter as tk
import os
import sys
import configparser


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
        print("hallo")

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

        self._freq_start = 11
        self._freq_end = 11
        self._freq_step = 11
        self._freq_repetitions = 11

        self._tunematch_tune = 11
        self._tunematch_match = 11
        self._tunematch_freq = 11
        self._tunematch_lut = 11

        self._load_sample = "sam"
        self._load_experiment = "exp"
        self._load_data = "Ech"

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

    @import_setting.getter
    def logo_path(self):
        print(self._log_path, "\n")
        return self._log_path

    @import_setting.setter
    def set_settins(self, path_settings):
        # def import_setting(self, path=os.path.dirname(sys.argv[0]), file="program/setting.cfg"):
        # read settings form setting.cfg file and set it ot ROM
        # path_settings = path+"/"+file
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

        configParser = configparser.ConfigParser()
        configParser.read(path_settings)
        setting_dict = {section: dict(configParser.items(section))
                        for section in configParser.sections()}

        print((setting_dict.keys()))
        print((setting_dict["setting"]))

        self._freq_start = setting_dict[0]  # ["settings"]["freq_start"]
        self._freq_end = setting_dict["setting"]["freq_end"]
        self._freq_step = setting_dict["setting"]["freq_step"]
        self._freq_repetitions = setting_dict["setting"]["freq_repetitions"]

        self._tunematch_tune = setting_dict["TandM_settings"]["tune_value"]
        self._tunematch_match = setting_dict["TandM_settings"]["match_value"]
        self._tunematch_freq = setting_dict["TandM_settings"]["tm_step_value"]
        self._tunematch_lut = setting_dict["TandM_settings"]["tm_lut_value"]

        self._load_sample = "1sam"
        self._load_experiment = "1exp"
        self._load_data = "1Ech"

        # logging.info("Values loaded from load_setting")
        self.import_values = {}
        self.import_values["freq"] = {"freq_start": self._freq_start, "freq_end": self._freq_end,
                                      "freq_step": self._freq_step, "freq_repetitions": self._freq_repetitions}
        self.import_values["tunematch"] = {}
        self.import_values["load"] = {}

        print("import_values", type(self.import_values))

        return self.import_values

    # ## @property
    # #def freq(self):
    # #    # implement to read from settings.cfg
    # #    self._freq_start = 10000
    # #    self._freq_end = 20000
    # #    self._freq_step = 1000
    # #    self._freq_repetitions = 100
    # #    freq = []
    # #    freq.append(self._freq_start)
    # #    freq.append(self._freq_end)
    # #    freq.append(self._freq_step)
    # #    freq.append(self._freq_repetitions)
    # #    return freq

    # @import_setting.setter
    # def define_frequency(self, start, stop, step, reps):
    #     print("setter value define_frequency", start)
    #     self._freq_start = start
    #     self._freq_end = stop
    #     self._freq_step = step
    #     self._freq_repetitions = reps
