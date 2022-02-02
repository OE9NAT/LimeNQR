# GUI for a SDR controlled magnetic resonance imaging - contrast agent analyse controller

To start gui run start.py file.

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


