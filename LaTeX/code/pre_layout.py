from pre_function import *
print("-_____start layout____-")

#import sys
#import numpy as np
#import matplotlib
#import tkinter as tk
#import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import (
# FigureCanvasTkAgg, NavigationToolbar2Tk)


# read and save input vales from GUI and save it to config.cfg file
def save_values():
    global input_values
    input_values = {}
    print("save input_values to config.cfg file")

    input_values["freq_start"] = freq_start_input.get()
    input_values["freq_end"] = freq_end_input.get()
    input_values["freq_step"] = freq_step_input.get()
    input_values["average"] = average_input.get()
    input_values["freq_end"] = freq_end_input.get()
    input_values["Tune_U_max"] = Tune_U_max_input.get()
    input_values["Match_U_max"] = Match_U_max_input.get()
    input_values["V_step"] = V_step_input.get()
    input_values["puls"] = puls_input.get()
    input_values["Dwell_t"] = Dwell_t_input.get()
    input_values["seq_steps"] = seq_steps_input.get()
    input_values["source_pw"] = source_pw_input.get()
    input_values["file_path"] = file_path_input.get()

    print("loadet all", input_values)

    # write to .cfg file
    config = configparser.ConfigParser()
    config["input_values"] = input_values
    with open('config.cfg', 'w') as configfile:
        config.write(configfile)

    return input_values


# Setup of gui
window_main = tk.Tk()
window_main.title("GUI for bach")
# Fensterbreite,hoehe, on secreen offset x, on screen offset y
window_main.geometry("1200x800+10+10")
window_main.option_add("Helvetica", '10')  # Frischart und groesse
window_main.resizable(width=False, height=False)  # False = no resize
#window_main.minsize(width_minsize=1200, height_minsize=800)
# ws.maxsize(350, 450)


#"red" "orange" "yellow" "green" "blue" "purple" "white" "black"
lable_text = tk.Label(text="Projekt Title ", foreground="green",
                      background="black", font=("Helvetica", 30))
lable_text.place(x=450, y=5, width=400, height=50)

######----- Measurement Settings ------######
input_width = 100
text_input_height = 30

lable_text = tk.Label(text="Measurment Settings ", foreground="green",
                      background="white", font=("Helvetica", 15))
lable_text.place(x=10, y=60, width=300, height=30)

# start frequency
freq_start_lable = tk.Label(text="START Frequency: ", background="green")
freq_start_lable.place(x=5, y=100, width=160, height=text_input_height)
simple_label("MHz", 290, 100)

freq_start_input = tk.Entry(fg="black", bg="white", width=40)
freq_start_input.place(x=200, y=100, width=input_width,
                       height=text_input_height)

# end frequency
freq_end_lable = tk.Label(text="END frequency: ", background="red")
freq_end_lable.place(x=5, y=150, width=160, height=text_input_height)
simple_label("MHz", 290, 150)Frequency

freq_end_input = tk.Entry(fg="black", bg="white", width=40)
freq_end_input.place(x=200, y=150, width=input_width, height=text_input_height)


# freq Steps
freq_step_lable = tk.Label(text="Frequency steps: ", background="orange")
freq_step_lable.place(x=5, y=200, width=160, height=text_input_height)
simple_label("steps", 290, 200)

freq_step_input = tk.Entry(fg="black", bg="white", width=40)
freq_step_input.place(x=200, y=200, width=input_width,
                      height=text_input_height)

# average
average_lable = tk.Label(text="number of average: ", background="orange")
average_lable.place(x=5, y=250, width=160, height=text_input_height)
simple_label("steps", 300, 250)

average_input = tk.Entry(fg="black", bg="white", width=40)
average_input.place(x=200, y=250, width=input_width, height=text_input_height)

button_run = tk.Button(window_main, text="RUN measurment",
                       command=RUN, foreground="green")
button_run.place(x=50, y=300, width=200, height=50)

######----- Tune&Match Settings ------######
lable_text = tk.Label(text="Tune&Match Settings", foreground="green",
                      background="white", font=("Arial Bold", 15))
lable_text.place(x=400, y=60, width=300, height=30)

# Tune U_max
Tune_U_max_lable = tk.Label(text="Tune U_max: ")
Tune_U_max_lable.place(x=400, y=100, width=160, height=text_input_height)
simple_label("V", 700, 100)

Tune_U_max_input = tk.Entry(fg="black", bg="white", width=40)
Tune_U_max_input.place(x=600, y=100, width=input_width,
                       height=text_input_height)


# Match U_max
Match_U_max_lable = tk.Label(text="Match U_max  : ")
Match_U_max_lable.place(x=400, y=150, width=160, height=text_input_height)
simple_label("V", 700, 150)

