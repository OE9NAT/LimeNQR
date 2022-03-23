try:
    import os
    import pip
    import sys
    import threading
except ImportError:
    print(" import error in start.py")

import logging  # DEBUG INFO WARNING ERROR
from logging.handlers import QueueHandler


# handler = logging.FileHandler("log/Value_log.log")
# handler = logging.handlers.RotatingFileHandler("log/Value_log.log")
# formatter = logging.Formatter("____ %(name)s ____  %(asctime)s : %(levelname)s : \n %(message)s")
# handler.setFormatter(formatter)

# Check if log file exist
if not os.path.exists("log"):
    os.makedirs("log")

# Check if dh5_file file exist for saving all measured files
if not os.path.exists("log/dh5_file"):
    os.makedirs("log/dh5_file")


logging.basicConfig(filename="log/DEFAULT_log.log",
                    level=logging.DEBUG,  # <- set logging level
                    format="______ %(name)s ______  %(asctime)s : %(levelname)s : \n %(message)s")  # set level


logger_start = logging.getLogger('start')
logger_start.addHandler(logging.StreamHandler())
logger_start.info("logging from start up")


def test_version():
    """
    # Description:

    Verification of the installed and use Python syste version

    # Args:

    NONE

    # Returns:

    True = if tested verifications passes
    False = if tested verification fails

    """

    # python system  check
    # print(sys.version)
    version = sys.version_info[0:2]

    print("Python version ", sys.version[0:40])

    if not sys.version_info[:2][0] > 2:
        print("\n Error \n installed python: ", "version ",
              version[0], ".", version[1], sep="")
        # print("version available ",sys.version_info)
        print("\n minimum requirements is python 3.7 \n ERROR end")
        return False

    logger_start.warning("start test python version "+sys.version)
    return True


def test_import():
    """
    # Description:

    Verification of all used modues what are used in the Projekt.
    If the module is able to be imported.

    # Args:

    NONE

    # Returns:

    True = if tested verifications passes
    False = if tested verification fails

    """
    # print("\n python modulse avalibel: ")
    # os.system('pip list')
    # print("\n end python modulse")

    # print("eggs geladen: ",'eggs' in sys.modules)
    # print("numpy geladen: ",'numpy' in sys.modules)

    # print("INFO imported \n")
    # print(*sys.modules.keys(),sep="\n")

    # list of all necessery imports
    try:
        import numpy
        import matplotlib
        import tkinter
        import tkinter.ttk
        # from tkinter import scrolledtext

        import matplotlib.pyplot
        # from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
        import configparser
        import queue
        import PIL
        import logging
        import h5py

        import os
        import sys
        import scipy
        import csv
        import serial
        import time

        # import RPi

    except ModuleNotFoundError as err:
        # Error handling
        print("\n #### ERROR loading import ####\n")
        print(err)
        print("\n#### ERROR loading import #### \n")
        # os.system('python -m pip install '+str(err))

        return False
    else:
        return True


def test_settings():
    """
    # Description:

    Space holder for additional requirement verification that want
    to be thestet at startup

    # Args:

    NONE

    # Returns:

    True = if tested verifications passes
    False = if tested verification fails

    """

    return True


def info_dialog():
    """
    # Description:

    Info text for presenting on startup

    # Args:

    NONE

    # Returns:

    message box of all of its information

    """

    text = """************************************************  \n
    Autor: Philipp MALIN
    Date: 01.07.2021
    Version: 1.0
    Description: Grapical user interface to control SDR
                 for Nuclear Quadrupole Resonance spectroscopy.
    \n************************************************  """
    return text


# start main programm
if __name__ == "__main__":
    print("start GUI")
    # thread count form the system
    print("number of treads running: ", threading.active_count())
    print("current treads: ", threading.current_thread())
    print("list of all treads: ", threading.enumerate())

    print(info_dialog())

    # do all checks
    test_dict = {}
    test_dict["test_version"] = test_version()
    test_dict["test_import"] = test_import()
    test_dict["test_settings"] = test_settings()

    print("Check list:", *test_dict.items(), sep="\n")

    if False in test_dict.values():
        test_import()
        # print("ERROR \n problem with imports \n")

        raise ImportError("imports are not satisfied")

    else:
        print("\n\nimports alles ok\n\n")

    # start Progra
    sys.path.append("program")

    import GUI  # start GUI
    GUI.GUI_start()

    print("-_____END check start of GUI ____-")
