import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import limr
from scipy.fftpack import fft, fftshift, fftfreq, ifft, ifftshift
import csv
import serial
import time
#from subprocess import call, Popen
#import itertools


print("RUN sequenz")

external_hardware = True  # False True
if os.environ.get('OS', '') == 'Windows_NT':
    external_hardware = False

#save_dh5_file = './pulse/FID'
save_dh5_file = './log/dh5_file'


# helper fuktion
def string2array(value):
    """Format string to a array which is seperated by a ","

    :param value: a long string to be split 
    :type value: str
    :return: array of split of handed over sring 
    :rtype: array

    :Example:
    >>> [1.2 ,1.3 ,1.4 ,1.5 ,1.6 ,1.7  ] = string2array("[1.2,1.3,1.4,1.5,1.6,1.7]")

    """
    value = value.replace("[", "").replace("]", "")
    value = value.split(",")
    # print("def string2array", value)
    return [float(i)for i in value]

# sequenz selection


def send_sdr(value_main, value_sequenz):
    """Execution of the sequence from the main window.
    It will hand over the parameters to the sequence what will send all parameterst to the sdr and will control the execution of the sequence.
    It handels the returened data from the sequence and will save it to set filestrukture

    :param value_main: all parameterst structured from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters structured dependent on the sequence
    :type value_sequenz: dict

    :Example:

    >>> run_external.send_sdr(self.get_values(), self.value_sequenz)     
    value_main =
     {'freq': {'freq_start': '80', 'freq_end': '100', 'freq_step': '100', 'freq_repetitions': '10'},
     'tunematch': {'tune': '3.3', 'match': '5', 'step': '10', 'lut': '10'},
     'load': {'sample': '_test_Sample', 'experiment': '_test_Experiment', 'data': '_test_Data'}
     'sequenz': {'sequenz': 'fid'}} # fid, spin, comp, spin_phase,own
    sequenz_select = {'start': {'datum created:': '2022-01-19 23:26:53.497312', 'user created:': 'User: laborPC', 'experiment:': "['Experiment initialise']", 'experiment parameter:': '[1.2]'},
     'setting': {'sequenz_type': 'fid', 'target_freq': '83.62', 'band_freq': '1.2', 'lo_freq': '82420000.0'},
     'SDR setting': {'correction_tx_i_dc': '-45', 'correction_tx_q_dc': '0', 'correction_tx_i_gain': '2047', 'correction_tx_q_gain': '2039', 'correction_tx_pahse': '3',    'correction_rx_i_dc': '0', 'correction_rx_q_dc': '0', 'correction_rx_i_gain': '2047', 'correction_rx_q_gain': '2047', 'correction_rx_phase': '0', 'low_pass_rx': '3000000.0', 'low_pass_tx': '130000000.0', 'gain_rx': '55.0', 'gain_tx': '40.0'},
     'Puls': {'puls_freq': '[1.2]', 'puls_duration': '[3e-06]', 'puls_amplitude': '[1]', 'puls_arangement': '[300]', 'puls_count': '1'},
     'Phase': {'phase_number': '[4, 1]', 'phase_level': '[0, 1]', 'phase_puls': '[0, 0.7853981633974483]', 'number_phase_level': '1'},
     'Readout': {'repetition_time': '5', 'acquisition_time': '82', 'gate_signal': '[1, 0, 50, 10]'}}

    """

    print("RUN SDR sequenz ")
    print("value_main ", value_main)

    sequenz_select = value_main.get("sequenz").get("sequenz")
    print("value_sequenz ", value_sequenz)

    sequenz_select = value_sequenz["setting"]["sequenz_type"]

    print("selected sequenz: ", sequenz_select)
    sequenz_freq_step = int(value_main.get("freq").get("freq_step"))
    print("frequenzy step, singel=1 or multi-band>1:", sequenz_freq_step)
    if sequenz_select == "fid":

        if sequenz_freq_step > 2:
            # Frequency band
            [x_time, y_time, x_freq, y_freq] = broad_seq_fid(
                value_main, value_sequenz)

        else:
            # one Frequency
            [x_time, y_time, x_freq, y_freq] = seq_fid(
                value_main, value_sequenz)

    elif sequenz_select == "spin":
        [x_time, y_time, x_freq, y_freq] = seq_spin(value_main, value_sequenz)

    elif sequenz_select == "comp":
        [x_time, y_time, x_freq, y_freq] = seq_comp(value_main, value_sequenz)

    elif sequenz_select == "spin_phase":
        [x_time, y_time, x_freq, y_freq] = seq_spin_phase(
            value_main, value_sequenz)

    elif sequenz_select == "own":
        [x_time, y_time, x_freq, y_freq] = seq_own(value_main, value_sequenz)

    else:
        print("Waring \n sequenz_select dose not exist!! \n", sequenz_select)

    print("\n  \n return values from sequenz")
    # store aquiried data to filestrukture
    # [22.52604167 22.55859375 22.59114583 22.62369792 22.65625 ]
    # x_time = [s.strip('\n') for s in x_time.tolist()]
    print(" x_time \n", x_time[:10])
    x_time = list(x_time)
    #x_time = x_time.tolist()
    print(" x_time \n", x_time[:10])
    print(type(y_time[0][0]), y_time[0], " y_time \n", y_time[:10])
    # <class 'numpy.complex128'> [(13.582009199130573-47.17961090224304j)]  y_time

    # [[0.29129709-1.5607999j] [0.53282316-0.78878987j] [0.88875632-1.65319897j] [1.04129911-1.4370967j ] [0.20866975-0.43285671j]]
    y_time_abs = [np.real(val) for sublist in y_time for val in sublist]
    y_time_compex = [val for sublist in y_time for val in sublist]
    print(" y_time_abs\n ", y_time_abs[:5])
    # abs([0.88875632-1.65319897j]) !!!!

    # [83.02038574 83.07041931 83.12045288 83.17048645 83.22052002]
    x_freq = x_freq.tolist()
    print(" x_freq\n ", x_freq[:5])

    # [[0.20988999] [0.06322438] [0.30136686] [0.06902654] [0.22243679]]
    y_freq = [val for sublist in y_freq for val in sublist]
    print(" y_freq\n ", y_freq[:5])

    print("type x_time", type(x_time))  # type y_freq <class 'list'>
    print("type y_time_abs", type(y_time_abs))  # type y_freq <class 'list'>
    print("type x_freq", type(x_freq))  # type y_freq <class 'list'>
    # type y_freq <class 'list'>
    print(len(y_freq), "type y_freq", type(y_freq))

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
    """singel frequency Free Induction Decay (FID) sequence measurment

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = seq_fid(value_main, value_sequenz)
    """

    print("fid seq \n", value_main)

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    # hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = float(value_main["freq"]["freq_start"]) * 10 ** (6)
    tgtfreq = 83.56e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target7 frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    # Sampling Rate
    l.sra = 30.72e6
    # number of averages
    l.nav = float(value_sequenz["setting"]["num_averages"])
    # number of repetitions

    l.nrp = float(value_sequenz['setting']['repetition_num'])
    # TX I DC correction
    l.tdi = float(value_sequenz['SDR setting']['correction_tx_i_dc'])
    # TX Q DC correction
    l.tdq = float(value_sequenz['SDR setting']['correction_tx_q_dc'])
    # TX I Gain correction
    l.tgi = float(value_sequenz['SDR setting']['correction_tx_i_gain'])
    # TX Q Gain correction
    l.tgq = float(value_sequenz['SDR setting']['correction_tx_q_gain'])
    # TX phase adjustment
    l.tpc = float(value_sequenz['SDR setting']['correction_tx_pahse'])
    # RX I Gain correction
    l.rgi = float(value_sequenz['SDR setting']['correction_rx_i_dc'])
    # RX Q Gain correction
    l.rgq = float(value_sequenz['SDR setting']['correction_rx_q_dc'])
    # RX I DC correction
    l.rdi = float(value_sequenz['SDR setting']['correction_rx_i_gain'])
    # RX Q DC correction
    l.rdq = float(value_sequenz['SDR setting']['correction_rx_q_gain'])
    # RX phase adjustment
    l.rpc = float(value_sequenz['SDR setting']['correction_rx_phase'])

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    # repetition time = 5e-3
    l.trp = float(value_sequenz['Readout']['repetition_time']) * 10 ** (-3)

    # acquisition time (gives minimum buffer size) =82e-6
    l.tac = float(value_sequenz['Readout']['acquisition_time']) * 10 ** (-6)

    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    value = value_sequenz['Readout']['gate_signal'].split(" ")
    l.t3d = [int(i)for i in value]   # [1, 0, 50, 10]

    # pulse durations
    # pulse frequency
    # l.pfr = [if_frq]
    l.pfr = [if_frq for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    # pulse  duration
    l.pdr = string2array(value_sequenz['Puls']['puls_duration'])  # [3e-6]

    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    l.pam = [value_sequenz['Puls']['puls_amplitude']
             for i in range(0, int(value_sequenz['Puls']['number_pulses']))]  # [1]
    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)
    l.pof = string2array(value_sequenz['Puls']['puls_arangement'])  # [300]

    l.npu = len(l.pfr)                                  # number of pulses

    l.rgn = float(value_sequenz['SDR setting']['gain_rx'])  # 55.0    # RX gain
    l.tgn = float(value_sequenz['SDR setting']['gain_tx'])  # 40.0  # TX gain

    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    # RX BW (IF or base band low pass filter)
    l.rlp = 3.0e6
    l.tlp = 130.0e6                                     # RX BW

    l.spt = save_dh5_file                            # directory to save to
    l.fpa = 'setup'

    print("\n ________\n", "start sequenz", "\n ________\n")
    l.run()

    # read back file and plot time signal + shifted fft
    if (1 == external_hardware):

        # reads back the file which was recently saved
        l.readHDF()

        # evaluation range, defines: blanking time and window length
        evran = [float(value_sequenz['setting']['blank_time']),
                 float(value_sequenz['setting']['window_time'])]  # [22.5, 42.5]

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
        fac_p_to_uV = float(
            value_sequenz['SDR setting']['factor_point2volts'])  # 447651/1e6
        # fac_p_to_uV = 447651/1e6
        tdy_mean = tdy_mean/l.nav

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
            len(tdx)/l.nav
        x = fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]

        plt.figure(5)
        plt.plot(x, y)  # freq plot
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        # plt.show()

        # print std (for SNR determination -> noise analysis without sample)
        print("std rms frequency domain next to peak X: " + str(np.std(y)))
        # print max of fft (for SNR evaluation - should give peak maximum)
        print(type(y[0]), "value y", y)
        print("MAX of Signal: " + str(max(y)))

        return tdx, tdy_mean, x, y  # time x-y , freq x-y
    else:
        raise Exception(" hardware is missing")


