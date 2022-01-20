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


def send_sdr(value_main, value_sequenz):
    print("RUN SDR sequenz ")
    print("value_main ", value_main)
    # value_main =
    # {'freq': {'freq_start': '1000', 'freq_end': '2000', 'freq_step': '100', 'freq_repetitions': '10'},
    # 'tunematch': {'tune': '3.3', 'match': '5', 'step': '10', 'lut': '10'},
    # 'load': {'sample': '_test_Sample', 'experiment': '_test_Experiment', 'data': '_test_Data'}
    # 'sequenz': {'sequenz': 'fid'}} # fid, spin, comp, spin_phase,own
    sequenz_select = value_main.get("sequenz").get("sequenz")
    print("value_sequenz ", value_sequenz)
    # {'start': {'datum created:': '2022-01-19 23:26:53.497312', 'user created:': 'User: MALIN Philipp', 'experiment:': "['Experiment initialise']", 'experiment parameter:': '[1.2]'},
    # 'setting': {'sequenz_type': 'fid', 'target_freq': '83.62', 'band_freq': '1.2', 'lo_freq': '82420000.0'},
    # 'SDR setting': {'correction_tx_i_dc': '-45', 'correction_tx_q_dc': '0', 'correction_tx_i_gain': '2047', 'correction_tx_q_gain': '2039', 'correction_tx_pahse': '3',    'correction_rx_i_dc': '0', 'correction_rx_q_dc': '0', 'correction_rx_i_gain': '2047', 'correction_rx_q_gain': '2047', 'correction_rx_phase': '0', 'low_pass_rx': '3000000.0', 'low_pass_tx': '130000000.0', 'gain_rx': '55.0', 'gain_tx': '40.0'},
    # 'Puls': {'puls_freq': '[1.2]', 'puls_duration': '[3e-06]', 'puls_amplitude': '[1]', 'puls_arangement': '[300]', 'puls_count': '1'},
    # 'Phase': {'phase_number': '[4, 1]', 'phase_level': '[0, 1]', 'phase_puls': '[0, 0.7853981633974483]', 'number_phase_level': '1'},
    # 'Readout': {'repetition_time': '5', 'acquisition_time': '82', 'gate_signal': '[1, 0, 50, 10]'}}
    sequenz_select = value_sequenz["setting"]["sequenz_type"]

    print("selected sequenz: ", sequenz_select)
    if sequenz_select == "fid":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value_main, value_sequenz)

    elif sequenz_select == "spin":
        [x_time, y_time, x_freq, y_freq] = seq_spin(value_main, value_sequenz)

    elif sequenz_select == "comp":
        [x_time, y_time, x_freq, y_freq] = seq_comp(value_main, value_sequenz)

    elif sequenz_select == "spin_phase":
        [x_time, y_time, x_freq, y_freq] = seq_fid(value_main, value_sequenz)

    elif sequenz_select == "spin_phase":
        [x_time, y_time, x_freq, y_freq] = seq_spin_phase(
            value_main, value_sequenz)

    elif sequenz_select == "own":
        [x_time, y_time, x_freq, y_freq] = seq_own(value_main, value_sequenz)

    else:
        print("Waring \n sequenz_select dose not exist!! \n", sequenz_select)

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
        for i, value_main in enumerate(x_time):
            wr.writerow([float(x_time[i]), y_time_abs[i], y_time_compex[i]])

    with open(file_freq, 'w', ) as seq_file:
        wr = csv.writer(seq_file, quoting=csv.QUOTE_ALL)
        wr.writerow(["x_freq", "y_freq"])
        for i, value_main in enumerate(x_freq):
            wr.writerow([float(x_freq[i]), float(y_freq[i])])


