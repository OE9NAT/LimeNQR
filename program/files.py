def load_file(path="data", experiment="test_experiment", cycle="test_cycle"):
    print("load")
    print("path"+path+"experiment" + experiment + "cycle" + cycle)

    import tkinter as tk
    # import tkinter.ttk as TTK #use for Combobox

    ######----- Setup of gui ------######
    window_experiment = tk.Tk()
    window_experiment.title("load experiment")
    # window_experiment.wm_iconbitmap(bitmap="@/home/pi/Bach_arbeit/stethoskop.xbm")
    window_experiment.wm_iconbitmap(bitmap=logo_path)
    # Fensterbreite,hoehe, on secreen offset x, on screen offset y
    window_experiment.geometry("600x520")
    window_experiment.option_add("Helvetica", '10')  # Frischart und groesse
    window_experiment.resizable(width=False, height=False)  # False = no resize
    text_input_height = 30

    def save_experiment():
        print("save all parameters to .cfg file")
        status_lable = tk.Label(window_experiment, text="updated sequenz !!")
        status_lable.place(x=10, y=250, width=500, height=text_input_height)

        # global experiment = {}
        experiment_dict["data"] = data.get()
        experiment_dict["experiment"] = experiment.get()
        experiment_dict["cycle"] = cycle.get()

        print(experiment_dict)

        path_lable.config(text="Seq. for data: "+experiment_dict["data"])
        experiment_lable.config(
            text="Seq. for experiment: "+experiment_dict["experiment"])
        cycle_lable.config(text="Seq. for cycle: "+experiment_dict["cycle"])

        save_values(
            experiment_dict["data"], experiment_dict["experiment"], experiment_dict["cycle"])
        print("end of save_experiment")

    # Title
    lable_text = tk.Label(window_experiment, text="Set Experiment strukture ",
                          foreground="green", background="OliveDrab4", font=("Helvetica", 30))
    lable_text.place(x=50, y=10, width=500, height=50)

    # Set parameters
    text_input_height = 40
    path_text = "Seq. for data: "+path
    path_lable = tk.Label(
        window_experiment, text=path_text, background="gray50")
    path_lable.place(x=50, y=100, width=500, height=text_input_height)

    experiment_text = "Seq. for experiment: "+experiment
    experiment_lable = tk.Label(
        window_experiment, text=experiment_text, background="gray50")
    experiment_lable.place(x=50, y=150, width=500, height=text_input_height)

    cycle_text = "Seq. for cycle: "+cycle
    cycle_lable = tk.Label(
        window_experiment, text=cycle_text, background="gray50")
    cycle_lable.place(x=50, y=200, width=500, height=text_input_height)

    # Experiment
    gray_light = "gray70"
    path_lable_input = tk.Label(
        window_experiment, text="Set Seq. data: ", background=gray_light)
    path_lable_input.place(x=50, y=300, width=300, height=40)
    data = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    data.place(x=350, y=300, width=200, height=40)

    experiment_lable_input = tk.Label(
        window_experiment, text="Set Seq. experiment: ", background=gray_light)
    experiment_lable_input.place(x=50, y=350, width=300, height=40)
    experiment = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    experiment.place(x=350, y=350, width=200, height=40)

    cycle_lable_input = tk.Label(
        window_experiment, text="Set Seq. cycle: ", background=gray_light)
    cycle_lable_input.place(x=50, y=400, width=300, height=40)
    cycle = tk.Entry(window_experiment, fg="black", bg="white", width=40)
    cycle.place(x=350, y=400, width=200, height=40)

    # Buttons
    save_button = tk.Button(window_experiment, text="Save",
                            background="SkyBlue4", command=lambda:  save_experiment())
    save_button.place(x=50, y=450, width=140, height=50)

    save_button = tk.Button(window_experiment, text="load",
                            command=lambda: print("butten load"))
    save_button.place(x=230, y=450, width=140, height=50)

    close_button = tk.Button(window_experiment, text="Close",
                             background="tomato4", command=window_experiment.destroy)
    close_button.place(x=410, y=450, width=140, height=50)

    return print("closing load file")
