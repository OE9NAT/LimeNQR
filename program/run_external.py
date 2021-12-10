import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq
import limr

import csv


print("RUN sequenz")

# class RUN_SDR():
#
#    def __init__(self, *args):
#
#    @property
#    def run_sdr(self):
#
#        print("run SDR sequenz")


def send_sdr(value):
    print("RUN SDR sequenz ")
    print("value ", value)
    # value =
    # {'freq': {'freq_start': '1000', 'freq_end': '2000', 'freq_step': '100', 'freq_repetitions': '10'},
    # 'tunematch': {'tune': '3.3', 'match': '5', 'step': '10', 'lut': '10'},
    # 'load': {'sample': '_test_Sample', 'experiment': '_test_Experiment', 'data': '_test_Data'}
    # 'sequenz': {'sequenz': 'fid'}} # fid, spin, comp, spin_phase,own
    sequenz_select = value.get("sequenz").get("sequenz")

    print("selected sequenz: ", sequenz_select)
    if sequenz_select == "fid":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value)

    if sequenz_select == "spin":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value)

    if sequenz_select == "comp":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value)

    if sequenz_select == "spin_phase":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value)

    if sequenz_select == "spin_phase":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value)

    # store aquiried data to filestrukture
    # [22.52604167 22.55859375 22.59114583 22.62369792 22.65625 ]
    # x_time = [s.strip('\n') for s in x_time.tolist()]
    x_time = x_time.tolist()
    print(" x_time ", x_time[:10])

    # [[0.29129709-1.52607999j] [0.53282316-0.78878987j] [0.88875632-1.65319897j] [1.04129911-1.4370967j ] [0.20866975-0.43285671j]]
    y_time_abs = [abs(val) for sublist in y_time for val in sublist]
    y_time_compex = [val for sublist in y_time for val in sublist]
    print(" y_time_abs ", y_time_abs[:5])
    # abs([0.88875632-1.65319897j]) !!!!

    # [83.02038574 83.07041931 83.12045288 83.17048645 83.22052002]
    x_freq = x_freq.tolist()
    print(" x_freq ", x_freq[:5])

    # [[0.20988999] [0.06322438] [0.30136686] [0.06902654] [0.22243679]]
    y_freq = [val for sublist in y_freq for val in sublist]
    print(" y_freq ", y_freq[:5])

    print("type x_time", type(x_time))  # type y_freq <class 'list'>
    print("type y_time_abs", type(y_time_abs))  # type y_freq <class 'list'>
    print("type x_freq", type(x_freq))  # type y_freq <class 'list'>
    print("type y_freq", type(y_freq))  # type y_freq <class 'list'>

    file_time = os.path.join("program", "scan_data_time.csv")
    file_freq = os.path.join("program", 'scan_data_freq.csv')

    with open(file_time, 'w', ) as seq_file:
        wr = csv.writer(seq_file, quoting=csv.QUOTE_ALL)
        wr.writerow(["x_time", "y_time_abs", "y_time_complex"])
        for i, value in enumerate(x_time):
            wr.writerow([float(x_time[i]), y_time_abs[i], y_time_compex[i]])

    with open(file_freq, 'w', ) as seq_file:
        wr = csv.writer(seq_file, quoting=csv.QUOTE_ALL)
        wr.writerow(["x_freq", "y_freq"])
        for i, value in enumerate(x_freq):
            wr.writerow([float(x_freq[i]), float(y_freq[i])])


def seq_fid(value):
    print("test")
    print("fid seq \n", value)

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = 83.62e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target7 frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    l.sra = 30.72e6                                     # Sampling Rate
    l.nav = 1000                                        # number of averages
    l.nrp = 1                                           # number of repetitions

    l.tdi = -45                                         # TX I DC correction
    l.tdq = 0                                           # TX Q DC correction
    l.tgi = 2047                                        # TX I Gain correction
    l.tgq = 2039                                        # TX Q Gain correction
    l.tpc = 3                                           # TX phase adjustment

    l.rgi = 2047                                        # RX I Gain correction
    l.rgq = 2047                                        # RX Q Gain correction
    l.rdi = 0                                           # RX I DC correction
    l.rdq = 0                                           # RX Q DC correction
    l.rpc = 0                                           # RX phase adjustment

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size
    l.trp = 5e-3                                        # repetition time
    # acquisition time (gives minimum buffer size)
    l.tac = 82e-6
    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    l.t3d = [1, 0, 50, 10]

    # pulse durations
    l.pfr = [if_frq]                                    # pulse frequency
    l.pdr = [3e-6]                                      # pulse  duration
    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    l.pam = [1]
    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)
    l.pof = [300]

    l.npu = len(l.pfr)                                  # number of pulses

    l.rgn = 55.0                                        # RX gain
    l.tgn = 40.0                                        # TX gain

    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    # RX BW (IF or base band low pass filter)
    l.rlp = 3.0e6
    l.tlp = 130.0e6                                     # RX BW

    l.spt = './pulse/FID'                              # directory to save to
    l.fpa = 'setup'

    l.run()

    # read back file and plot time signal + shifted fft
    if (1 == 1):

        # reads back the file which was recently saved
        l.readHDF()

        # evaluation range, defines: blanking time and window length
        evran = [22.5, 42.5]

        # np.where sometimes does not work out, so it is put in a try except
        # always check the console for errors

        evidx = np.where((l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]))[0]

        # time domain x and y data
        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]

        # correcting a offset in the time domain by subtracting the mean
        tdy_mean = tdy-np.mean(tdy)

        # fft of the corrected time domain data
        fdy1 = fftshift(fft(tdy_mean, axis=0), axes=0)

        # fft freq and fft shift is here used to scale the x axis (frequency axis)
        fdx1 = fftfreq(len(fdy1))*30.72
        fdx1 = fftshift(fdx1)

        # scaling factor which converts the y axis (usually a proportional number of points) into uV
        fac_p_to_uV = 447651/1e6

        tdy_mean = tdy_mean/l.nav/fac_p_to_uV/RX_gainfactor

        plt.figure(1)
        plt.plot(tdx, tdy_mean)  # zeit plot
        plt.xlabel("t in µs")
        plt.ylabel("Amplitude in µV")
        # plt.show()

        # get LO frequency and add it to the base band fft x-Axis in order to illustrate the applied frequency
        # for single side spectrum and shift (only single frequency)
        lof = l.HDF.attr_by_key('lof')

        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6

        # cutting out the window of the interessting part of the computed fft spectrum (here from 83 - 84 MHz)
        # window of interest
        shifter = 12  # 0#50
        stopper = 270  # 300
        # here the right side of the spectrum is selected
        y = abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper])) / \
            len(tdx)/fac_p_to_uV/l.nav/RX_gainfactor
        x = fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]

        plt.figure(5)
        plt.plot(x, y)  # freq plot
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        # plt.show()

        # print std (for SNR determination -> noise analysis without sample)
        print("std rms frequency domain next to peak X: " + str(np.std(y)))
        # print max of fft (for SNR evaluation - should give peak maximum)
        print("MAX of Signal: " + str(max(y)))

        return tdx, tdy_mean, x, y


def send_tune_match(tune, match, tm_step, tm_lut):
    print("start tune and match sequenz on Arduino ")
    print("tune ", tune)
    print("match ", match)
    print("tm_step ", tm_step)
    print("tm_lut ", tm_lut)