def seq_fid(value_main, value_sequenz):
    print("fid seq \n", value_main)
    """ file from lukas FIDseq.py adopted """

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
    # number of averages
    l.nav = value_main["freq"]["freq_repetitions"]   # number of repetitions
    # TX I DC correction
    l.nrp = value_sequenz['SDR setting']['repetition_time']
    # TX Q DC correction
    l.tdi = value_sequenz['SDR setting']['correction_tx_i_dc']
    # TX I Gain correction
    l.tdq = value_sequenz['SDR setting']['correction_tx_q_dc']
    # TX Q Gain correction
    l.tgi = value_sequenz['SDR setting']['correction_tx_i_gain']
    # TX phase adjustment
    l.tgq = value_sequenz['SDR setting']['correction_tx_q_gain']
    # RX I Gain correction
    l.tpc = value_sequenz['SDR setting']['correction_tx_pahse']
    # RX Q Gain correction
    l.rgi = value_sequenz['SDR setting']['correction_rx_i_dc']
    # RX I DC correction
    l.rgq = value_sequenz['SDR setting']['correction_rx_q_dc']
    # RX Q DC correction
    l.rdi = value_sequenz['SDR setting']['correction_rx_i_gain']
    # RX phase adjustment
    l.rdq = value_sequenz['SDR setting']['correction_rx_q_gain']
    l.rpc = value_sequenz['SDR setting']['correction_rx_phase']

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
    if (1 == 0):

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
    else:
        raise Exception(" hardware is missing")


def seq_spin(value_main, value_sequenz):
    print("spin seq \n", value_main)
    """ File from Lukas: SpinEchoseq.py adopted """

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = 83.62e6  # 119.3e6#90.4e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    l.sra = 30.72e6                                     # Sampling Rate
    l.nav = 1000                                        # number of averages
    l.nrp = 1                                           # number of repetitions

    l.tdi = -45                                         # TX I DC correction
    l.tdq = 0                                           # TX Q DC correction
    l.tgi = 2047                                        # TX I Gain correction
    l.tgq = 2039                                        # TX Q Gain correction
    l.tpc = 3                                           # TX phase adjustment

    l.rgi = 2047
    l.rgq = 2047
    l.rdi = 0
    l.rdq = 0
    l.rpc = 0
    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    l.trp = 5e-3                                        # repetition time
    l.tac = 82e-6                                       # acquisition time
    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    l.t3d = [1, 0, 50, 10]

    # pulse durations
    l.pfr = [if_frq, if_frq]                            # pulse frequency
    l.pdr = [3e-6, 6e-6]                                # pulse  duration
    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    l.pam = [1, 1]
    # pulse arrangement 300 means 13 us from zero approx. is then start of the first pulse
    l.pof = [300, np.ceil(9e-6*l.sra)]

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
        evran = [34.5, 54.5]

        # np.where sometimes does not work out, so it is put in a try except
        # always check the console for errors
        try:
            evidx = np.where((l.HDF.tdx > evran[0]) & (
                l.HDF.tdx < evran[1]))[0]
        except:
            print("error due to np.where evaluation!")

        # time domain x and y data
        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]

        # correcting a offset in the time domain by subtracting the mean
        tdy_mean = tdy-np.mean(tdy)

        # fft of the corrected time domain data
        fdy1 = fftshift(fft(tdy_mean, axis=0), axes=0)

        # fft freq and fft shift is here used to scale the x axis (frequency axis)
        fdx1 = fftfreq(len(fdy1))*l.sra/1e6
        fdx1 = fftshift(fdx1)

        # scaling factor which converts the y axis (usually a proportional number of points) into uV
        fac_p_to_uV = 447651/1e6

        tdy_mean = tdy_mean/l.nav/fac_p_to_uV/RX_gainfactor

        # plt.figure(1);
        # plt.plot(tdx,tdy_mean)
        # plt.xlabel("t in µs")
        # plt.ylabel("Amplitude in µV")
        # plt.show()

        # get LO frequency and add it to the base band fft x-Axis in order to illustrate the applied frequency
        # for single side spectrum and shift (only single frequency)
        lof = l.HDF.attr_by_key('lof')

        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6

        shifter = 12
        stopper = 270

        # here the right side of the spectrum is selected
        y = abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper])
                )//l.nav/len(tdx)/447651*1e6/RX_gainfactor
        x = fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]
        print("std rms frequency domain next to peak X: " + str(np.std(y)))

        # plt.figure(2);
        # plt.plot(x, y)
        # plt.xlabel("f in MHz")
        # plt.ylabel("Amplitude in µV")
        # plt.title("double sided spectrum with phase cycling")
        # plt.show()

        print("MAX of Signal: " + str(max(y)))

        return tdx, tdy_mean, x, y
    else:
        raise Exception(" hardware is missing")