def broad_seq_fid(value_main, value_sequenz):
    """multi frequency Free Induction Decay (FID) sequence measurment

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = broad_seq_fid(value_main, value_sequenz)

    """

    print("broad frequency FID")

    U_Tune_max = 5.0  # max voltage for tuning cap
    #U_Tune_max = value_main.get("tunematch").get("tune")
    U_Match_max = 5.0  # max voltage for matching cap
    #U_Match_max = value_main.get("tunematch").get("match")

    #vec = list()
    #ref = list()
    ut = list()
    um = list()
    #ref_list = list()
    freqList = list()

    start_flag = 'Set_Voltage\n'
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
    time.sleep(1)

    arduino.write(start_flag.encode())

    filename = './program/scantry2.csv'
    TMfile = './program/TM83_84.csv'
    averages = 5000
    sampleRate = 30.72e6

    # open Tune-Match file and load the voltages and frequencies into seperate arrays
    with open(TMfile) as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        data = [(float(col1), float(col2), float(col3))
                for col1, col2, col3 in reader]

    np_data = np.asarray(data)

    print(np.shape(np_data))

    for freq in range(0, np.shape(np_data)[0]):
        freqList.append(np_data[freq][0])
    freqList = np.asarray(freqList)

    for utval in range(0, np.shape(np_data)[0]):
        ut.append(np_data[utval][1])
    ut = np.asarray(ut)

    for umval in range(0, np.shape(np_data)[0]):
        um.append(np_data[umval][2])
    um = np.asarray(um)

    # calculate the frequency step by the difference of two frequencies in the Tune-Match file
    freq_step = (freqList[1]-freqList[0])

    l = limr.limr('./program/pulseN_test_USB.cpp')  # ('./pulseN_test_USB.cpp')
    l.sra = 30.72e6                                      # Sampling Rate
    l.nav = float(value_sequenz["setting"]["num_averages"])

    def seq(tgtfreq):
        # IF or base band frequency
        if_frq = 1.2e6

        l.lof = tgtfreq-if_frq                                  # LO frequency
        # l.sra = 30.72e6                                      # Sampling Rate

        # number of averages
        #l.nav = float(value_sequenz["setting"]["num_averages"])
        l.nrp = 1                                               # number of repetitions

        # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size)
        l.trp = 5e-3                                            # repetition time
        l.tac = 82e-6                                           # acquisition time
        # GPIO Pin3 is centered around the pulse
        l.t3d = [1, 10, 53, 10]

        l.tdi = -32                                             # TX I DC correction
        l.tdq = 50                                              # TX Q DC correction
        l.tgi = 2047                                            # TX I Gain correction
        l.tgq = 2041                                            # TX Q Gain correction
        l.tpc = 1                                               # TX phase adjustment

        l.pfr = [if_frq]
        l.pdr = [16e-6]
        l.pam = [1]
        l.pof = [300]

        # number of pulses
        l.npu = len(l.pfr)

        l.rgn = 55.0                                            # RX gain
        l.tgn = 50.0                                            # TX gain

        l.rlp = 3.0e6                                           # RX BW
        l.tlp = 130.0e6                                         # RX BW

        l.spt = './pulse/FID'                                  # directory to save to
        l.fpa = 'setup'

        l.run()

        # read back file and plot time signal + shifted fft
        if (1 == external_hardware):

            # reads back the file which was recently saved
            l.readHDF()

            # evaluation range, defines: blanking time and window length
            evran = [36.5, 56.5]

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

            # get LO frequency and add it to the base band fft x-Axis in order to illustrate the applied frequency
            # for single side spectrum and shift (only single frequency)
            lof = l.HDF.attr_by_key('lof')

            for i in range(0, len(fdx1)):
                fdx1[i] = fdx1[i]+lof[0]/1e6

            # shifter takes the whole fft and shifts it away from zero point (zer0 if offset = 0 or low)
            # window of interest
            shifter = 50
            stopper = 0

            # here the right side of the spectrum is selected
            y = abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]))
            x = fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]

            # calculate the idices which are in the excitation range to cut it out of the recorded spectrum
            excitation_indeces = np.where(
                (x > tgtfreq/1e6) & (x <= ((tgtfreq+freq_step)/1e6)))

            # print number of the cut out points
            print("points per scan: " + str(len(excitation_indeces)))

            x_exc = x[excitation_indeces]

            y_exc = np.asarray(y[excitation_indeces])

            # look if the filename exists or if new file needs to be produced
            # if not, create file and write the header into it
            if(os.path.isfile(filename) == 0):
                print("Filename not given yet - new file will be generated!")
                f = open(filename, 'w')
                f.write('frequency\tamplitude\n')
                f.close()

            # if existing file, append recorded data
            else:
                print("File does already exist, scan data will be appended!")

            for i in range(0, len(x_exc)):
                f = open(filename, 'a')
                f.write(str(x_exc[i])+'\t'+str(y_exc[i, 0])+'\n')
                f.close()

    for i in range(0, len(um)):
        # set voltages for certain frequency
        start_flag = 'Set_Voltage\n'
        arduino.write(start_flag.encode())
        UT = int(ut[i]*4095/U_Tune_max)
        UM = int(um[i]*4095/U_Match_max)

        UT = str(UT)
        UM = str(UM)

        # send the voltages to the Arduino
        if (arduino.readline().decode() == 'ready\n'):
            arduino.write(UT.encode() + b'\n')
            arduino.write(b'stop\n')

            arduino.write(UM.encode() + b'\n')
            arduino.write(b'stop\n')

            if (arduino.readline().decode() == 'done\n'):
                print('\nSuccessfully sent: \n')
                print('Tune-voltage: ' + arduino.readline().decode())
                print('Match-voltage: ' + arduino.readline().decode())
            else:
                print('Error by sending data to Arduino')

        # print the current frequency which will be applied
        print("\n")
        print("Current Excitation Frequency: " + str(freqList[i]/1e6) + " MHz")
        print("\n")
        # call the FIDcut. sequence to carry out the experiment at the frequency step
        seq(freqList[i])
    # close arduino connection
    arduino.close()

    # plot the resulting spectrum of the whole scan
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        data = [(float(col1), float(col2))
                for col1, col2, in reader]

    np_data = np.asarray(data)

    print(np_data)

    plt.figure(10)
    plt.plot(np_data[:, 0], np_data[:, 1])
    plt.xlabel("f in MHz")
    plt.ylabel("Amplitude")
    # plt.show()

    print("STD: " + str(np.std(np_data[:, 1])))

    x_time = np.array([22.0, 22.1, 22.2, 22.3, 22.4,
                      22.5, 22.6, 22.7, 22.8, 22.9])
    y_time = [0.2+9.70j, -1.5+3.0j, -2.0 + 5.31j, -0.1+3.0j, -0.1 -
              0.4j, 0.4-2.3j, 1.3-3.3j, -0.5-4.1j, -1.7-6.4j, -1.9-7.0j]
    y_time = [0.3+i + 1.50j for i in range(10)]
    y_time = [[np.complex128(i)]for i in y_time]

    x_freq = np.array(np_data[:, 0])
    y_freq = np.array([[np.array(i)]for i in np_data[:, 1]])

    if (1 == external_hardware):
        #print("np_data[:, 0]", np_data[:, 0])
        #print("np_data[:, 1]", np_data[:, 1])
        return x_time, y_time, x_freq, y_freq  # time x-y , freq x-y
    else:
        raise Exception(" hardware is missing")


