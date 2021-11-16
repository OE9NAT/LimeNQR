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