def seq_comp(value_main, value_sequenz):

    print("comp seq \n", value_main)
    """ File from Lukas: CompositePulseseq.py adopted """

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = 83.62e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    l.sra = 30.72e6                                     # Sampling Rate
    l.nav = 250                                         # number of averages
    l.nrp = 1                                           # number of repetitions

    l.tdi = -45                                         # TX I DC correction
    l.tdq = 0                                           # TX Q DC correction
    l.tgi = 2047                                        # TX I Gain correction
    l.tgq = 2039                                        # TX Q Gain correction
    l.tpc = 3                                           # TX phase adjustment

    l.rgi = 2047
    l.rgq = 2047
    l.rdi = 0
    l.rdq = 0
    l.rpc = 0

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    l.trp = 5e-3                                        # repetition time
    l.tac = 82e-6                                       # acquisition time
    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    l.t3d = [1, 0, 50, 10]

    # phase cycling definitions
    # number of phases (here we only need 4 phases, but the programm cycles now in steps of 45 degree and we always need those 45 degree steps)
    l.pcn = [1, 4]
    # l.pcl = [0,1]                                        # pcyc level (only needed if more then 1 pulse is used (and a relative / different phase is necessary), so only Spin Echo needs/ uses it)
    l.pph = [0, np.pi/4]
    # l.pba = 1

    # pulse durations
    l.pfr = [if_frq, if_frq]                            # pulse frequency
    l.pdr = [3e-6, 6e-6]                                # pulse  duration

    # relative pulse amplitude
    l.pam = [1, 1]
    # pulse arrangement 1 means immediate start of the pulse
    l.pof = [300, np.ceil(3e-6*l.sra)]

    # l.pph = [0, np.pi/2]

    l.npu = len(l.pfr)                              # number of pulses

    l.rgn = 55.0                                            # RX gain
    l.tgn = 40.0                                            # TX gain
    # l.tgn = 30 # for noise measurements

    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    l.rlp = 3.0e6                                          # RX Base-Band BW
    l.tlp = 130.0e6                                         # TX Base-Band BW

    l.spt = './pulse/FID'                                  # directory to save to
    l.fpa = 'setup'

    l.run()

    if (1 == 0):

        l.readHDF()

        evran = [27.5, 47.5]

        evidx = np.where((l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]))[0]

        print(type(evran[0]))

        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]

        tdy_mean_self = tdy
        tdy_mean = tdy-np.mean(tdy)

        tdy_mean_0_45 = tdy_mean[:, 0]
        tdy_mean_0_135 = tdy_mean[:, 1]
        tdy_mean_0_m135 = tdy_mean[:, 2]
        tdy_mean_0_m45 = tdy_mean[:, 3]

        tdy_comp = (-tdy_mean_0_45 + tdy_mean_0_135 -
                    tdy_mean_0_m135 + tdy_mean_0_m45)

        tdy_time = tdy_comp/l.nav/447651*1e6

        fdy1 = fftshift(fft(tdy_mean, axis=0), axes=0)

        fdy2 = fftshift(fft(tdy, axis=0), axes=0)

        fdy_comp = fftshift(fft(tdy_comp, axis=0), axes=0)

        # print(len(fdy1))

        fdx1 = fftfreq(len(fdy1))*30.72
        fdx1 = fftshift(fdx1)

        fdx_comp = fftfreq(len(fdy_comp))*30.72
        fdx_comp = fftshift(fdx_comp)

        # get rid of dc offset
        nums = np.shape(fdy1)[1]

        # plt.figure(1);
        # plt.plot(tdx,tdy_comp/l.nav/447651*1e6)
        #plt.xlabel("t in µs")
        #plt.ylabel("Amplitude in µV")
        # plt.show()

        lof = l.HDF.attr_by_key('lof')

        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6
            # print(fdx1[i])

        # fft of composite pulsed sequence
        shifter = 12  # 0#50
        stopper = 270  # 300

        y = abs(
            (fdy_comp[int(len(fdy_comp)/2)+shifter:len(fdy_comp)-1-stopper]))
        x = fdx1[int(len(fdy_comp)/2)+shifter:len(fdy_comp)-1-stopper]

        y_freq = y/l.nav/len(tdx)/447651*1e6/RX_gainfactor

        print("std rms frequency domain next to peak X: " +
              str(np.std(y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)))

        # plt.figure(2);
        #plt.plot(x, y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)
        #plt.xlabel("f in MHz")
        #plt.ylabel("Amplitude in µV")
        # plt.title("composite")
        # plt.show()

        return tdx, tdy_time, x, y_freq
    else:
        raise Exception(" hardware is missing")


