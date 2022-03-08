#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 15:07:27 2021

@author: luki
"""

import serial
#import time
import matplotlib.pyplot as plt
import csv
#from subprocess import call, Popen
import numpy as np


def loadPlot(filename):
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
