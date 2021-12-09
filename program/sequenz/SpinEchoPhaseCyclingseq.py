#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 09:43:48 2021

@author: luki
"""

import numpy as np
from numpy.fft import rfft, irfft, rfftfreq
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq, ifft, ifftshift
import limr

from scipy.signal import hilbert

def phase_shift(iptsignal, angle):

    # Resolve the signal's fourier spectrum
    spec = fft(iptsignal)
    #freq = rfftfreq(iptsignal.size, d=dt)

    # Perform phase shift in freqeuency domain
    #default it was +1.0j
    spec *= np.exp(-1.0j * np.deg2rad(angle))

    # Inverse FFT back to time domain
    phaseshift = ifft(spec, n=len(iptsignal))
    return phaseshift


if __name__ == '__main__':
    
    l = limr.limr('./pulseN_test_USB.cpp');
    
    l.noi = -1                                          #hardcoded initialization of the lime. needed if parameters (e.g. Gain, tgi, tdi, are changed and need to be set to chip)
    
    #target frequency of the experiment
    tgtfreq = 83.62e6
    
    #IF or base band frequency
    if_frq = 1.2e6
    
    l.lof = tgtfreq-if_frq                              # LO frequency (target7 frequency - base band frequency)
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
    
    #repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
    #be adjusted in the ways that it fits to an integer multiply of the buffer size
    l.trp = 5e-3                                        # repetition time
    l.tac = 82e-6                                       # acquisition time (gives minimum buffer size)
    l.t3d = [1, 0, 50, 10]                              # GPIO Pin3 is centered around the pulse (used as a Gate Signal)


    l.pcn = [4, 1]                                      # number of phases
    l.pph = [0, np.pi/2]                                #pulse phase (added to phase shift due to pcn)


    
    # pulse durations
    l.pfr = [if_frq, if_frq]                            # pulse frequency
    l.pdr = [3e-6, 6e-6]                                # pulse  duration
    l.pam = [1, 1]                                      # relative pulse amplitude
    l.pof = [300, np.ceil(9e-6*l.sra)]			        # pulse arrangement (first one is triggered then second one after 15 us)

    
    l.npu = len(l.pfr)                                  # number of pulses
    
    l.rgn = 55.0                                        # RX gain between 5 and 55 (usually 40 was used, 55 better and maximum)
    l.tgn = 40.0                                        # TX gain
    
    
    #RX gain was set to 40 dB when the scaling facotr from points to V was determined - so a higher or lower values then 40 need correction for the plots
    RX_gainfactor = 1
    
    if l.rgn == 40:
        RX_gainfactor = 1
    else:
        RX_gainfactor = 10**((l.rgn-40)/20)

    l.rlp = 3.0e6                                        # RX BW
    l.tlp = 130.0e6                                      # RX BW
    
    l.spt =  './pulse/SCAN'                              # directory to save to
    l.fpa = 'setup'
                                        
    # call to program
    l.run()

    #read back and post-processing
    if (1 == 1):
    
        l.readHDF()

        #select range which should be investigated (ECHO time setting)
        evran = [35, 55]  
        
        evidx = np.where( (l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]) )[0]

            
        tdx = l.HDF.tdx[evidx]
        tdy = l.HDF.tdy[evidx]
        

        tdy_mean = tdy-np.mean(tdy)
        
        #take RX time domain data from hdf5 file
        tdy_mean_0_90 = tdy_mean[:,0]
        tdy_mean_90_90 = tdy_mean[:,1]
        tdy_mean_180_90 = tdy_mean[:,2]
        tdy_mean_270_90 = tdy_mean[:,3]
        

        #use function to shift RX phaseaccordingly to kazan (therefore k1, k2, k3, k4)    
        k1 = tdy_mean_0_90
        k2 = phase_shift(tdy_mean_90_90, 270)
        k3 = phase_shift(tdy_mean_180_90, 180)
        k4 = phase_shift(tdy_mean_270_90, 90)
        
    
        tdy_mean_self = (k1+k2+k3+k4)

        #plot resulting time domain data and scale it to uV
        plt.figure(1);
        plt.plot(tdx, tdy_mean_self/l.nav/447651*1e6/RX_gainfactor/4)
        plt.xlabel("t in µs")
        plt.ylabel("Amplitude in µV")
        plt.show()   
        

        fdy1 = fftshift(fft(tdy_mean_self,axis=0),axes=0)

        fdx1 = fftfreq(len(fdy1))*l.sra/1e6
        fdx1 = fftshift(fdx1)
        
        
        #for single side spectrum and shift (only single frequency)
        lof=l.HDF.attr_by_key('lof')
            
        for i in range(0, len(fdx1)):
            fdx1[i] = fdx1[i]+lof[0]/1e6
            
            
        shifter = 12
        stopper = 270
    
        #here the right side of the spectrum is selected
        y=abs((fdy1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]))//l.nav/len(tdx)/447651*1e6/4/RX_gainfactor
        x=fdx1[int(len(fdy1)/2)+shifter:len(fdy1)-1-stopper]
        print("std rms frequency domain next to peak X: " + str(np.std(y)))
        print("MAX of Signal: " + str(max(y)))
        
        
        plt.figure(2);
        plt.plot(x, y)
        plt.xlabel("f in MHz")
        plt.ylabel("Amplitude in µV")
        plt.title("double sided spectrum with phase cycling")
        plt.show()
        
  