def seq_spin(value_main, value_sequenz):
    """Spin-Echo sequence 

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = seq_spin(value_main, value_sequenz)
    """

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
    sample_rate_sdr = 30.72e6
    l.sra = sample_rate_sdr                                   # Sampling Rate
    l.nav = 1000                                        # number of averages

    l.nrp = float(value_sequenz['setting']['repetition_num'])
    # TX I DC correction
    l.tdi = float(value_sequenz['SDR setting']['correction_tx_i_dc'])
    # TX Q DC correction
    l.tdq = float(value_sequenz['SDR setting']['correction_tx_q_dc'])
    # TX I Gain correction
    l.tgi = float(value_sequenz['SDR setting']['correction_tx_i_gain'])
    # TX Q Gain correction
    l.tgq = float(value_sequenz['SDR setting']['correction_tx_q_gain'])
    # TX phase adjustment
    l.tpc = float(value_sequenz['SDR setting']['correction_tx_pahse'])
    # RX I Gain correction
    l.rgi = float(value_sequenz['SDR setting']['correction_rx_i_dc'])
    # RX Q Gain correction
    l.rgq = float(value_sequenz['SDR setting']['correction_rx_q_dc'])
    # RX I DC correction
    l.rdi = float(value_sequenz['SDR setting']['correction_rx_i_gain'])
    # RX Q DC correction
    l.rdq = float(value_sequenz['SDR setting']['correction_rx_q_gain'])
    # RX phase adjustment
    l.rpc = float(value_sequenz['SDR setting']['correction_rx_phase'])

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    # repetition time = 5e-3
    l.trp = float(value_sequenz['Readout']['repetition_time']) * 10 ** (-3)

    # acquisition time (gives minimum buffer size) =82e-6
    l.tac = float(value_sequenz['Readout']['acquisition_time']) * 10 ** (-6)

    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    value = value_sequenz['Readout']['gate_signal'].split(" ")
    l.t3d = [int(i)for i in value]   # [1, 0, 50, 10]

    # pulse durations
    # pulse frequency

    l.pfr = [if_frq for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    # pulse  duration

    # puls = value_sequenz['Puls']['puls_duration']
    # puls = puls.replace("[", "").replace("]", "")
    # puls = puls.split(",")
    # puls = [float(i) for i in puls]

    puls = string2array(value_sequenz['Puls']['puls_duration'])

    l.pdr = puls  # [3e-6]

    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    amplitude = [float(value_sequenz['Puls']['puls_amplitude'])for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    l.pam = amplitude  # [1]

    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)

    # offset = value_sequenz['Puls']['puls_arangement']
    # offset = offset.replace("[", "").replace("]", "")
    # offset = offset.split(",")
    # offset = [float(i) for i in offset]
    offset = string2array(value_sequenz['Puls']['puls_arangement'])

    # correction for data input
    l.pof = [np.ceil((offset[0]) * l.sra),
             np.ceil((offset[1] + puls[0]) * l.sra)]

    # **************test******************
    # l.pfr = [if_frq, if_frq]
    # l.pdr = [3e-6, 6e-6]                   # pulse in mu sec
    # l.pam = [1, 1]                         # amplitude
    # l.pof = [300, np.ceil(60e-6*l.sra)]     # offset in sec
    # ********************************

    l.npu = len(l.pfr)                                  # number of pulses

    l.rgn = float(value_sequenz['SDR setting']['gain_rx'])  # 55.0    # RX gain
    l.tgn = float(value_sequenz['SDR setting']['gain_tx'])  # 40.0  # TX gain

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
    if (1 == external_hardware):

        # reads back the file which was recently saved
        l.readHDF()

        # evaluation range, defines: blanking time and window length
        evran = [float(value_sequenz['setting']['blank_time']),
                 float(value_sequenz['setting']['window_time'])]  # [22.5, 42.5]

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
        fac_p_to_uV = float(
            value_sequenz['SDR setting']['factor_point2volts'])  # 447651/1e6

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
    """composite pulse sequence with pulses that change their phase in time 

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = seq_comp (value_main, value_sequenz)
    """

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

    # number of averages
    l.nav = float(value_sequenz["setting"]["num_averages"])
    # number of repetitions
    l.nrp = float(value_sequenz['setting']['repetition_num'])
    # TX I DC correction
    l.tdi = float(value_sequenz['SDR setting']['correction_tx_i_dc'])
    # TX Q DC correction
    l.tdq = float(value_sequenz['SDR setting']['correction_tx_q_dc'])
    # TX I Gain correction
    l.tgi = float(value_sequenz['SDR setting']['correction_tx_i_gain'])
    # TX Q Gain correction
    l.tgq = float(value_sequenz['SDR setting']['correction_tx_q_gain'])
    # TX phase adjustment
    l.tpc = float(value_sequenz['SDR setting']['correction_tx_pahse'])
    # RX I Gain correction
    l.rgi = float(value_sequenz['SDR setting']['correction_rx_i_dc'])
    # RX Q Gain correction
    l.rgq = float(value_sequenz['SDR setting']['correction_rx_q_dc'])
    # RX I DC correction
    l.rdi = float(value_sequenz['SDR setting']['correction_rx_i_gain'])
    # RX Q DC correction
    l.rdq = float(value_sequenz['SDR setting']['correction_rx_q_gain'])
    # RX phase adjustment
    l.rpc = float(value_sequenz['SDR setting']['correction_rx_phase'])

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    # repetition time
    # l.trp = 5e-3
    l.trp = float(value_sequenz['Readout']['repetition_time'])*10**-3

    # acquisition time
    # l.tac = 82e-6
    l.tac = float(value_sequenz['Readout']['acquisition_time']) * 10**-6
    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    # l.t3d=[1, 0, 50, 10]
    value = value_sequenz['Readout']['gate_signal'].split(" ")
    l.t3d = [int(i)for i in value]

    # phase cycling definitions
    # number of phases (here we only need 4 phases, but the programm cycles now in steps of 45 degree and we always need those 45 degree steps)
    # l.pcn = [1, 4]
    l.pcn = value_sequenz['Phase']['phase_number'].split(" ")

    # l.pcl = [0,1]                                        # pcyc level (only needed if more then 1 pulse is used (and a relative / different phase is necessary), so only Spin Echo needs/ uses it)
    # l.pph = [0, np.pi/4]
    l.pph = value_sequenz['Phase']['phase_puls'].split(" ")

    # l.pba = 1

    # pulse frequency
    l.pfr = [if_frq for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]

    # pulse  duration
    puls = string2array(value_sequenz['Puls']['puls_duration'])
    l.pdr = puls  # [3e-6]

    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    amplitude = [float(value_sequenz['Puls']['puls_amplitude'])for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    l.pam = amplitude  # [1]

    # pulse arrangement 1 means immediate start of the pulse
    offset = string2array(value_sequenz['Puls']['puls_arangement'])
    # correction for data input only for 2 pulses
    print("offset ", offset)
    print("puls ", puls)
    # dont run faster than the allowed :P
    l.pof = [np.ceil((offset[0]) * l.sra),
             np.ceil((offset[1] + puls[0]) * l.sra)]

    # **************test******************
    # l.pfr = [if_frq, if_frq]
    # l.pdr = [3e-6, 6e-6]                   # pulse in mu sec
    # l.pam = [1, 1]                         # amplitude
    # l.pof = [300, np.ceil(60e-6*l.sra)]     # offset in sec
    print("\n \n testing")
    print("puls l.pdr", l.pdr)
    print("offset l.pof", l.pof)
    print("\n \n testing")
    # ********************************

    l.npu = len(l.pfr)                              # number of pulses
    l.rgn = float(value_sequenz['SDR setting']['gain_rx'])  # 55.0    # RX gain
    l.tgn = float(value_sequenz['SDR setting']['gain_tx'])  # 40.0  # TX gain
    # l.tgn = 30 # for noise measurements

    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    l.rlp = 3.0e6                                          # RX Base-Band BW
    l.tlp = 130.0e6                                         # TX Base-Band BW

    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)

    # offset = value_sequenz['Puls']['puls_arangement']
    # offset = offset.replace("[", "").replace("]", "")
    # offset = offset.split(",")
    # offset = [float(i) for i in offset]
    offset = string2array(value_sequenz['Puls']['puls_arangement'])

    # correction for data input
    l.pof = [np.ceil((offset[0]) * l.sra),
             np.ceil((offset[1] + puls[0]) * l.sra)]

    # **************test******************
    # l.pfr = [if_frq, if_frq]
    # l.pdr = [3e-6, 6e-6]                   # pulse in mu sec
    # l.pam = [1, 1]                         # amplitude
    # l.pof = [300, np.ceil(60e-6*l.sra)]     # offset in sec
    # ********************************

    l.spt = './pulse/FID'                                  # directory to save to
    l.fpa = 'setup'

    l.run()

    if (1 == external_hardware):

        l.readHDF()

        evran = [float(value_sequenz['setting']['blank_time']),
                 float(value_sequenz['setting']['window_time'])]  # [27.5, 47.5]

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
        # print("tdy_time", tdy_time[:10])
        # [[ 1.84069325+5.41949576j] [-0.09787128+5.64195399j][-0.23770217+4.23728919j] ...]

        tdy_time = [[np.complex128(i)]for i in tdy_time]

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
        # plt.xlabel("t in µs")
        # plt.ylabel("Amplitude in µV")
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

        y_freq = [[np.complex128(i)]for i in y_freq]

        print("std rms frequency domain next to peak X: " +
              str(np.std(y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)))

        # plt.figure(2);
        # plt.plot(x, y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)
        # plt.xlabel("f in MHz")
        # plt.ylabel("Amplitude in µV")
        # plt.title("composite")
        # plt.show()

        return tdx, tdy_time, x, y_freq
    else:
        raise Exception(" hardware is missing")


def seq_spin_phase(value_main, value_sequenz):
    """spin-echo with phase-cycling  sequence

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = seq_spin_phase(value_main, value_sequenz)
    """

    # l = limr.limr('./pulseN_test_USB.cpp')
    l = limr.limr('./program/pulseN_test_USB.cpp')

    def phase_shift(iptsignal, angle):
        # Resolve the signal's fourier spectrum
        spec = fft(iptsignal)
        # freq = rfftfreq(iptsignal.size, d=dt)

        # Perform phase shift in freqeuency domain
        # default it was +1.0j
        spec *= np.exp(-1.0j * np.deg2rad(angle))

        # Inverse FFT back to time domain
        phaseshift = ifft(spec, n=len(iptsignal))
        return phaseshift

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
    l.nav = float(value_sequenz["setting"]["num_averages"])
    # number of repetitions

    l.nrp = float(value_sequenz['setting']['repetition_num'])
    # TX I DC correction
    l.tdi = float(value_sequenz['SDR setting']['correction_tx_i_dc'])
    # TX Q DC correction
    l.tdq = float(value_sequenz['SDR setting']['correction_tx_q_dc'])
    # TX I Gain correction
    l.tgi = float(value_sequenz['SDR setting']['correction_tx_i_gain'])
    # TX Q Gain correction
    l.tgq = float(value_sequenz['SDR setting']['correction_tx_q_gain'])
    # TX phase adjustment
    l.tpc = float(value_sequenz['SDR setting']['correction_tx_pahse'])
    # RX I Gain correction
    l.rgi = float(value_sequenz['SDR setting']['correction_rx_i_dc'])
    # RX Q Gain correction
    l.rgq = float(value_sequenz['SDR setting']['correction_rx_q_dc'])
    # RX I DC correction
    l.rdi = float(value_sequenz['SDR setting']['correction_rx_i_gain'])
    # RX Q DC correction
    l.rdq = float(value_sequenz['SDR setting']['correction_rx_q_gain'])
    # RX phase adjustment
    l.rpc = float(value_sequenz['SDR setting']['correction_rx_phase'])

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    # repetition time = 5e-3
    l.trp = float(value_sequenz['Readout']['repetition_time']) * 10 ** (-3)

    # acquisition time (gives minimum buffer size) =82e-6
    l.tac = float(value_sequenz['Readout']['acquisition_time']) * 10 ** (-6)

    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    value = value_sequenz['Readout']['gate_signal'].split(" ")
    l.t3d = [int(i)for i in value]   # [1, 0, 50, 10]

    # pulse durations
    # pulse frequency
    # l.pfr = [if_frq]
    l.pfr = [if_frq for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    puls = string2array(value_sequenz['Puls']['puls_duration'])
    # pulse  duration
    l.pdr = puls  # [3e-6]
    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)

    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    amplitude = [float(value_sequenz['Puls']['puls_amplitude'])for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    l.pam = amplitude  # [1]

    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)

    # offset = value_sequenz['Puls']['puls_arangement']
    # offset = offset.replace("[", "").replace("]", "")
    # offset = offset.split(",")
    # offset = [float(i) for i in offset]
    offset = string2array(value_sequenz['Puls']['puls_arangement'])

    # correction for data input
    l.pof = [np.ceil((offset[0]) * l.sra),
             np.ceil((offset[1] + puls[0]) * l.sra)]

    l.npu = len(l.pfr)                                  # number of pulses

    # phase cycling definitions
    # number of phases (here we only need 4 phases, but the programm cycles now in steps of 45 degree and we always need those 45 degree steps)
    # l.pcn = [1, 4]
    #l.pcn = value_sequenz['Phase']['phase_number'].split(" ")

    # l.pcl = [0,1]                                        # pcyc level (only needed if more then 1 pulse is used (and a relative / different phase is necessary), so only Spin Echo needs/ uses it)
    # l.pph = [0, np.pi/4]
    #l.pph = value_sequenz['Phase']['phase_puls'].split(" ")

    # test
    l.pcn = [4, 1]                                      # number of phases
    l.pph = [0, np.pi/2]  # pulse phase (added to phase shift due to pcn)
    # test

    print("-----------------------------------------------------------------------------------------------------------------------------------------------")
    print("\n \n puls l.pof ", l.pof)
    print("offset l.pdr  ", l.pdr)

    # RX gain between 5 and 55 (usually 40 was used, 55 better and maximum)
    l.rgn = float(value_sequenz['SDR setting']['gain_rx'])  # 55.0    # RX gain
    l.tgn = float(value_sequenz['SDR setting']['gain_tx'])  # 40.0  # TX gain

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
    if (1 == external_hardware):

        l.readHDF()

        # select range which should be investigated (ECHO time setting)
        evran = [float(value_sequenz['setting']['blank_time']),
                 float(value_sequenz['setting']['window_time'])]

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

        print(type(k1), "k1", k1[:5])
        print("k2", k2[:5])
        print("k3", k3[:5])
        print("k4", k4[:5])

        tdy_mean_self = (k1+k2+k3+k4)
        tdy_time = tdy_mean_self/l.nav/447651*1e6/RX_gainfactor/4
        tdy_time = tdy_mean_self

        # #plot resulting time domain data and scale it to uV
        # plt.figure(1);
        # plt.plot(tdx, tdy_time)
        # plt.xlabel("t in µs")
        # plt.ylabel("Amplitude in µV")
        # plt.show()

        fdy1 = fftshift(fft(tdy_mean_self, axis=0), axes=0)

        fdx1 = fftfreq(len(fdy1))*l.sra/1e6
        #fdx1 = fftshift(fdx1)

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
        tdy_time = [[np.complex128(i)]for i in tdy_time]

        return tdx, tdy_time, x, y
    else:
        raise Exception(" hardware is missing")


def seq_own(value_main, value_sequenz):
    """own sequence can be used to desine a arbitrary sequence used with up to 10 pulses und all its dependet phases

    :param value_main: all parameterst from the main window 
    :type value_main: dict
    :param value_sequenz: all parameters dependent on the sequence
    :type value_sequenz: dict
    :raises Exception: Exception: if not possible to send to the hardware
    :return: steps time domain, amplitude time domain,steps frequency domain, amplitude frequency domain
    :rtype: [list, list, list, list]


    :Example:
    >>> [x_time, y_time, x_freq, y_freq] = seq_own(value_main, value_sequenz)
    """

    l = limr.limr('./program/pulseN_test_USB.cpp')
    l.noi = -1

    # target frequency of the experiment
    tgtfreq = 83.62e6

    # IF or base band frequency
    if_frq = 1.2e6

    # LO frequency (target7 frequency - base band frequency)
    l.lof = tgtfreq-if_frq
    # Sampling Rate
    l.sra = 30.72e6
    # number of averages
    l.nav = float(value_sequenz["setting"]["num_averages"])
    # number of repetitions

    l.nrp = float(value_sequenz['setting']['repetition_num'])
    # TX I DC correction
    l.tdi = float(value_sequenz['SDR setting']['correction_tx_i_dc'])
    # TX Q DC correction
    l.tdq = float(value_sequenz['SDR setting']['correction_tx_q_dc'])
    # TX I Gain correction
    l.tgi = float(value_sequenz['SDR setting']['correction_tx_i_gain'])
    # TX Q Gain correction
    l.tgq = float(value_sequenz['SDR setting']['correction_tx_q_gain'])
    # TX phase adjustment
    l.tpc = float(value_sequenz['SDR setting']['correction_tx_pahse'])
    # RX I Gain correction
    l.rgi = float(value_sequenz['SDR setting']['correction_rx_i_dc'])
    # RX Q Gain correction
    l.rgq = float(value_sequenz['SDR setting']['correction_rx_q_dc'])
    # RX I DC correction
    l.rdi = float(value_sequenz['SDR setting']['correction_rx_i_gain'])
    # RX Q DC correction
    l.rdq = float(value_sequenz['SDR setting']['correction_rx_q_gain'])
    # RX phase adjustment
    l.rpc = float(value_sequenz['SDR setting']['correction_rx_phase'])

    # repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    # be adjusted in the ways that it fits to an integer multiply of the buffer size

    # repetition time = 5e-3
    l.trp = float(value_sequenz['Readout']['repetition_time']) * 10 ** (-3)

    # acquisition time (gives minimum buffer size) =82e-6
    l.tac = float(value_sequenz['Readout']['acquisition_time']) * 10 ** (-6)

    # GPIO Pin3 is centered around the pulse (used as a Gate Signal)
    value = value_sequenz['Readout']['gate_signal'].split(" ")
    l.t3d = [int(i)for i in value]   # [1, 0, 50, 10]

    # pulse durations
    # pulse frequency

    l.pfr = [if_frq for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    # pulse  duration

    # puls = value_sequenz['Puls']['puls_duration']
    # puls = puls.replace("[", "").replace("]", "")
    # puls = puls.split(",")
    # puls = [float(i) for i in puls]

    puls = string2array(value_sequenz['Puls']['puls_duration'])
    l.pdr = puls  # [3e-6]

    # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
    amplitude = [float(value_sequenz['Puls']['puls_amplitude'])for i in range(
        0, int(value_sequenz['Puls']['number_pulses']))]
    l.pam = amplitude  # [1]

    # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)

    # offset = value_sequenz['Puls']['puls_arangement']
    # offset = offset.replace("[", "").replace("]", "")
    # offset = offset.split(",")
    # offset = [float(i) for i in offset]
    offset = string2array(value_sequenz['Puls']['puls_arangement'])

    # correction for data input
    print("offset", offset)
    print("puls", puls)
    #l.pof = [offset[0], np.ceil((offset[1] + puls[0]) * l.sra)]

    puls = [float(0)] + puls  # shift pulses to align with offset
    offset_shift = []
    for i, val in enumerate(offset):
        #print(i, "offset:", type(offset[i]), " pulse:", type(puls[i]))
        #print(i, "offset:", (offset[i]), " pulse:", (puls[i]))
        offset_sum = puls[i] + offset[i]
        offset_sum = offset_sum * l.sra
        offset_sum = np.ceil(offset_sum)
        #print("offset_sum", offset_sum)
        offset_shift.append(offset_sum)
    # first offest parameter defalt set, hardware requirement
    offset_shift[0] = 300

    # offset = [np.ceil(float(offset[i] + puls[i]) * l.sra)
    #          for i, val in enumerate(offset)]

    l.pof = offset_shift
    print("l.pof ", l.pof)
    # **************test******************
    #l.pfr = [if_frq, if_frq]
    # l.pdr = [3e-6, 6e-6]                   # pulse in mu sec
    # l.pam = [1, 1]                         # amplitude
    # l.pof = [300, np.ceil(30e-6*l.sra)]    # offset in sec
    # ********************************

    l.npu = len(l.pfr)                         # number of pulses

    l.rgn = float(value_sequenz['SDR setting']['gain_rx'])  # 55.0    # RX gain
    l.tgn = float(value_sequenz['SDR setting']['gain_tx'])  # 40.0  # TX gain

    RX_gainfactor = 1

    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    # RX BW (IF or base band low pass filter)
    l.rlp = 3.0e6
    l.tlp = 130.0e6                                     # RX BW

    l.spt = save_dh5_file                            # directory to save to
    l.fpa = 'setup'

    print("\n ________\n", "start sequenz", "\n ________\n")
    l.run()

    # retun values
    x_time = np.array([22.0, 22.1, 22.2, 22.3, 22.4,
                      22.5, 22.6, 22.7, 22.8, 22.9])
    y_time = [0.2+9.70j, -1.5+3.0j, -2.0 + 5.31j, -0.1+3.0j, -0.1 -
              0.4j, 0.4-2.3j, 1.3-3.3j, -0.5-4.1j, -1.7-6.4j, -1.9-7.0j]
    y_time = [0.3+i + 1.50j for i in range(10)]
    y_time = [[np.complex128(i)]for i in y_time]
    # y_time <class 'numpy.complex128'> [0.19533675+9.700897j]

    x_freq = np.array([83.0, 83.1, 83.2, 83.3, 83.4, 83.5, 83.6, 83.7, 83.8])
    y_freq = [0.1, 0.2, 0.3, 0.5, 1.9, 0.5, 0.3, 0.2, 0.1]
    y_freq = np.array([[np.array(i)]for i in y_freq])

    return x_time, y_time, x_freq, y_freq


def send_tune_match(tune, match, tm_step, tm_lut):
    """provisions for development of a new tuning and matching system

    :param tune: max voltage range of tunig capacitor
    :type tune: float
    :param match: max voltage range of matching capacitor
    :type match: float
    :param tm_step: step size of measured data
    :type tm_step: int
    :param tm_lut: resolution of saved measured data
    :type tm_lut: int
    """

    print("start tune and match sequenz on Arduino ")
    print("tune ", tune)
    print("match ", match)
    print("tm_step ", tm_step)
    print("tm_lut ", tm_lut)
