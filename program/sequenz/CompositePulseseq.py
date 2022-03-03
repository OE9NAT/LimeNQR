#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 09:55:05 2021

@author: luki
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift, fftfreq
import limr


l = limr.limr('./pulseN_test_USB.cpp');

l.noi = -1

#target frequency of the experiment
tgtfreq = 83.62e6

#IF or base band frequency
if_frq = 1.2e6

l.lof = tgtfreq-if_frq                              # LO frequency (target frequency - base band frequency)
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



#repetition and acquisition time (acquisition time can only be an integer multiple of the buffer size from Cpp, so the number here will automatically
#be adjusted in the ways that it fits to an integer multiply of the buffer size

l.trp = 5e-3                                        # repetition time
l.tac = 82e-6                                       # acquisition time
l.t3d = [1, 0, 50, 10]                             # GPIO Pin3 is centered around the pulse (used as a Gate Signal)


# phase cycling definitions
l.pcn = [1,4]                                       # number of phases (here we only need 4 phases, but the programm cycles now in steps of 45 degree and we always need those 45 degree steps)
#l.pcl = [0,1]                                        # pcyc level (only needed if more then 1 pulse is used (and a relative / different phase is necessary), so only Spin Echo needs/ uses it)
l.pph = [0, np.pi/4]
#l.pba = 1

# pulse durations
l.pfr = [if_frq, if_frq]                            # pulse frequency
l.pdr = [3e-6, 6e-6]                                # pulse  duration

l.pam = [1, 1]                                      # relative pulse amplitude
l.pof = [300, np.ceil(3e-6*l.sra)]                    # pulse arrangement 1 means immediate start of the pulse
   
#l.pph = [0, np.pi/2]

l.npu = len(l.pfr)                              # number of pulses

l.rgn = 55.0                                            # RX gain
l.tgn = 40.0                                            # TX gain
#l.tgn = 30 # for noise measurements

RX_gainfactor = 1
    
if l.rgn == 40:
    RX_gainfactor = 1
else:
    RX_gainfactor = 10**((l.rgn-40)/20)


l.rlp = 3.0e6                                          # RX Base-Band BW
l.tlp = 130.0e6                                         # TX Base-Band BW

l.spt =  './pulse/FID'                                  # directory to save to
l.fpa = 'setup'

l.run()

####################################################################################################### read back file and plot time signal + shifted fft 
if (1 == 1):

    l.readHDF()
    
    evran = [27.5, 47.5] 
    
    evidx = np.where( (l.HDF.tdx > evran[0]) & (l.HDF.tdx < evran[1]) )[0]

    print(type(evran[0]))
    
    tdx = l.HDF.tdx[evidx]
    tdy = l.HDF.tdy[evidx]    
    

    tdy_mean_self=tdy
    tdy_mean = tdy-np.mean(tdy)
    
    
    tdy_mean_0_45 = tdy_mean[:,0]
    tdy_mean_0_135 = tdy_mean[:,1]
    tdy_mean_0_m135 = tdy_mean[:,2]
    tdy_mean_0_m45 = tdy_mean[:,3]
    
    tdy_comp = (-tdy_mean_0_45 + tdy_mean_0_135 - tdy_mean_0_m135 + tdy_mean_0_m45)


    fdy1 = fftshift(fft(tdy_mean,axis=0),axes=0)

    fdy2 = fftshift(fft(tdy,axis=0),axes=0)
    
    fdy_comp = fftshift(fft(tdy_comp,axis=0),axes=0)

    #print(len(fdy1))

    fdx1 = fftfreq(len(fdy1))*30.72
    fdx1 = fftshift(fdx1)

    fdx_comp = fftfreq(len(fdy_comp))*30.72
    fdx_comp = fftshift(fdx_comp)

    #get rid of dc offset
    nums = np.shape(fdy1)[1]

    plt.figure(1);
    plt.plot(tdx,tdy_comp/l.nav/447651*1e6) 
    plt.xlabel("t in µs")
    plt.ylabel("Amplitude in µV")
    plt.show()
    

    lof=l.HDF.attr_by_key('lof')

    for i in range(0, len(fdx1)):
        fdx1[i] = fdx1[i]+lof[0]/1e6
        #print(fdx1[i])

    
    # fft of composite pulsed sequence
    shifter = 12#0#50
    stopper = 270#300
    
    y=abs((fdy_comp[int(len(fdy_comp)/2)+shifter:len(fdy_comp)-1-stopper]))
    x=fdx1[int(len(fdy_comp)/2)+shifter:len(fdy_comp)-1-stopper]
    
    print("std rms frequency domain next to peak X: " + str(np.std(y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)))

    plt.figure(2);
    plt.plot(x, y/l.nav/len(tdx)/447651*1e6/RX_gainfactor)
    plt.xlabel("f in MHz")
    plt.ylabel("Amplitude in µV")
    plt.title("composite")
    plt.show() 
 