#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 08:06:56 2021

@author: luki
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq
import limr
import os.path
import sys


l = limr.limr('../pulseN_USB.cpp');



#target frequency of the experiment
#tgtfreq = float(sys.argv[1])
#tgtfreq = 83.5e6





def seq(tgtfreq, filename, averages, sampleRate):
    #IF or base band frequency
    if_frq = 3e6
    ################################################################################################### SET UP SDR AND PULSE PARAMETERS, LOF and IF ...
    l.lof = tgtfreq-if_frq                                   # LO frequency
    l.sra = sampleRate                                         # Sampling Rate
    l.nav = averages                                         # number of averages
    l.nrp = 1                                               # number of repetitions
    
    #repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size)
    l.trp = 1e-3#0.5e-3#1e-3                                            # repetition time
    l.tac = 82e-6                                           # acquisition time
    l.t3d = [1, 10, 53, 10]                                 # GPIO Pin3 is centered around the pulse
    
    
    
    l.tdi = -32                                         # TX I DC correction
    l.tdq = 50                                          # TX Q DC correction
    l.tgi = 2047                                        # TX I Gain correction       
    l.tgq = 2041                                        # TX Q Gain correction 
    l.tpc = 1                                           # TX phase adjustment
    
    # phase cycling definitions
    #l.pcn = [4]                              # number of phases
    #l.pcl = [1]                                            # pcyc level (only needed if more then 1 pulse is used, so only Spin Echo needs/ uses it)
    
    #l.pba = 1
    
    # pulse durations
    #l.pfr = [if_frq, if_frq]                                        # pulse frequency
    #l.pdr = [30e-6, 30e-6]                                          # pulse  duration
    #l.pam = [0.9, 0.9]                                           # relative pulse amplitude
    #l.pof = [300, np.ceil(50e-6*l.sra)]                                     # pulse arrangement 1 means immediate start of the pulse
       
    l.pfr = [if_frq]
    l.pdr = [16e-6]
    l.pam = [1]        
    l.pof = [300]
             
             
    l.npu = len(l.pfr)                              # number of pulses
    
    l.rgn = 55.0                                            # RX gain
    l.tgn = 50.0                                            # TX gain
    
    
    l.rlp = 8.0e6                                          # RX BW
    l.tlp = 130.0e6                                         # RX BW
    
    l.spt =  './pulse/FID'                                  # directory to save to
    l.fpa = 'setup'
    
    l.run()
    
    #read back file and plot time signal + shifted fft 
    if (1 == 1):
    
        #reads back the file which was recently saved
        l.readHDF()
    
        #evaluation range, defines: blanking time and window length
        evran = [36.5, 56.5]
         
        #np.where sometimes does not work out, so it is put in a try except
        #always check the console for errors
        try:
            evidx = np.where( (l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]) )[0]
        except:
            print("error due to np.where evaluation!")
        
        #time domain x and y data    
        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]
    
        #correcting a offset in the time domain by subtracting the mean
        tdy_mean = tdy-np.mean(tdy)
    
        #fft of the corrected time domain data
        fdy1 = fftshift(fft(tdy_mean,axis=0),axes=0)
    
        #fft freq and fft shift is here used to scale the x axis (frequency axis)
        fdx1 = fftfreq(len(fdy1))*l.sra/1e6
        fdx1 = fftshift(fdx1)
    
        #scaling factor which converts the y axis (usually a proportional number of points) into uV
        fac_p_to_uV = 447651/1e6
        
        tdy_mean = tdy_mean/l.nav/fac_p_to_uV
        
        """
        plt.figure(1);
        plt.plot(tdx,tdy_mean)
        plt.xlabel("t in µs")
        plt.ylabel("Amplitude in µV")
        plt.show()
        """
        
        #get LO frequency and add it to the base band fft x-Axis in order to illustrate the applied frequency
        #for single side spectrum and shift (only single frequency)
        lof=l.HDF.attr_by_key('lof')
    
        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6
    
    
        #shifter takes the whole fft and shifts it away from zero point (zer0 if offset = 0 or low)
        #window of interest
        shifter = 50#0#50
        stopper = 0#300
        
        #here the right side of the spectrum is selected
        y=abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]))/len(tdx)/fac_p_to_uV/l.nav
        x=fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]
    
        """
        plt.figure(5);
        plt.plot(x, y)
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        plt.show() 
        """
        #print("len x: " +str(len(x)))
        
        
        #search for the excitation field // has to be choosen which one is the right version
        #excitation_indeces = np.where((x > ((tgtfreq-1/l.pdr[0])/1e6)) & (x <= ((tgtfreq+1/l.pdr[0])/1e6)))
        
        #same as above, only applied with the frequency steps given due to the TM routine
        freq_step = 0.1e6
        excitation_indeces = np.where((x > tgtfreq/1e6) & (x <= ((tgtfreq+freq_step)/1e6)))
        
        #print("peak index range: " + str(1/l.pdr[0]))
        
        """
        plt.figure(10);
        plt.plot(x[excitation_indeces], y[excitation_indeces])
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        plt.show() 
        """
        x_exc = x[excitation_indeces]
        
        y_exc = np.asarray(y[excitation_indeces])
        
        
        #headfile works fine with appending rest, but only needs to be done once
        
    
        
        #filename = 'scan-data.csv'
        
        if(os.path.isfile(filename) == 0):
            print("Filename not given yet - new file will be generated!")
            f = open(filename, 'w')
            f.write('frequency\tamplitude\n')
            f.close()
        else:
            print("File does already exist, scan data will be appended!")
        
        
        for i in range(0, len(x_exc)):
            f = open(filename, 'a')
            f.write(str(x_exc[i])+'\t'+str(y_exc[i,0])+'\n')
            f.close()
        
        
        """
        #here the whole spectrum (double sided) is plotted
        y=abs((fdy1))/len(tdx)/fac_p_to_uV/l.nav
        x=fdx1
        
        
        plt.figure(3);
        plt.plot(x, y)
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        plt.show()
        
        #print("len x: " +str(len(tdx)))
        """
  
    
"""   
def main():
    seq(111.5e6, 'scan5X.csv', 1000, 30.72e6)

if __name__ == "__main__":
    main()    
"""