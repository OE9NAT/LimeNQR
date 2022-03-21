# GUI for SDR based NQR system - "LimeNQR"

A intuitive gaphical user interface (GUI) for a software defined radio (SDR) which is used for the nuclear quadrupole resonance (NQR) spectroscopy was developed. Additional a automatic data handling system was impplemented as it is essential for an efficient testing and measuring. A automated structured workflow minimises the risk of experiment errors an the loss of important acquired data. Additionally a Sequence generator was implemented with the ability to dynamic select, from one pulse up to ten pulses. The GUI is able to be used to set the represented Phases from φmin =0 up till φmax =2π for every pulse and all the hardware specific parameters.
As one of the requirement was that the Software will be used for a lab exercise with students, it should include warning statements if destructive settings are saved to be run on the SDR. On the other hand for experienced user it has the ability to load standardised .cfg files from the system.

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

Lanching will show the main window where everythink can be controled from and also start the sequence. 
![main window](https://github.com/OE9NAT/bacharbeit/blob/on_hardware2/images/win_main.JPG)
It will allow the user to load preset files from previus measuremnts but he can also set some new variables. 

After selectingt all parameters and setting its limits for the range of
 intrest the information can first be send to the Arduino to set the 
resonat circuit and than to the SDR for sweeping the frequency band.
When all measured infromation is collected it will be stored in the file
 struckture as devined in de main GUI for later analyses.


For ease of use in the main window there is a window plot available.
It will allow a detailed analysis of the last measured data and all 
previus ones.

Have a good measurment.

https://asciiflow.com/#/


