# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:46:20 2018

@author: andrin

Class that eases interfacing with the limesdr routines written in Cpp, 
notably the pulse_test_USB and pulseN_test_USB routines, which runs a pulse sequence 
according to passed arguments

The class allows for setting of the arguments as well as for parametric sweeps to
implement arbitrary sequences

Note for release: The communication between the python and the Cpp routine is very rudimentary, meaning using command line arguments that are parametrically read from the Cpp source.
Update Feb 2020: Slight changes to make it compatible with Python 3

"""
import subprocess                # to call the program
import datetime                  # to generate timestamps for parsweeps
import h5py                      # to have organized data storage.....
import numpy as np               # ...
import matplotlib.pyplot as plt


class limr():
    
    def __init__(self, filename = './pulseN_USB.cpp'):
        
        # check first for the filename provided
        if filename[-3:] == 'cpp':
            self.Csrc = filename
        else:
            self.Csrc = './pulseN_USB.cpp'
            
        # the program to call
        self.Cprog = self.Csrc[:-4]
        
        fp = open(self.Csrc, 'r')

        in_arg = {}
        startpattern = 'struct Config2HDFattr_t HDFattr[]'
        stoppattern = '};'
        parsing = False
        ii_oupargs = 0
        for line in fp.readlines():
            if (stoppattern in line) & parsing:
                break
            if parsing:
                stripped = line.replace('\t','').replace('"','').strip('\n').strip(',').strip('{').strip('}')
                splitted = stripped.split(',')
                # remove irrrelevant stuff
                rmvidx = range(4,len(splitted)-1)
                for ii in range(len(rmvidx)):
                    splitted.pop(4)
                if splitted[0] == '///':
                    splitted[0] = '//' + str(ii_oupargs)
                    ii_oupargs+=1
                in_arg[splitted[0]] = splitted
                in_arg[splitted[0]][0] = []
            if startpattern in line:
                parsing = True
        fp.close()
        
        self.parsinp = in_arg
        
        for key in in_arg:
            setattr(self, key, in_arg[key][0])
            
        # initialize other variables    
        self.parvar = {}      
        self.parvar_cpl = {}        
        self.HDFfile = []
        
        self.HDF = HDF()
        
        self.segcount = 0
            
    # print the arguments that have been set
    def print_params(self, allel = False):
        for key in sorted(self.parsinp):
            val = getattr(self,key)
            if (val != []) | (allel):
                print('{:<5}: {:>50}    {:<25}'.format(key, val, self.parsinp[key][1]))
       
        
        
    # add parameter variation: 
    # key is the argument to vary
    # idx the indices of values
    # strt the starting point
    # end the endpoint
    # npts the dimension of the sweep
    def parsweep(self, key, strt, end, npts, idx = 0):

        if ~isinstance(idx,list): idx = [idx]   # idx as list eases iteration  
        
        # check the key
        try:
            vals = getattr(self,key)
        except:
            print('Problem with sweep: Key ' + key + ' is not valid! See below for valid keys')
            self.print_params(allel=True)
            return            
            
        # check for existing val and for proper dimension. Dimension is a priori not known due to number of pulses that can be flexible
        if (vals == []):
            print('Problem with sweep: Initialize first a value to argument ' + key +'. I will try with assuming zero')
            vals = 0;
        if isinstance(vals, (list, np.ndarray)):
            if len(vals) < max(idx):
                print('Problem with sweep: ' + key + ' has only ' + str(len(vals)) + ' objects, while an index of ' + str(max(idx)) + ' was requested!')
                return
            startlist = [[vals[jj] for jj in range(len(vals))] for ii in range(npts)]
        elif max(idx) > 0:
            print('Problem with sweep: ' + key + ' is scalar, while an index of ' + str(max(idx)) + ' was requested!')
            return
        else:
            startlist = [[vals] for ii in range(npts)]

        # check if a parvar already exists for this key
        if len(self.parvar) == 0:
            self.parvar['sweeplist'] = startlist
        elif not((key == self.parvar['key']) & (npts == self.parvar['dim'])):
            self.parvar['sweeplist'] = startlist
                
        self.parvar['key'] = key
        self.parvar['dim'] = npts        
        
        if npts > 1:
            incr = (end - strt)/(npts-1)
        else:
            incr = 0;
            
        
        for ii_swp in range(npts):
            for swp_idx in idx:
                self.parvar['sweeplist'][ii_swp][swp_idx] = strt + ii_swp*incr
 
    # add coupled parameter variation of another variable: (one variable is not enough... two neither, but better than one. A list of dicts would more general....) 
    # key is the argument to vary
    # idx the indices of values
    # strt the starting point
    # end the endpoint
    # npts the dimension of the sweep
    def parsweep_cpl(self, key, strt, end, npts, idx = 0):

        if ~isinstance(idx,list): idx = [idx]   # idx as list eases iteration  
        
        # check the key
        try:
            vals = getattr(self,key)
        except:
            print('Problem with sweep: Key ' + key + ' is not valid! See below for valid keys')
            self.print_params(allel=True)
            return            
            
        # check for existing val and for proper dimension. Dimension is a priori not known due to number of pulses that can be flexible
        if (vals == []):
            print('Problem with sweep: Initialize first a value to argument ' + key +'. I will try with assuming zero')
            vals = 0;
        if isinstance(vals, (list, np.ndarray)):
            if len(vals) < max(idx):
                print('Problem with sweep: ' + key + ' has only ' + str(len(vals)) + ' objects, while an index of ' + str(max(idx)) + ' was requested!')
                return
            startlist = [[vals[jj] for jj in range(len(vals))] for ii in range(npts)]
        elif max(idx) > 0:
            print('Problem with sweep: ' + key + ' is scalar, while an index of ' + str(max(idx)) + ' was requested!')
            return
        else:
            startlist = [[vals] for ii in range(npts)]

        # check if a parvar already exists for this key
        if len(self.parvar_cpl) == 0:
            self.parvar_cpl['sweeplist'] = startlist
        elif not((key == self.parvar_cpl['key']) & (npts == self.parvar_cpl['dim'])):
            self.parvar_cpl['sweeplist'] = startlist
                
        self.parvar_cpl['key'] = key
        self.parvar_cpl['dim'] = npts        
        
        incr = (end - strt)/(npts-1)
        
        for ii_swp in range(npts):
            for swp_idx in idx:
                self.parvar_cpl['sweeplist'][ii_swp][swp_idx] = strt + ii_swp*incr

           
            
    def run(self, oup = True):
        # check if there is a parvar or only a single
        if len(self.parvar) == 0:
            self.__run_single(oup)
        else:
            # store the value currently in the swept parameter
            stdval = getattr(self, self.parvar['key'])
            
            if len(self.parvar_cpl) != 0:
                stdval2 = getattr(self, self.parvar_cpl['key'])
            
            # handle the timestamp
            stddatestr = getattr(self,'fst')
            if (stddatestr == []):
                setattr(self, 'fst', datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

            # give it a useful name 
            stdfilepat = getattr(self,'fpa')
            if (stdfilepat == []):
                setattr(self, 'fpa', self.parvar['key'] + '_swp')
                
            # actual iteration over the sweeplist
            for ii in range(self.parvar['dim']):
                setattr(self, self.parvar['key'], self.parvar['sweeplist'][ii])
                if len(self.parvar_cpl) != 0: # as well as the coupled variable
                    setattr(self, self.parvar_cpl['key'], self.parvar_cpl['sweeplist'][ii])
                    
                self.__run_single(oup)
            
            # save parvar info as attribute, which means that we need to detect the file
            if getattr(self,'nos') != 0: # this one is suspicious...
                if self.HDFfile == []:
                    self.HDFfile = self.__guess_savepath()
                try:
                    # this is probably erroneous and was never recognized...! self.parvar is not a key/value pair
                    f = h5py.File(self.HDFfile, 'r+')
                    for key in self.parvar:
                        f.attrs.create(key, self.parvar[key])
                    f.close()
                except:
                    print('Problem opening file ' + self.HDFfile)
                    
            setattr(self, self.parvar['key'], stdval)   # set back to non-swept value
            setattr(self, 'fst', stddatestr)            # set back to non-swept value
            setattr(self, 'fpa', stdfilepat)            # set back to non-swept value
            if len(self.parvar_cpl) != 0:
                setattr(self, self.parvar_cpl['key'], stdval2)   # set back to non-swept value

            
    def readHDF(self, filename = ''):
        if filename != '':
            self.HDFfile = filename
            
        self.HDF.load(self.HDFfile)
        
    
    # helper functoin to guess the savepath from the file. This should not be called, since it should be obtained from the output of the program call        
    def __guess_savepath(self):
        savepath = getattr(self,'spt')
        if savepath == []: savepath = './asdf/' # not recommended here: knowledge about the standard directory in the cpp file.... could be parsed, but user will usually provide a folder to limr.spt
        if savepath[-1] != '/': savepath += '/' # and that little fix since users seldomly put the '/' for the directory...
        savepath = savepath + getattr(self,'fst') + '_' + getattr(self,'fpa') + '.h5'
        return savepath
    
    # run for one single constellation         
    def __run_single(self, oup = True):
        terminated = False
        
        while (terminated == False):
            
            str2call= self.Cprog
            
            for key in self.parsinp:
                vals = getattr(self,key)
                if (vals == []): continue # ignore arguments that are not set
                str2call += ' -' + key   # set the key and then the value/s
                if isinstance(vals, (list, np.ndarray)):
                    for val in vals:
                            str2call +=  ' ' + str(val)
                else:
                    str2call +=  ' ' + str(vals)
                    
                    
            if oup: print(str2call)
            p = subprocess.Popen(str2call, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
              
            if getattr(self,'nos') != 0:         
                terminated = True          
            
            for line_b in p.stdout.readlines():
                line = line_b.decode('utf-8').rstrip()
                if oup: print(line),
                if '.h5' in line:
                    self.HDFfile = line
                    terminated = True
                if 'Unable to open device' in line:
                    terminated = True
                if 'Muted output, exiting immediate' in line:
                    terminated = True
                if self.Cprog + ': not found' in line:
                    terminated = True
                if 'Devices found: 0' in line:
                    terminated = True
                if 'Segmentation' in line:
                    self.segcount += 1
                    terminated = False
            self.retval = p.wait()
            
            if terminated == False:
                print('RE-RUNNING DUE TO PROBLEM WITH SAVING!!!')
            
# class for accessing data of stored HDF5 file
class HDF():
    
    def __init__(self, filename = ''):
        
        # check first for the filename provided
        if filename != '':
            self.HDFsrc = filename
        else:
            self.HDFsrc = ''
        
        # get data
        self.__get_data()
        
    # just an alias for __init__ that does load a specific file
    def load(self, filename = ''):
        self.__init__(filename)
            
    # gets the data of the file        
    def __get_data(self):
        
        if (self.HDFsrc == '') | (self.HDFsrc == []):
            # initialize all as empty
            self.tdy = []
            self.tdx = []
            self.attrs = []
            self.parsoutp = {}
            self.parvar = {}
            
        else:
            f = h5py.File(self.HDFsrc, 'r')
            
    
            HDFkeys = list(f.keys())
            
            for ii, HDFkey in enumerate(HDFkeys):
                if ii == 0:
                    # initialize data array
                    dsize = f[HDFkey].shape
                    inddim = dsize[0]
                    self.tdy = np.zeros((int(dsize[1]/2), int(dsize[0] * len(HDFkeys))),dtype=np.complex_)
                    
                    # initialize the output objects
                    self.attrs = [dynclass() for jj in range(len(HDFkeys))]
                    
                    # get the attribute keys
                    self.parsoutp = {}
                    ii_oupargs = 0
                    for item in f[HDFkey].attrs.items():
                        itemname = item[0][5:]
                        itemarg = item[0][1:4]
                        if not ('///' in itemarg):
                            self.parsoutp[itemarg] = [ item[1], itemname]
                        else:
                            self.parsoutp['//'+str(ii_oupargs)] = [ item[1], itemname]
                            ii_oupargs+=1
                            
                    # look for eventual parvar lists
                    self.parvar = {}
                    for item in f.attrs.items():
                        self.parvar[item[0]] = item[1]
                    
                
                # Get the data
                data_raw = np.array(f[HDFkey])
                try:
                    self.tdy[:,ii*inddim:(ii+1)*inddim] = np.transpose(np.float_(data_raw[:,::2])) + 1j*np.transpose(np.float_(data_raw[:,1::2]))
                except:
                    pass
                    
                    
                # Get the arguments
                ii_oupargs = 0  
                for item in f[HDFkey].attrs.items():
                    itemname = item[0][5:]
                    itemarg = item[0][1:4]
                    if not ('///' in itemarg):
                        setattr(self.attrs[ii], itemarg, item[1])
                    else:
                        setattr(self.attrs[ii], '//'+str(ii_oupargs), item[1])
                        ii_oupargs+=1
            
            f.close()
            srate_MHz = getattr(self.attrs[0], 'sra')*1e-6
            self.tdx = 1/srate_MHz*np.arange(self.tdy.shape[0])

    # get an argument by matching the text description
    def attr_by_txt(self, pattern):
        for key in sorted(self.parsoutp):
            if pattern in self.parsoutp[key][1]: # pattern match
                attr = getattr(self.attrs[0], key)
                try:
                    ouparr = np.zeros( ( len(attr), len(self.attrs)), attr.dtype)
                except:
                    ouparr = np.zeros( ( 1, len(self.attrs)), attr.dtype)
                    
                for ii in np.arange(len(self.attrs)):
                    ouparr[:,ii] = getattr(self.attrs[ii], key)
                return np.transpose(ouparr)
        
        print('Problem obtaining the attribute from the description using the pattern ' + pattern + '!')
        print('Valid descriptions are: ')
        self.print_params()
        
    # get an argument by key
    def attr_by_key(self, key):
        if key in dir(self.attrs[0]):
            attr = getattr(self.attrs[0], key)
            try:
                ouparr = np.zeros( ( len(attr), len(self.attrs)), attr.dtype)
            except:
                ouparr = np.zeros( ( 1, len(self.attrs)), attr.dtype)
            for ii in np.arange(len(self.attrs)):
                ouparr[:,ii] = getattr(self.attrs[ii], key)
            return np.transpose(ouparr)
        
        print('Problem obtaining the attribute from key ' + key + '!')
        print('Valid keys are: ')
        self.print_params()
               

    # print the arguments
    def print_params(self, ouponly = False):
        for key in sorted(self.parsoutp):
            val = getattr(self.attrs[0], key)
            if not('//' in key):    # input argument?
                if ouponly: continue;
                    
            print('{:<5}: {:>50}    {:<25}'.format(key, val, self.parsoutp[key][1]))
            
    def plot_dta(self, fignum = 1, stack = False, dtamax = 0.0):
        if (fignum == 1) & stack: fignum = 2;
            
        if self.tdy != []:
            
            if dtamax == 0:
                dtamax = np.max(np.max(abs(self.tdy),axis=0))
            offset = 1.5*dtamax
            
            plt.figure(fignum)
            plt.clf()
            if stack:
                for ii in np.arange(self.tdy.shape[1]):
                    plt.plot(self.tdx, self.tdy[:,ii].real + ii* offset)
            else:
                plt.plot(self.tdx, self.tdy.real)
            plt.xlabel('$t$ [$\mu$s]')
            plt.ylabel('$y$ [Counts]')
                
# empty class to store dynamic attributes, basically for the attributes in HDF keys
class dynclass:
    pass


# addendum that does not fit 100% into this class file, but is related
# class to control the E3631A via serial interface
import serial
import time
from os import listdir

class PSU():
    
    def __init__(self):

        self.GperV = 14.309
        self.sleeptime = 0.4
        
        devdir = '/dev/'
        ttydevs = [f for f in listdir(devdir) if 'ttyUSB' in f]
#        ttydev = devdir + [f for f in ttydevs if int(f[-1]) > 4][0]
        ttydev = devdir + [f for f in ttydevs][0]
            
        self.psu=serial.Serial(ttydev, stopbits=2, dsrdtr=True)

        # read at the beginning to remove eventual junk
        response = self.psu.read_all()

        self.psu.write("*IDN?\r\n")
        time.sleep(self.sleeptime)
        response = self.psu.read_all()
        if response == 'HEWLETT-PACKARD,E3631A,0,2.1-5.0-1.0\r\n':
            print('Success in opening the HP PSU!')
        else:
            print('Fail!!!')
            
        self.psu.write("INST:SEL P6V\r\n")
        time.sleep(self.sleeptime)
        self.psu.write("OUTP:STAT ON\r\n")
        time.sleep(self.sleeptime)
        
        self.psu.close()


    def getVoltage(self):
        
        if not self.psu.isOpen():
            self.psu.open()
        # read at the beginning to remove eventual junk
        self.psu.read_all()
        time.sleep(self.sleeptime)
        self.psu.write("VOLT?\r\n")
        time.sleep(self.sleeptime)
        actval = float(self.psu.read_all())
        self.psu.close()
        return actval
        
        
    def setVoltage(self, setval, dV = 0.02, ramptime = 0.1):
        
        actval = self.getVoltage()
        
        diff = setval  - actval
        dVsigned = dV * (-1 if diff < 0 else 1)
        
        if not self.psu.isOpen():
            self.psu.open()
        while (abs(diff) > dV):
            actval += dVsigned
            diff -= dVsigned
            self.psu.write("VOLT " + str(actval) + "\r\n")
            time.sleep(ramptime)
        
        self.psu.write("VOLT " + str(setval) + "\r\n")
        time.sleep(ramptime)
        
        self.psu.close()
        
    def getField(self):
        
        return self.getVoltage() * self.GperV

    def setField(self, field):
        
        return self.setVoltage(field / self.GperV)
