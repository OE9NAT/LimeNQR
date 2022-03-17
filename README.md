# GUI for SDR based NQR system - "LimeNQR"

A intuitive gaphical user interface (GUI) for a software defined radio (SDR) which is used for the nuclear quadrupole resonance (NQR) spectroscopy was developed. Additional a automatic data handling system was impplemented as it is essential for an efficient testing and measuring. A automated structured workflow minimises the risk of experiment errors an the loss of important acquired data. Additionally a Sequence generator was implemented with the ability to dynamic select, from one pulse up to ten pulses. The GUI is able to be used to set the represented Phases from φmin =0 up till φmax =2π for every pulse and all the hardware specific parameters.
As one of the requirement was that the Software will be used for a lab exercise with students, it should include warning statements if destructive settings are saved to be run on the SDR. On the other hand for experienced user it has the ability to load standardised .cfg files from the system.

To start the GUI, run in the terminal window the start.py file.

This Program will first chek the right version of python. 
It will also chek if all necessary imports and modulse are available.

After loading the setting.cfg file it will check for plausilbility and 
hardware limits of all variables set.


Lanching the main.py will show the GUI of the main Window. It is 
desined that everythink can be started and controled from there. 
It will allow the user to load preset files from previus measuremnts
but he can also set some new variables. 

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


