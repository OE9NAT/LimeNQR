import tkinter as tk
import os
import sys


class Value_Settings:

    def __init__(self):
        print("Value_Settings")

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
                sys.argv[0])) + "/program/icon_logo.xbm"
            window.wm_iconbitmap(bitmap=self._log_path)
        window.destroy()
        print("path of logo: ", self._log_path)

    @staticmethod
    def hallo_word():
        print("hallo")

    @staticmethod
    def import_setting(path=os.path.dirname(
            sys.argv[0]), file="program/setting.cfg"):
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

        self._freq_start = 11
        self._freq_end = 11
        self._freq_step = 11
        self._freq_repetitions = 11

        self._tm_tune = 11
        self.tm_match = 11
        self.tm_freq = 11
        self._tm_lut = 11

        logging.info("Values loaded from load_setting")
        return setting_dict

    @property  # getter for path of logo for window
    def logo_path(self):
        print(self._log_path, "\n")
        return self._log_path

    @property
    def freq(self):
        # implement to read from settings.cfg
        self._freq_start = 10000
        self._freq_end = 20000
        self._freq_step = 1000
        self._freq_repetitions = 100
        freq = []
        freq.append(self._freq_start)
        freq.append(self._freq_end)
        freq.append(self._freq_step)
        freq.append(self._freq_repetitions)
        return freq

    @freq.setter
    def define_frequency(self, start, stop, step, reps):
        self._freq_start = start
        self._freq_end = stop
        self._freq_step = step
        self._freq_repetitions = reps


class global_variables():

    def __init__(self):
        get
        set