def seq_spin_phase(value_main, value_sequenz):
    print("spin_phase seq \n", value_main)
    """ file from Lukas SpinEchoPhaseCyclingseq.py adopted """

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    def phase_shift(iptsignal, angle):
        # Resolve the signal's fourier spectrum
        spec = fft(iptsignal)
        #freq = rfftfreq(iptsignal.size, d=dt)

        # Perform phase shift in freqeuency domain
        # default it was +1.0j
        spec *= np.exp(-1.0j * np.deg2rad(angle))

        # Inverse FFT back to time domain
        phaseshift = ifft(spec, n=len(iptsignal))
        return

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = 83.62e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target7 frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    l.sra = 30.72e6                                     # Sampling Rate
    l.nav = 250                                        # number of averages
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

    l.pcn = [4, 1]                                      # number of phases
    l.pph = [0, np.pi/2]  # pulse phase (added to phase shift due to pcn)

    # pulse durations
    l.pfr = [if_frq, if_frq]                            # pulse frequency
    l.pdr = [3e-6, 6e-6]                                # pulse  duration
    # relative pulse amplitude
    l.pam = [1, 1]
    # pulse arrangement (first one is triggered then second one after 15 us)
    l.pof = [300, np.ceil(9e-6*l.sra)]

    l.npu = len(l.pfr)                                  # number of pulses

    # RX gain between 5 and 55 (usually 40 was used, 55 better and maximum)
    l.rgn = 55.0
    l.tgn = 40.0                                        # TX gain

    # RX gain was set to 40 dB when the scaling facotr from points to V was determined - so a higher or lower values then 40 need correction for the plots
    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    l.rlp = 3.0e6                                        # RX BW
    l.tlp = 130.0e6                                      # RX BW

    l.spt = './pulse/SCAN'                              # directory to save to
    l.fpa = 'setup'

    # call to program
    l.run()

    # read back and post-processing
    if (1 == 1):

        l.readHDF()

        # select range which should be investigated (ECHO time setting)
        evran = [35, 55]

        evidx = np.where((l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]))[0]

        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]

        tdy_mean = tdy-np.mean(tdy)

        # take RX time domain data from hdf5 file
        tdy_mean_0_90 = tdy_mean[:, 0]
        tdy_mean_90_90 = tdy_mean[:, 1]
        tdy_mean_180_90 = tdy_mean[:, 2]
        tdy_mean_270_90 = tdy_mean[:, 3]

        # use function to shift RX phaseaccordingly to kazan (therefore k1, k2, k3, k4)
        k1 = tdy_mean_0_90
        k2 = phase_shift(tdy_mean_90_90, 270)
        k3 = phase_shift(tdy_mean_180_90, 180)
        k4 = phase_shift(tdy_mean_270_90, 90)

        tdy_mean_self = (k1+k2+k3+k4)
        tdy_time = tdy_mean_self/l.nav/447651*1e6/RX_gainfactor/4

        # #plot resulting time domain data and scale it to uV
        # plt.figure(1);
        # plt.plot(tdx, tdy_time)
        # plt.xlabel("t in µs")
        # plt.ylabel("Amplitude in µV")
        # plt.show()

        fdy1 = fftshift(fft(tdy_mean_self, axis=0), axes=0)

        fdx1 = fftfreq(len(fdy1))*l.sra/1e6
        fdx1 = fftshift(fdx1)

        # for single side spectrum and shift (only single frequency)
        lof = l.HDF.attr_by_key('lof')

        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6

        shifter = 12
        stopper = 270

        # here the right side of the spectrum is selected
        y = abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper])
                )//l.nav/len(tdx)/447651*1e6/4/RX_gainfactor
        x = fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]
        print("std rms frequency domain next to peak X: " + str(np.std(y)))
        print("MAX of Signal: " + str(max(y)))

        # plt.figure(2)
        # plt.plot(x, y)
        # plt.xlabel("f in MHz")
        # plt.ylabel("Amplitude in µV")
        # plt.title("double sided spectrum with phase cycling")
        # plt.show()

        return tdx, tdy_time, x, y
    else:
        raise Exception(" hardware is missing")


def seq_own(value_main, value_sequenz):
    print("fid sspin_phaseeq \n", value_main)
    """own Sequenz """

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1


def send_tune_match(tune, match, tm_step, tm_lut):
    print("start tune and match sequenz on Arduino ")
    print("tune ", tune)
    print("match ", match)
    print("tm_step ", tm_step)
    print("tm_lut ", tm_lut)
