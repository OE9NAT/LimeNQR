# GUI for SDR based NQR system - "LimeNQR"

An intuitive gaphical user interface (GUI) for a software defined radio (SDR), which is used for the nuclear quadrupole resonance [(NQR)](https://www.tugraz.at/institute/ibi/research/nuclear-quadrupole-resonance/)  spectroscopy, was developed. Additional a automatic data handling system was impplemented as it is essential for an efficient testing and measuring. A automated structured workflow minimises the risk of experiment errors an the loss of important acquired data. Additionally a Sequence generator was implemented with the ability to dynamic select, from one pulse up to ten pulses. The GUI is able to be used to set the represented Phases from φmin =0 up till φmax =2π for every pulse and all the hardware specific parameters.
As one of the requirement was that the Software will be used for a lab exercise with students, it has a plausability check of inputvariabels and additionaly the ability to include warning statements for destructive settings to be run on the hardware. On the other hand for experienced users it has the ability to load standardised .cfg files from the system.

How to check if the correct Python verison is on the system.
```
>python --version
Python 3.9.7
```

Start the GUI, run the terminal window in the folder where the file start.py is located with the following python command.
```
>python start.py
```
output:
```
logging from start up
start GUI
number of treads running:  1
current treads:  <_MainThread(MainThread, started 14904)>
list of all treads:  [<_MainThread(MainThread, started 14904)>]
************************************************

    Autor: Philipp MALIN
    Date: 01.07.2021
    Version: 1.2
    Description: Grapical user interface to control SDR
                 for Nuclear Quadrupole Resonance spectroscopy.

************************************************
Python version  3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021,
start test python version 3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit (AMD64)]
Check list:
('test_version', True)
('test_import', True)
('test_settings', True)


imports alles ok
```

The Program will first check for the right version of python. 
It will also check if all necessary imports and modulse are available.

Lanching will show the main window where everythink can be controlled from and also presents the start butten to run the sequence. 
![main window](https://github.com/OE9NAT/bacharbeit/blob/main/images/main_window_0.png)
It will allow the user to load pre set files from previus measuremnts but he can also set some new variables. 

After selectingt all parameters and setting its limits for the range of intrest the information will be sent to the hardware automaticaly.  First the tuning and matching unit will set the resonat circuit and than the SDR will make the measurment at the particular frequency. The repetative measurment process will be done for the number of samples averages adjusted. Reiterating the tuning and matching for the specified frequency band range will follow in the specified step size.
When all measured information is collected it will be stored in the file struckture as referred in the main GUI.


For ease of use in the main window there is a window for re-evaluations and visualisation available.
With further development it will allow a detailed analysis of the last measured data and all previus ones.

Have a great measurment.


https://asciiflow.com/#/