Match_U_max_input = tk.Entry(fg="black", bg="white", width=40)
Match_U_max_input.place(x=600, y=150, width=input_width,
                        height=text_input_height)

# Voltage steps
V_step_lable = tk.Label(text="number of average: ")
V_step_lable.place(x=400, y=200, width=160, height=text_input_height)
simple_label("steps", 700, 200)

V_step_input = tk.Entry(fg="black", bg="white", width=40)
V_step_input.place(x=600, y=200, width=input_width, height=text_input_height)

send_TMfile = tk.Button(window_main, text="Send TM-file",
                        command=RUN, foreground="green")
send_TMfile.place(x=500, y=300, width=200, height=50)


######----- Loading  ------######
lable_text = tk.Label(text="Sequence Settings", foreground="green",
                      background="white", font=("Arial Bold", 15))
lable_text.place(x=800, y=60, width=300, height=30)

# Pulse

pulse_lable = tk.Label(text="Pulse: ")
pulse_lable.place(x=800, y=100, width=160, height=text_input_height)
puls_input = tk.Entry(fg="black", bg="white", width=40)
puls_input.place(x=1000, y=100, width=input_width, height=text_input_height)

# Dwell time
Dwell_t_lable = tk.Label(text="Dwell time: ")
Dwell_t_lable.place(x=800, y=150, width=160, height=text_input_height)

Dwell_t_input = tk.Entry(fg="black", bg="white", width=40)
Dwell_t_input.place(x=1000, y=150, width=input_width, height=text_input_height)

# Nr. of Points
seq_steps_lable = tk.Label(text="Nr. of steps: ")
seq_steps_lable.place(x=800, y=200, width=160, height=text_input_height)
simple_label("steps", 1100, 250)

seq_steps_input = tk.Entry(fg="black", bg="white", width=40)
seq_steps_input.place(x=1000, y=200, width=input_width,
                      height=text_input_height)

# Source PW
source_pw_lable = tk.Label(text="Source PW: ")
source_pw_lable.place(x=800, y=250, width=160, height=text_input_height)

source_pw_input = tk.Entry(fg="black", bg="white", width=40)
source_pw_input.place(x=1000, y=250, width=input_width,
                      height=text_input_height)
simple_label("%", 1100, 250)

# Filepath for Storage for loading data
file_path_lable = tk.Label(text="Filepath: ")
file_path_lable.place(x=800, y=300, width=160, height=text_input_height)

file_path_input = tk.Entry(fg="black", bg="white", width=40)
file_path_input.place(x=1000, y=300, width=input_width,
                      height=text_input_height)


######----- Plotter  ------######
#btn = tk.Label(window_main, text='A simple plot', foreground="green",background="white", font=("Arial Bold", 15))
#btn.place(x = 10, y = 350, width=200, height=30)


t = np.arange(0.0, 2.0, 0.01)
s1 = np.sin(2*np.pi*t)
s2 = np.sin(4*np.pi*t)

#fig = plt.figure(figsize=(1, 2))
fig = plt.figure()
# set the spacing between subplots
plt.subplots_adjust(left=0.07, bottom=0.06, right=0.99,
                    top=0.9, wspace=0.4, hspace=0.4)


time_plot = plt.subplot(211)
plt.plot(t, s1)
time_plot.title.set_text("Time")
plt.grid()


feq_plot = plt.subplot(212)
plt.plot(t, 2*s1)
feq_plot.title.set_text("Frequency")
plt.grid()


# specify the window as master
canvas = FigureCanvasTkAgg(fig, master=window_main)
canvas.draw()
canvas.get_tk_widget().place(x=10, y=360, width=500, height=400)

# navigation toolbar for the Plot
toolbarFrame = tk.Frame(master=window_main)
toolbarFrame.place(x=50, y=760, width=450, height=35)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


######----- Buttens  ------######

butons_y = 740  # hight of buttens

button_run = tk.Button(window_main, text="RUN",
                       command=RUN, foreground="green")
button_run.place(x=550, y=butons_y, width=150, height=50)

button_val = tk.Button(window_main, text="variable_input_win",
                       command=lambda:  Varify_meas_set("HI"), foreground="red")
button_val.place(x=700, y=butons_y, width=150, height=50)


close_button = tk.Button(window_main, text="save_values", command=save_values)
close_button.place(x=850, y=butons_y, width=150, height=50)

exit_button = tk.Button(window_main, text="Beenden", command=window_main.quit)
exit_button.place(x=1000, y=butons_y, width=150, height=50)


# show window, wait for user imput
window_main.mainloop()

print("-_____END layout____-")
