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


U_Tune_max = 5.0 #max voltage for tuning cap
U_Match_max = 5.0 # max voltage for matching cap


vec=list()
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

#open Tune-Match file and load the voltages and frequencies into seperate arrays
with open(TMfile) as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    data = [(float(col1), float(col2), float(col3))
                for col1, col2, col3 in reader]
    
np_data=np.asarray(data)    

print(np.shape(np_data))

for freq in range(0, np.shape(np_data)[0]):
    freqList.append(np_data[freq][0])
freqList=np.asarray(freqList)
    
for utval in range(0, np.shape(np_data)[0]):
    ut.append(np_data[utval][1])
ut=np.asarray(ut)    

for umval in range(0, np.shape(np_data)[0]):
    um.append(np_data[umval][2])
um=np.asarray(um) 

#calculate the frequency step by the difference of two frequencies in the Tune-Match file
freqStep = (freqList[1]-freqList[0])


for i in range(0, len(um)):
    #set voltages for certain frequency
    start_flag = 'Set_Voltage\n'
    arduino.write(start_flag.encode())
    UT = int(ut[i]*4095/U_Tune_max)
    UM = int(um[i]*4095/U_Match_max)
    
    UT = str(UT)
    UM = str(UM)

    #send the voltages to the Arduino
    if (arduino.readline().decode() == 'ready\n'):
        arduino.write(UT.encode() + b'\n')
        arduino.write(b'stop\n')
        
        arduino.write(UM.encode() + b'\n')
        arduino.write(b'stop\n')
        
    
        if (arduino.readline().decode() == 'done\n'):
            print('\nSuccessfully sent: \n' )
            print('Tune-voltage: ' + arduino.readline().decode())
            print('Match-voltage: ' + arduino.readline().decode())              
        else:
            print('Error by sending data to Arduino')

    #print the current frequency which will be applied
    print("\n")
    print("Current Excitation Frequency: " + str(freqList[i]/1e6) + " MHz")
    print("\n")
    #call the FID sequence to carry out the experiment at the frequency step
    FIDcut.seq(freqList[i], filename, averages, sampleRate, freqStep)
#close arduino connection    
arduino.close()

#call the method to plot the resulting spectrum of the whole scan
scanloader.loadPlot(filename)




