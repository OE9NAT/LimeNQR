#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 13:45:35 2021

@author: luki
"""

import serial
import time
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq
import csv
from subprocess import call, Popen
import numpy as np
import itertools
# _import FIDcut
import limr
#import os.path
#import sys


U_Tune_max = 5.0  # max voltage for tuning cap
U_Match_max = 5.0  # max voltage for matching cap


vec = list()
ref = list()
ut = list()
um = list()
ref_list = list()
freqList = list()


start_flag = 'Set_Voltage\n'
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
time.sleep(1)

arduino.write(start_flag.encode())

U_Tune_max = 5
U_Match_max = 5


filename = 'scantry2.csv'
TMfile = 'TM83_84.csv'
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
freqStep = (freqList[1]-freqList[0])


l = limr.limr('./pulseN_test_USB.cpp')


def seq(tgtfreq, filename, averages, sampleRate, freq_step):
    # IF or base band frequency
    if_frq = 1.2e6

    l.lof = tgtfreq-if_frq                                  # LO frequency
    l.sra = sampleRate                                      # Sampling Rate
    l.nav = averages                                        # number of averages
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

    l.npu = len(l.pfr)                                      # number of pulses

    l.rgn = 55.0                                            # RX gain
    l.tgn = 50.0                                            # TX gain

    l.rlp = 3.0e6                                           # RX BW
    l.tlp = 130.0e6                                         # RX BW

    l.spt = './pulse/FID'                                  # directory to save to
    l.fpa = 'setup'

    l.run()

    # read back file and plot time signal + shifted fft
    if (1 == 1):

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
    seq(freqList[i], filename, averages, sampleRate, freqStep)
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
plt.show()

print("STD: " + str(np.std(np_data[:, 1])))
