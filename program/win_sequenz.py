
import variables
import os
import sys
import configparser
import PIL.Image as image
from datetime import datetime
import numpy as np

import tkinter as tk
import tkinter.ttk as TTK  # use for Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter import scrolledtext   # use for logger
from PIL import ImageTk, Image  # .jpg

import logging  # DEBUG INFO WARNING ERROR
from logging.handlers import QueueHandler

import function as helper

logger_seq = logging.getLogger('win_sequenz')
logger_seq.addHandler(logging.StreamHandler())
logger_seq.info("logging from winsow sequenz at start up")

value_set = variables.Value_Settings()
logo_path = value_set.logo_path


# class Seq_values:
#    print("class Sequenz values setup")


class Window_seq:
    print("class Sequenz Window setup")
    frame_boarder = 4
    max_number_puls = 10

    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)

        # Sequenz
        self.sequenz_type = "fid"

        self.target_freq = 83.62  # target frequency of the experiment in MHz
        self.band_freq = 1.2    # IF or base band frequency in MHz
        self.blank_time = 10    # duration after puls, before window
        self.window_time = 10  # time to read the signal

        self.samplerate = 30.72      # Sampling Rate in M sap per sec
        self.averaging = 1000        # number of averages
        self.repetition_num = 1         # number of repetitions

        self.correction_tx_i_dc = -45  # TX I DC correction
        self.correction_tx_q_dc = 0  # TX Q DC correction
        self.correction_tx_i_gain = 2047   # TX I Gain correction
        self.correction_tx_q_gain = 2039  # TX Q Gain correction
        self.correction_tx_pahse = 3  # TX phase adjustment

        self.correction_rx_i_dc = 0     # RX I DC correction
        self.correction_rx_q_dc = 0     # RX Q DC correction
        self.correction_rx_i_gain = 2047  # RX I Gain correction
        self.correction_rx_q_gain = 2047  # RX Q Gain correction
        self.correction_rx_phase = 0     # RX phase adjustment

        # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
        # be adjusted in the ways that it fits to an integer multiply of the buffer size
        self.repetition_time = 5  # repetition time in mseconds
        self.acquisition_time = 82  # acquisition time microseconds e-6
        # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
        self.gate_signal = [1, 0, 50, 10]

        self.phase_number = [4, 1]  # number of phases
        # pcyc level (only needed if more then 1 pulse is used (and a relative / different phase is necessary))
        self.phase_level = [0, 1]
        # pulse phase (added to phase shift due to pcn)
        self.phase_puls = [0, np.pi/4]
        self.number_phase_level = 1

        # pulse durations
        self.puls_freq = [self.band_freq]       # pulse frequency
        self.puls_duration = [3e-6]  # diy  pulse  duration
        # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
        self.puls_amplitude = [1]
        # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)
        self.puls_arangement = [300]

        # base band low pass filter)
        self.low_pass_rx = 3.0e6  # RX BW
        self.low_pass_tx = 130.0e6       # RX BW

        self.gain_rx = 55.0       # RX gain
        self.gain_tx = 40.0       # TX gain

        puls_count = len(self.puls_freq)     # number of pulses
        lo_freq = self.target_freq * 1000000 - self.band_freq * 1000000
        rx_gain_factor = 10**((self.puls_freq[0]-40)/20)

        self.storage = ["Experiment initialise"]

        # call Window
        # Window_seq.window_sequenz(self, seq_type)

    # @staticmethod  # property
    def window_sequenz(self, seq_type="0", value_settings="1", puls_cylce="1"):
        print("type of sequenz: ", seq_type)
        print("settings variables: \n \n", value_settings)
        # settings variables:  {'freq': {'freq_start': '1000', 'freq_end': '2000', 'freq_step': '100', 'freq_repetitions': '10'}, 'tunematch': {'tune': '3.3', 'match': '5', 'step': '10', 'lut': '10'}, 'load': {'sample': '_test_Sample', 'experiment': '_test_Experiment', 'data': '_test_Data'}, 'sequenz': {'sequenz': 'fid'}}
        print("settings variables: \n \n", value_settings["freq"])
        self.puls_freq = value_settings["freq"]
        self.storage = value_settings["load"]
        self.sequenz_type = seq_type

        print("number of puls_cylce of sequenz: ", puls_cylce)
        puls_cylce = int(puls_cylce)

        if puls_cylce > Window_seq.max_number_puls:
            puls_cylce = Window_seq.max_number_puls

            print("max puls_cylce reached")

        # open GUI window and Present settings
        # sequenz window
        logger_seq.info("start win_sequenz.py start class logger_seq init")
        self.win_seq = tk.Tk()
        self.win_seq.title("Magnetic Resonance Imaging - Sequenz Manager")
        # self.win_seq.wm_iconbitmap(bitmap=logo_path)
        self.win_seq.wm_iconbitmap(
            bitmap="C:/Users/MALIN Philipp/git/bacharbeit/program/icon_logo.ico")

        self.win_seq.geometry("1200x1000")  # "1000x750+400+100"
        # (width_minsize=1200, height_minsize=800)
        self.win_seq.minsize(380, 400)
        # self.win_seq.maxsize(1200, 850)

        # zeilen hoehe
        self.win_seq.grid_rowconfigure(0, weight=1, minsize=60)  # zeilen hoehe
        self.win_seq.grid_rowconfigure(
            1, weight=4, minsize=100)  # zeilen hoehe
        self.win_seq.grid_rowconfigure(
            2, weight=8, minsize=100)  # zeilen hoehe
        self.win_seq.grid_rowconfigure(3, weight=4, minsize=50)  # zeilen hoehe
        # self.win_seq.grid_rowconfigure(4, weight=4, minsize=50)  # zeilen hoehe

        # spalten breite
        self.win_seq.grid_columnconfigure(0, weight=1, minsize=280)
        self.win_seq.grid_columnconfigure(1, weight=4, minsize=300)
        self.win_seq.grid_columnconfigure(2, weight=4, minsize=280)

        # Titile
        frame_title = tk.Frame(self.win_seq, bg="grey")
        frame_title.grid(columnspan=3, row=0, column=0, padx=Window_seq.frame_boarder,
                         pady=Window_seq.frame_boarder, sticky="nsew")
        lable_text = tk.Label(frame_title, text="Set Sequenz ",
                              foreground="green", background="OliveDrab4", font=("Helvetica", 30))
        lable_text.pack(fill="x")

        # Info box experiment strukture
        self.info_box = tk.LabelFrame(self.win_seq, text="info box", bg='grey')
        self.info_box.grid(row=1, column=0, padx=Window_seq.frame_boarder,
                           pady=Window_seq.frame_boarder, sticky="nsew")

        self.input_info_sequenz = tk.Label(
            self.info_box, text="Sequenz selected:", bg='grey')
        self.input_info_sequenz.pack()

        self.sequenz_type_input = tk.Entry(
            self.info_box, fg="black", bg="white")
        self.sequenz_type_input.pack()
        self.sequenz_type_input.insert(0, self.sequenz_type)

        info_text = "Measurment Settings\n"
        info_text += "START frequency: " + \
            str(value_settings["freq"]["freq_start"])+"\n"
        info_text += "END frequency: " + \
            str(value_settings["freq"]["freq_end"])+"\n"
        info_text += "frequency steps: " + \
            str(value_settings["freq"]["freq_step"])+"\n"
        info_text += "average: " + \
            str(value_settings["freq"]["freq_repetitions"])+"\n"
        self.lable_info_experiment = tk.Label(
            self.info_box, text=info_text, bg='grey')
        self.lable_info_experiment.pack()

        info_text = "\n Experiment strukture:"+"\n"
        info_text += "Sample: " + value_settings["load"]["sample"] + "\n"
        info_text += "Experiment: " + value_settings["load"]["experiment"]+"\n"
        info_text += "Data: " + value_settings["load"]["data"]+"\n"
        self.lable_info_experiment = tk.Label(
            self.info_box, text=info_text, bg='grey')
        self.lable_info_experiment.pack()

        # plot sequenz
        frame_plot = tk.Frame(self.win_seq, bg="grey")
        frame_plot.grid(columnspan=2, row=1, column=1, padx=Window_seq.frame_boarder,
                        pady=Window_seq.frame_boarder, sticky="nsew")

        def plot_sequenz(offset, puls, delay=20, window=40, frequency=100, amplitude=1):
            rest = 10  # end of puls

            duration = []
            duration_list = []

            for count, value in enumerate(puls):
                duration.extend([0 for i in range(0, offset[count])])
                duration.extend([1 for i in range(0, puls[count])])
                duration_list.append(offset[count])
                duration_list.append(puls[count])

            delay_start = len(duration)
            duration.extend([0 for i in range(0, delay)])

            window_start = len(duration)
            duration.extend([1 for i in range(0, window)])
            duration.extend([0 for i in range(0, rest)])

            start_time = 0
            end_time = len(duration)
            sample_rate = 1000

            time = np.arange(start_time, end_time, 1/sample_rate)

            start_time = time[0]
            end_time = time[-1]
            time = np.arange(start_time, end_time, 1/sample_rate)
            print(start_time, "end_time", end_time)

            sinus = amplitude * np.sin(2 * np.pi * frequency * time)
            sinus = amplitude * np.sin(2 * np.pi * time)
            # sinus = sinus * np.repeat(duration, sample_rate)

            x_puls = np.repeat(range(len(duration)), sample_rate)
            y_puls = np.repeat(duration, sample_rate)
            x_puls = x_puls[1:]
            y_puls = y_puls[:-1]
            x_puls = np.append(x_puls, x_puls[-1] + 1)
            y_puls = np.append(y_puls, y_puls[-1])

            time = np.append(time, time[-1]).tolist()
            sinus = np.append(sinus, sinus[-1]).tolist()

            sinus_puls = [sinus[count] if value ==
                          1 else 0 for count, value in enumerate(y_puls)]

            # with dampend responce
            print("window_start,", window_start*sample_rate)
            window_start_upsample = window_start*sample_rate

            sinus_puls = [sinus_puls[count] * (np.exp(-(count-window_start_upsample-200)*0.0001)) if count >
                          window_start_upsample else sinus_puls[count] for count, value in enumerate(sinus_puls)]

            print(len(x_puls), "x_puls", x_puls[0: 15])
            print(len(y_puls), "y_puls", y_puls[0: 15])
            print(len(sinus_puls), "sinus_puls \n", sinus_puls[0: 5])
            print(len(time), "time \n", time[0: 5])

            figure = Figure(figsize=(5, 5), dpi=100)
            fig_plot = figure.add_subplot()

            # plt.plot(sinus, 'ro')
            fig_plot.plot(time, sinus_puls)
            fig_plot.plot(x_puls, y_puls)
            fig_plot.legend(['Puls frequenzy', 'Enwrap of Puls'])

            off_bool = True
            point_summ = 0
            for count, point in enumerate(duration_list):
                if off_bool:
                    fig_plot.annotate('Offset '+str(int(count/2+1)), (point_summ, 1),
                                      textcoords="offset points", xytext=(10, -20), ha='left')
                    off_bool = False
                else:
                    fig_plot.annotate('Puls '+str(int((count+1)/2)), (point_summ, 1),
                                      textcoords="offset points", xytext=(10, 10), ha='left')
                    off_bool = True
                point_summ += point

            fig_plot.annotate('Delay', (point_summ, 1),
                              textcoords="offset points", xytext=(10, -20), ha='left')
            fig_plot.annotate('Window', (window_start, 1),
                              textcoords="offset points", xytext=(10, 10), ha='left')

            if amplitude < 1.5:
                fig_plot.set_ylim(-1.2, 1.7)
            fig_plot.set_title("Sequenz of Pulssequenz")
            fig_plot.set_xlabel("Time in ms")
            fig_plot.set_ylabel("Amplitude")

            #fig_plot.savefig('plot.jpg', dpi=300)
            # fig_plot.show()

            return figure

        # fix
        if seq_type == "fid":

            puls = [100]  # in ms
            offset = [50]
            delay = 30
            window = 70
            freq_plot = int(value_settings["freq"]["freq_start"])

            plot_fig = plot_sequenz(
                offset, puls, frequency=freq_plot, amplitude=1)

            # specify the window as master
            canvas = FigureCanvasTkAgg(plot_fig, master=frame_plot)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

        elif seq_type == "spin":
            puls = [5, 2, 10, 8]
            offset = [20, 10, 5, 8]
            delay = 11
            window = 20

            plot_fig = plot_sequenz(offset, puls, delay, window)

            # specify the window as master
            canvas = FigureCanvasTkAgg(plot_fig, master=frame_plot)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

        elif seq_type == "comp":
            puls = [5, 2, 10, 8]
            offset = [20, 10, 5, 8]
            delay = 11
            window = 20

            plot_fig = plot_sequenz(offset, puls, delay, window)

            # specify the window as master
            canvas = FigureCanvasTkAgg(plot_fig, master=frame_plot)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()

        elif seq_type == "spin_phase":
            puls = [5, 2, 10, 8]
            offset = [20, 10, 5, 8]
            delay = 11
            window = 20

            plot_fig = plot_sequenz(offset, puls, delay, window)

            # specify the window as master
            canvas = FigureCanvasTkAgg(plot_fig, master=frame_plot)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            # own sequenz
            img_path = "/program/sequenz/own_seq.JPG"
            image_path = os.path.abspath(os.path.dirname(
                sys.argv[0])) + img_path
            image = Image.open(image_path)
            image_puls = image.resize((750, 300))
            image_puls = ImageTk.PhotoImage(image_puls, master=self.win_seq)
            pic_label = tk.Label(frame_plot, image=image_puls)
            pic_label.pack(fill="both", expand="yes")
            pic_label.image = image_puls
            image.close()

        # inputbox
        # SDR settings
        self.frame_sdr = tk.LabelFrame(
            self.win_seq, text="SDR Settings", bg='grey')
        self.frame_sdr.grid(row=2, column=0, padx=Window_seq.frame_boarder,
                            pady=Window_seq.frame_boarder, sticky="nsew", rowspan=2)
        self.frame_sdr.grid_columnconfigure(0, weight=1)
        self.frame_sdr.grid_columnconfigure(1, weight=1)

        lable_info_rx_gain = tk.Label(self.frame_sdr, text="RX gain", padx=Window_seq.frame_boarder,
                                      pady=Window_seq.frame_boarder, bg='grey')
        lable_info_rx_gain.grid(row=2, column=0)
        self.gain_rx_input = tk.Entry(self.frame_sdr, fg="black", bg="white")
        self.gain_rx_input.grid(row=2, column=1, sticky="ew")

        lable_info_tx_gain = tk.Label(self.frame_sdr, text="TX gain", padx=Window_seq.frame_boarder,
                                      pady=Window_seq.frame_boarder, bg='grey')
        lable_info_tx_gain.grid(row=3, column=0)
        self.gain_tx_input = tk.Entry(self.frame_sdr, fg="black", bg="white")
        self.gain_tx_input.grid(row=3, column=1, sticky="ew")

        lable_info_rx_pass = tk.Label(self.frame_sdr, text="RX low-pass", padx=Window_seq.frame_boarder,
                                      pady=Window_seq.frame_boarder, bg='grey')
        lable_info_rx_pass.grid(row=4, column=0)
        self.low_pass_rx_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.low_pass_rx_input.grid(row=4, column=1, sticky="ew")

        lable_info_tx_pass = tk.Label(self.frame_sdr, text="TX low-pass", padx=Window_seq.frame_boarder,
                                      pady=Window_seq.frame_boarder, bg='grey')
        lable_info_tx_pass.grid(row=5, column=0)
        self.low_pass_tx_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.low_pass_tx_input.grid(row=5, column=1, sticky="ew")

        lable_correction_tx_i_dc = tk.Label(self.frame_sdr, text="correction_tx_i_dc", padx=Window_seq.frame_boarder,
                                            pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_tx_i_dc.grid(row=6, column=0)
        self.correction_tx_i_dc_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_tx_i_dc_input.grid(row=6, column=1, sticky="ew")

        lable_correction_tx_q_dc = tk.Label(self.frame_sdr, text="correction_tx_q_dc", padx=Window_seq.frame_boarder,
                                            pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_tx_q_dc.grid(row=7, column=0)
        self.correction_tx_q_dc_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_tx_q_dc_input.grid(row=7, column=1, sticky="ew")

        lable_correction_tx_i_gain = tk.Label(self.frame_sdr, text="correction_tx_i_gain", padx=Window_seq.frame_boarder,
                                              pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_tx_i_gain.grid(row=8, column=0)
        self.correction_tx_i_gain_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_tx_i_gain_input.grid(row=8, column=1, sticky="ew")

        lable_correction_tx_q_gain = tk.Label(self.frame_sdr, text="correction_tx_q_gain", padx=Window_seq.frame_boarder,
                                              pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_tx_q_gain.grid(row=9, column=0)
        self.correction_tx_q_gain_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_tx_q_gain_input.grid(row=9, column=1, sticky="ew")

        lable_correction_tx_pahse = tk.Label(self.frame_sdr, text="correction_tx_pahse", padx=Window_seq.frame_boarder,
                                             pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_tx_pahse.grid(row=10, column=0)
        self.correction_tx_pahse_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_tx_pahse_input.grid(row=10, column=1, sticky="ew")

        lable_correction_rx_i_dc = tk.Label(self.frame_sdr, text="correction_rx_i_dc", padx=Window_seq.frame_boarder,
                                            pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_rx_i_dc.grid(row=11, column=0)
        self.correction_rx_i_dc_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_rx_i_dc_input.grid(row=11, column=1, sticky="ew")

        lable_correction_rx_q_dc = tk.Label(self.frame_sdr, text="correction_rx_q_dc", padx=Window_seq.frame_boarder,
                                            pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_rx_q_dc.grid(row=12, column=0)
        self.correction_rx_q_dc_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_rx_q_dc_input.grid(row=12, column=1, sticky="ew")

        lable_correction_rx_i_gain = tk.Label(self.frame_sdr, text="correction_rx_i_gain", padx=Window_seq.frame_boarder,
                                              pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_rx_i_gain.grid(row=13, column=0)
        self.correction_rx_i_gain_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_rx_i_gain_input.grid(row=13, column=1, sticky="ew")

        lable_correction_rx_q_gain = tk.Label(self.frame_sdr, text="correction_rx_q_gain", padx=Window_seq.frame_boarder,
                                              pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_rx_q_gain.grid(row=14, column=0)
        self.correction_rx_q_gain_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_rx_q_gain_input.grid(row=14, column=1, sticky="ew")

        lable_correction_rx_phase = tk.Label(self.frame_sdr, text="correction_rx_phase", padx=Window_seq.frame_boarder,
                                             pady=Window_seq.frame_boarder, bg='grey')
        lable_correction_rx_phase.grid(row=15, column=0)
        self.correction_rx_phase_input = tk.Entry(
            self.frame_sdr, fg="black", bg="white")
        self.correction_rx_phase_input.grid(row=15, column=1, sticky="ew")

        self.gain_rx_input.insert(0, self.gain_rx)
        self.gain_tx_input.insert(0, self.gain_tx)
        self.low_pass_rx_input.insert(0, self.low_pass_rx)
        self.low_pass_tx_input.insert(0, self.low_pass_tx)
        self.correction_tx_i_dc_input.insert(0, self.correction_tx_i_dc)
        self.correction_tx_q_dc_input.insert(0, self.correction_tx_q_dc)
        self.correction_tx_i_gain_input.insert(0, self.correction_tx_i_gain)
        self.correction_tx_q_gain_input.insert(0, self.correction_tx_q_gain)
        self.correction_tx_pahse_input.insert(0, self.correction_tx_pahse)
        self.correction_rx_i_dc_input.insert(0, self.correction_rx_i_dc)
        self.correction_rx_q_dc_input.insert(0, self.correction_rx_q_dc)
        self.correction_rx_i_gain_input.insert(0, self.correction_rx_i_gain)
        self.correction_rx_q_gain_input.insert(0, self.correction_rx_q_gain)
        self.correction_rx_phase_input.insert(0, self.correction_rx_phase)

        # Time of Puls and Delay
        self.frame_puls = tk.LabelFrame(
            self.win_seq, text="Timing of Puls", bg='grey')
        self.frame_puls.grid(row=2, column=1, padx=Window_seq.frame_boarder,
                             pady=Window_seq.frame_boarder, sticky="nsew", rowspan=2)
        self.frame_puls.grid_propagate(False)

        self.frame_puls.grid_columnconfigure(0, weight=1)
        self.frame_puls.grid_columnconfigure(1, weight=1)
        # self.frame_puls.grid_rowconfigure(0, weight=1)
        # self.frame_puls.grid_rowconfigure(1, weight=1)
        # self.frame_puls.grid_rowconfigure(2, weight=1)
        # self.frame_puls.grid_rowconfigure(3, weight=1)

        # ADDING A SCROLLBAR
        myscrollbar = tk.Scrollbar(self.frame_puls, orient="vertical")
        # myscrollbar.pack(side="right",fill="y")
        myscrollbar.grid(row=0, column=2, sticky="nsew", rowspan=10)

        if seq_type == "fid":
            print("FID sequnez", seq_type)
            number_pulses = 1

        elif seq_type == "spin":
            print("spin Echo sequenz =", seq_type)
            number_pulses = 2

        elif seq_type == "comp":
            print("Composite Pulse", seq_type)
            number_pulses = 3

        elif seq_type == "spin_phase":
            print("own", seq_type)
            number_pulses = 4

        elif seq_type == "own":
            print("own", seq_type)
            number_pulses = puls_cylce

        else:
            number_pulses = puls_cylce

        for number in range(number_pulses):
            number_puls = number*2
            number_delay = number*2+1

            lable_delay = tk.Label(
                self.frame_puls, text="Delay "+str(number+1)+" in ms", bg='grey')
            lable_delay.grid(row=number_delay, column=0)
            delay = tk.Entry(self.frame_puls, fg="black", bg="white")
            delay.grid(row=number_delay, column=1, sticky="ew")
            # delay.config(yscrollcommand=myscrollbar.set)

            lable_puls = tk.Label(
                self.frame_puls, text="Puls "+str(number+1)+" in ms", bg='grey')
            lable_puls.grid(row=number_puls, column=0)
            pulse = tk.Entry(self.frame_puls, fg="black", bg="white")
            pulse.grid(row=number_puls, column=1, sticky="ew")
            # pulse.config(yscrollcommand=myscrollbar.set)

        # # time of Readout
        frame_readout = tk.LabelFrame(self.win_seq, text="Readout", bg='grey')
        frame_readout.grid(row=2, column=2, padx=Window_seq.frame_boarder,
                           pady=Window_seq.frame_boarder, sticky="nsew")

        frame_readout.grid_columnconfigure(0, weight=1)
        frame_readout.grid_columnconfigure(1, weight=1)

        # Repetition
        lable_repetition_time = tk.Label(
            frame_readout, text="Repetition time in ms", bg='grey')
        lable_repetition_time.grid(row=1, column=0, sticky="ew")

        self.repetition_time_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.repetition_time_input.grid(row=1, column=1, sticky="ew")
        self.repetition_time_input.insert(0, self.repetition_time)

        # Acquirer
        lable_acquirer = tk.Label(
            frame_readout, text="Acquirer time in ms", bg='grey')
        lable_acquirer.grid(row=2, column=0, sticky="ew")

        self.acquisition_time_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.acquisition_time_input.grid(row=2, column=1, sticky="ew")
        self.acquisition_time_input.insert(0, self.acquisition_time)

        # gate_signal
        lable_gate_signal = tk.Label(
            frame_readout, text="gate_signal array", bg='grey')
        lable_gate_signal.grid(row=3, column=0, sticky="ew")

        self.gate_signal_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.gate_signal_input.grid(row=3, column=1, sticky="ew")
        self.gate_signal_input.insert(0, self.gate_signal)

        # blank_time
        lable_blank_time = tk.Label(
            frame_readout, text="Blanking time in ms", bg='grey')
        lable_blank_time.grid(row=4, column=0, sticky="ew")

        self.blank_time_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.blank_time_input.grid(row=4, column=1, sticky="ew")
        self.blank_time_input.insert(0, self.blank_time)

        # window_time
        lable_window_time = tk.Label(
            frame_readout, text="Window Time in ms", bg='grey')
        lable_window_time.grid(row=5, column=0, sticky="ew")

        self.window_time_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.window_time_input.grid(row=5, column=1, sticky="ew")
        self.window_time_input.insert(0, self.window_time)

        # # Phase
        frame_readout = tk.LabelFrame(
            self.win_seq, text="Phase & Puls-parameter", bg='grey')
        frame_readout.grid(row=3, column=2, padx=Window_seq.frame_boarder,
                           pady=Window_seq.frame_boarder, sticky="nsew")

        frame_readout.grid_columnconfigure(0, weight=1)
        frame_readout.grid_columnconfigure(1, weight=1)

        # phase_number
        lable_phase_number = tk.Label(
            frame_readout, text="phase_number array", bg='grey')
        lable_phase_number.grid(row=1, column=0, sticky="ew")

        self.phase_number_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.phase_number_input.grid(row=1, column=1, sticky="ew")
        self.phase_number_input.insert(0, self.phase_number)

        # phase_level
        lable_phase_level = tk.Label(
            frame_readout, text="phase_number array", bg='grey')
        lable_phase_level.grid(row=2, column=0, sticky="ew")

        self.phase_level_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.phase_level_input.grid(row=2, column=1, sticky="ew")
        self.phase_level_input.insert(0, self.phase_level)

        # phase_puls
        lable_phase_puls = tk.Label(
            frame_readout, text="phase_puls array", bg='grey')
        lable_phase_puls.grid(row=3, column=0, sticky="ew")

        self.phase_puls_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.phase_puls_input.grid(row=3, column=1, sticky="ew")
        self.phase_puls_input.insert(0, self.phase_puls)

        # number_phase_level
        lable_number_phase_level = tk.Label(
            frame_readout, text="number_phase_level array", bg='grey')
        lable_number_phase_level.grid(row=4, column=0, sticky="ew")

        self.number_phase_level_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.number_phase_level_input.grid(row=4, column=1, sticky="ew")
        self.number_phase_level_input.insert(0, self.number_phase_level)

        # puls_amplitude
        lable_puls_amplitude = tk.Label(
            frame_readout, text="puls_amplitude", bg='grey')
        lable_puls_amplitude.grid(row=5, column=0, sticky="ew")

        self.puls_amplitude_input = tk.Entry(
            frame_readout, fg="black", bg="white")
        self.puls_amplitude_input.grid(row=5, column=1, sticky="ew")
        self.puls_amplitude_input.insert(0, self.puls_amplitude)

        #

        # Buttens
        frame_Buttens = tk.Frame(self.win_seq, bg='grey')
        frame_Buttens.grid(row=4, column=1, padx=2, pady=2, sticky="nsew")

        button_run = tk.Button(frame_Buttens, text="load",
                               command=lambda: Window_seq.load_seq(self))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="save",
                               command=lambda: Window_seq.save_seq(self))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="test",
                               command=lambda: print("space for expantion "))  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="left")

        button_run = tk.Button(frame_Buttens, text="close",
                               background="tomato4", command=self.win_seq.destroy)  # load_last_values)
        button_run.pack(fill="x", padx=2, pady=2, side="right")

    @ staticmethod
    def save_seq(self):
        # get input parameter and save to class variables

        self.sequenz_type = self.sequenz_type_input.get()

        # read Timing of Puls
        read_array = []
        for entery in self.frame_puls.winfo_children():
            if entery.winfo_class() == 'Entry':
                entery_value = entery.get()
                print("Puls entery", entery, "value: ", entery_value)
                if len(entery_value) == 0:
                    helper.error_type_window(
                        entery_value, int, "Puls entery", "Fill in all Puls parameter")
                    break
                try:
                    var_input = int(entery_value)
                except ValueError:
                    helper.error_type_window(entery_value, int, "Puls entery")
                read_array.append(var_input)

        delay_array = read_array[::2].copy()
        pulse_array = read_array[1::2].copy()
        print("pulse_array", pulse_array)
        print("delay_array", delay_array)

        #self.puls_freq = [12377777777]
        self.blank_time = self.blank_time_input.get()
        self.window_time = self.window_time_input.get()

        # read Readout
        self.repetition_time = self.repetition_time_input.get()
        self.acquisition_time = self.acquisition_time_input.get()
        self.gate_signal = self.gate_signal_input.get()

        # read SDR Settings
        self.correction_tx_i_dc = self.correction_tx_i_dc_input.get()
        self.correction_tx_q_dc = self.correction_tx_q_dc_input.get()
        self.correction_tx_i_gain = self.correction_tx_i_gain_input.get()
        self.correction_tx_q_gain = self.correction_tx_q_gain_input.get()
        self.correction_tx_pahse = self.correction_tx_pahse_input.get()
        self.correction_rx_i_dc = self.correction_rx_i_dc_input.get()
        self.correction_rx_q_dc = self.correction_rx_q_dc_input.get()
        self.correction_rx_i_gain = self.correction_rx_i_gain_input.get()
        self.correction_rx_q_gain = self.correction_rx_q_gain_input.get()
        self.correction_rx_phase = self.correction_rx_phase_input.get()
        self.low_pass_rx = self.low_pass_rx_input.get()
        self.low_pass_tx = self.low_pass_tx_input.get()
        self.gain_rx = self.gain_rx_input.get()
        self.gain_tx = self.gain_tx_input.get()

        # Phase and puls paramterer
        self.phase_number = self.phase_number_input.get()
        self.phase_level = self.phase_level_input.get()
        self.phase_puls = self.phase_puls_input.get()
        self.number_phase_level0 = self.number_phase_level_input.get()
        self.puls_amplitude = self.puls_amplitude_input.get()

        # save to cfg file
        seq_variabels = Window_seq.save2cfg(self)
        return seq_variabels

    def save2cfg(self, file="program/setting_sequenz.cfg", file_path=os.path.dirname(sys.argv[0])):

        print("save settings to .cfg file")
        path_settings = os.path.join(file_path, file)
        if not os.path.exists(path_settings):
            print("file Setting not found", path_settings)
            # path_settings = filedialog.askopenfilename(
            #    initialdir='/home/', title='select settings.cfg path')
        print("setting file: ", path_settings)

        configParser_new = configparser.ConfigParser()
        configParser_new["start"] = {}
        configParser_new["start"]["Datum created:"] = str(datetime.now())
        configParser_new["start"]["User created:"] = "User: " + \
            str(os.getlogin())
        configParser_new["start"]["Experiment:"] = str(self.storage)
        configParser_new["start"]["Experiment parameter:"] = str(
            self.puls_freq)

        # puls settings
        # configParser_new["setting"] = {"key0": "value0", "key1": "value1"}
        configParser_new["setting"] = {}
        configParser_new["setting"]["sequenz_type"] = str(self.sequenz_type)
        configParser_new["setting"]["target_freq"] = str(self.target_freq)
        configParser_new["setting"]["band_freq"] = str(self.band_freq)
        configParser_new["setting"]["blank_time"] = str(self.blank_time)
        configParser_new["setting"]["window_time"] = str(self.window_time)

        # configParser_new["setting"]["band_freq"] = str(self.samplerate)
        # configParser_new["setting"]["band_freq"] = str(self.averaging)
        # configParser_new["setting"]["band_freq"] = str(self.repetition_num)

        configParser_new["setting"]["lo_freq"] = str(self.target_freq *
                                                     1000000 - self.band_freq * 1000000)

        # SDR Settings
        # configParser_new["SDR setting"] = {"key0": "value0", "key1": "value1"}
        configParser_new["SDR setting"] = {}
        configParser_new["SDR setting"]["correction_tx_i_dc"] = str(
            self.correction_tx_i_dc)
        configParser_new["SDR setting"]["correction_tx_q_dc"] = str(
            self.correction_tx_q_dc)
        configParser_new["SDR setting"]["correction_tx_i_gain"] = str(
            self.correction_tx_i_gain)
        configParser_new["SDR setting"]["correction_tx_q_gain"] = str(
            self.correction_tx_q_gain)
        configParser_new["SDR setting"]["correction_tx_pahse"] = str(
            self.correction_tx_pahse)

        configParser_new["SDR setting"]["correction_rx_i_dc"] = str(
            self.correction_rx_i_dc)
        configParser_new["SDR setting"]["correction_rx_q_dc"] = str(
            self.correction_rx_q_dc)
        configParser_new["SDR setting"]["correction_rx_i_gain"] = str(
            self.correction_rx_i_gain)
        configParser_new["SDR setting"]["correction_rx_q_gain"] = str(
            self.correction_rx_q_gain)
        configParser_new["SDR setting"]["correction_rx_phase"] = str(
            self.correction_rx_phase)

        configParser_new["SDR setting"]["low_pass_rx"] = str(self.low_pass_rx)
        configParser_new["SDR setting"]["low_pass_tx"] = str(self.low_pass_tx)
        configParser_new["SDR setting"]["gain_rx"] = str(self.gain_rx)
        configParser_new["SDR setting"]["gain_tx"] = str(self.gain_tx)

        configParser_new["Puls"] = {}
        configParser_new["Puls"]["puls_freq"] = str(self.puls_freq)
        configParser_new["Puls"]["puls_duration"] = str(self.puls_duration)
        configParser_new["Puls"]["puls_amplitude"] = str(self.puls_amplitude)
        configParser_new["Puls"]["puls_arangement"] = str(self.puls_arangement)
        configParser_new["Puls"]["puls_count"] = str(len(self.puls_freq))

        configParser_new["Phase"] = {}
        configParser_new["Phase"]["phase_number"] = str(self.phase_number)
        configParser_new["Phase"]["phase_level"] = str(self.phase_level)
        configParser_new["Phase"]["phase_puls"] = str(self.phase_puls)
        configParser_new["Phase"]["number_phase_level"] = str(
            self.number_phase_level)

        configParser_new["Readout"] = {}
        configParser_new["Readout"]["repetition_time"] = str(
            self.repetition_time)
        configParser_new["Readout"]["acquisition_time"] = str(
            self.acquisition_time)
        configParser_new["Readout"]["gate_signal"] = str(self.gate_signal)

        # write configfile
        with open(path_settings, "w") as configfile:
            configParser_new.write(configfile)

        return {s: dict(configParser_new.items(s)) for s in configParser_new.sections()}

    def load_seq(self):
        print("load all variabels from .cfg file")

        seq_variabels = Window_seq.read2cfg(self)

        self.blank_time_input.insert(0, seq_variabels["setting"]["blank_time"])
        self.window_time_input.insert(
            0, seq_variabels["setting"]["blank_time"])

        # read Readout
        self.repetition_time_input.insert(
            0, seq_variabels["Readout"]["repetition_time"])
        self.acquisition_time_input.insert(
            0, seq_variabels["Readout"]["acquisition_time"])
        self.gate_signal_input.insert(
            0, seq_variabels["Readout"]["gate_signal"])

        # read SDR Settings
        self.correction_tx_i_dc_input.insert(
            0, seq_variabels["SDR setting"]["correction_tx_i_dc"])
        self.correction_tx_q_dc_input.insert(
            0, seq_variabels["SDR setting"]["correction_tx_q_dc"])
        self.correction_tx_i_gain_input.insert(
            0, seq_variabels["SDR setting"]["correction_tx_i_gain"])
        self.correction_tx_q_gain_input.insert(
            0, seq_variabels["SDR setting"]["correction_tx_q_gain"])
        self.correction_tx_pahse_input.insert(
            0, seq_variabels["SDR setting"]["correction_tx_pahse"])
        self.correction_rx_i_dc_input.insert(
            0, seq_variabels["SDR setting"]["correction_rx_i_dc"])
        self.correction_rx_q_dc_input.insert(
            0, seq_variabels["SDR setting"]["correction_rx_q_dc"])
        self.correction_rx_i_gain_input.insert(
            0, seq_variabels["SDR setting"]["correction_rx_i_gain"])
        self.correction_rx_q_gain_input.insert(
            0, seq_variabels["SDR setting"]["correction_rx_q_gain"])
        self.correction_rx_phase_input.insert(
            0, seq_variabels["SDR setting"]["correction_rx_phase"])
        self.low_pass_rx_input.insert(
            0, seq_variabels["SDR setting"]["low_pass_rx"])
        self.low_pass_tx_input.insert(
            0, seq_variabels["SDR setting"]["low_pass_tx"])
        self.gain_rx_input.insert(0, seq_variabels["SDR setting"]["gain_rx"])
        self.gain_tx_input.insert(0, seq_variabels["SDR setting"]["gain_tx"])

        # Phase and puls paramterer
        self.phase_number_input.insert(
            0, seq_variabels["Phase"]["phase_number"])
        self.phase_level_input.insert(0, seq_variabels["Phase"]["phase_level"])
        self.phase_puls_input.insert(0, seq_variabels["Phase"]["phase_puls"])
        self.number_phase_level_input.insert(
            0, seq_variabels["Phase"]["number_phase_level"])
        self.puls_amplitude_input.insert(
            0, seq_variabels["Puls"]["puls_amplitude"])

        return seq_variabels

    def read2cfg(self, file_path=os.path.dirname(sys.argv[0]), file="program/setting_sequenz.cfg"):
        " read .cfg file from file "
        path_settings = os.path.join(file_path, file)
        if not os.path.exists(path_settings):
            print("file Setting not found", path_settings)

        configParser = configparser.ConfigParser()
        configParser.read(path_settings)
        setting_dict = {section: dict(configParser.items(section))
                        for section in configParser.sections()}

        print("read from cfg file", setting_dict)
        return setting_dict


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
