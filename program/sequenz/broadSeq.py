#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 13:45:35 2021

@author: luki
"""

import serial
import time
import matplotlib.pyplot as plt
import csv
from subprocess import call, Popen
import numpy as np
import itertools
import FIDcut
import scanloader


LUT_size = 50  # usually 20 to 50 values
U_Tune_max = 5.0  # max voltage for tuning cap
U_Match_max = 5.0  # max voltage for matching cap
# freq_points = 11 # e.g. 10 MHz subdevided into 100 kHz steps

vec = list()
ref = list()
ut = list()
um = list()
ref_list = list()
freqList = list()


start_flag = 'Set_Voltage\n'
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
#arduino = serial.Serial(port='/dev/tty.usbmodem14201', baudrate=115200)
time.sleep(1)

arduino.write(start_flag.encode())

U_Tune_max = 5
U_Match_max = 5


filename = 'scanNEW-nosample.csv'
TMfile = 'TM-manual-dummy-nosample.csv'  # XTM_80-90-50-4.csv'
averages = 5000
sampleRate = 30.72e6


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


print(ut)
print(um)
print(freqList)


for i in range(0, len(um)):
    start_flag = 'Set_Voltage\n'
    arduino.write(start_flag.encode())
    UT = int(ut[i]*4095/U_Tune_max)
    UM = int(um[i]*4095/U_Match_max)

    UT = str(UT)
    UM = str(UM)

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
    # time.sleep(1)
    #call(['gnome-terminal', '-e', "python3 FIDcut.py "+str(freqList[i])])

    print("\n")
    print("Current Excitation Frequency: " + str(freqList[i]/1e6) + " MHz")
    print("\n")
    FIDcut.seq(freqList[i], filename, averages, sampleRate)
    # needed as the call is not terminated ; 3 is for 1000 ave 4 for 2000 15 for 10000
    # time.sleep(4)

arduino.close()

with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    data = [(float(col1), float(col2))
            for col1, col2, in reader]

np_data = np.asarray(data)
# print(np_data)

plt.figure(10)
plt.plot(np_data[:, 0], np_data[:, 1])
plt.xlabel("f in MHz")
plt.ylabel("Amplitude")
plt.show()

print("STD: " + str(np.std(np_data[:, 1])))
