#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 09:37:39 2021

@author: luki
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq
import limr

l = limr.limr('./pulseN_test_USB.cpp');

l.noi = -1                                          #hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)

#target frequency of the experiment
tgtfreq = 83.62e6

#IF or base band frequency
if_frq = 1.2e6

l.lof = tgtfreq-if_frq                              # LO frequency (target7 frequency - base band frequency)
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

#repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
#be adjusted in the ways that it fits to an integer multiply of the buffer size
l.trp = 5e-3                                        # repetition time
l.tac = 82e-6                                       # acquisition time (gives minimum buffer size)
l.t3d = [1, 0, 50, 10]                              # GPIO Pin3 is centered around the pulse (used as a Gate Signal)

# pulse durations
l.pfr = [if_frq]                                    # pulse frequency
l.pdr = [3e-6]                                      # pulse  duration
l.pam = [1]                                         # relative pulse amplitude (only makes sense if 2 or more pulses are in the sequence)
l.pof = [300]                                       # pulse arrangement 1 means immediate start of the pulse (3us from zero approx. is then start of the first pulse)
  

l.npu = len(l.pfr)                                  # number of pulses

l.rgn = 55.0                                        # RX gain
l.tgn = 40.0                                        # TX gain

RX_gainfactor = 1
    
if l.rgn == 40:
    RX_gainfactor = 1
else:
    RX_gainfactor = 10**((l.rgn-40)/20)

l.rlp = 3.0e6                                       # RX BW (IF or base band low pass filter)
l.tlp = 130.0e6                                     # RX BW

l.spt =  './pulse/FID'                              # directory to save to
l.fpa = 'setup'


l.run()

#read back file and plot time signal + shifted fft 
if (1 == 1):

    #reads back the file which was recently saved
    l.readHDF()

    #evaluation range, defines: blanking time and window length
    evran = [22.5, 42.5]
     
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
    fdx1 = fftfreq(len(fdy1))*30.72
    fdx1 = fftshift(fdx1)

    #scaling factor which converts the y axis (usually a proportional number of points) into uV
    fac_p_to_uV = 447651/1e6
    
    tdy_mean = tdy_mean/l.nav/fac_p_to_uV/RX_gainfactor
    
    plt.figure(1);
    plt.plot(tdx,tdy_mean)
    plt.xlabel("t in µs")
    plt.ylabel("Amplitude in µV")
    plt.show()
    
    
    #get LO frequency and add it to the base band fft x-Axis in order to illustrate the applied frequency
    #for single side spectrum and shift (only single frequency)
    lof=l.HDF.attr_by_key('lof')

    for i in range(0, len(fdx1)):
        fdx1[i] = fdx1[i]+lof[0]/1e6


    #cutting out the window of the interessting part of the computed fft spectrum (here from 83 - 84 MHz)
    #window of interest
    shifter = 12#0#50
    stopper = 270#300
    #here the right side of the spectrum is selected
    y=abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]))/len(tdx)/fac_p_to_uV/l.nav/RX_gainfactor
    x=fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]
    
    plt.figure(5);
    plt.plot(x, y)
    plt.xlabel("f in MHz")
    plt.ylabel("Amplitude in µV")
    plt.show() 
    
    
    #print std (for SNR determination -> noise analysis without sample)
    print("std rms frequency domain next to peak X: " + str(np.std(y)))
    #print max of fft (for SNR evaluation - should give peak maximum)
    print("MAX of Signal: " + str(max(y)))
