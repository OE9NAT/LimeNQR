import os
import sys
import configparser
import PIL.Image as image


import logging  # DEBUG INFO WARNING ERROR
from logging.handlers import QueueHandler

logger_win_load_seq = logging.getLogger('win_load_seq')
logger_win_load_seq.addHandler(logging.StreamHandler())
logger_win_load_seq.info("logging from win_seq_puls start up")


class Puls:
    def __init__(self, P1="10", TP1="20", TE1="30", TA="40"):  # **kwargs
        self.puls_1 = P1
        self.pulspause_1 = TP1
        self.echo_1 = TE1
        self.acquire = TA
        self.nr_puls = 1

        print("\n duration of 1st puls ", P1)
        print("\n duration of 1st puls pause ", TP1)
        print("\n duration of 1st Echo ", TE1)
        print("\n ___ \n time of Acquire ", TA)

    def add_puls(P, TP, TE):
        print("add puls to sequence")

### save new experiment ###


def save_file(path, experiment="test_experiment_1", data="test_data_11"):
    data = path+"/"+experiment+"/"+data

    try:
        # os.mkdir(experiment)
        os.makedirs(data)
    except OSError as error:
        print("error file1 Experiment olready exists")
        logger_win_load_seq.error('error message')

    return "testing save"

# read and save input vales from GUI and save it to config.cfg file


def save_values(path="test_data", experiment="test_experiment", data="test_data"):
    cfg_section = "puls_sequenz"
    input_values = {}
    print("save to cfg_section: " + cfg_section)

    input_values["P_1"] = globals()["P_1_input"].get()
    input_values["TP_1"] = globals()["TP_1_input"].get()
    input_values["TA"] = globals()["TA_input"].get()

    path_lable.config(text="Seq. for data: "+path)
    experiment_lable.config(text="Seq. for experiment: "+experiment)
    data_lable.config(text="Seq. for data: "+data)

    logger_win_load_seq.info('load inputs from save_valsues ')
    print("loadet all in save_values", input_values)

    # read and write to config.cfg
    config = configparser.ConfigParser()

    # generate files
    save_file(path, experiment, data)
    config["filepath"] = {"path": path,
                          "experiment": experiment, "data": data}

    # save sequence file
    data = path+"/"+experiment+"/"+"config.cfg"
    try:
        with open(data, "r") as configfile:
            print("####### ___"+data)
            # config.read("config.cfg")

        print("_____________________ TEST pre ______________________")
        print("available of file_path ___ ",
              config.has_option(cfg_section, "file_path"))
        print("available of puls_sequence ___ ",
              config.has_option(cfg_section, "puls_sequence"))
        print("types of sections avalibel ____ ", config.sections())
        # print("types of options avalibel of option ___ ", config.has_option(cfg_section, "file_path"))
        print("_____________________ TEST after ______________________")

        if config.has_section(cfg_section):  # config.has_option(section, option)
            print(".cfg section exist ", data)
            config[cfg_section] = input_values
            logger_win_load_seq.info('Values were saved and overwritten')
        else:
            print(".cfg section dose not exist")
            config.add_section(cfg_section)
            config[cfg_section] = input_values
            logger_win_load_seq.info('Values were saved and new written')

    except IOError:
        print("generated new .cfg file ", data)
        config[cfg_section] = input_values
        logger_win_load_seq.info('Values were saved and written to a new file')

    with open(data, "w") as configfile:
        print("## save .cfg to __", data)
        config.write(configfile)
    logger_win_load_seq.info('save_values end ')


### loading data from past experiments ####
class win_load_file(tk.Tk):

    def __init__(self, path="test_sample", experiment="test_experiment", data="test_data", *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        ######----- contant ------######
        frame_boarder = 4
        self.path = path
        self.experiment = experiment
        self.data = data

        text_log = "class window _main calling filestrukture"
        text_log = text_log + "path " + path + "\n"
        text_log = text_log + "experiment " + experiment + "\n"
        text_log = text_log + "data " + data + "\n"

        logger_win_load_seq.info(text_log)
        print("def win_load_seq from win_load_seq.py\n" + log_text)

        import tkinter as tk
        # import tkinter.ttk as TTK #use for Combobox

        ######----- Setup of gui ------######
        window_experiment = tk.Tk()
        window_experiment.title("set new experiment")
        window_experiment.wm_iconbitmap(bitmap=log_path)
        # Fensterbreite,hoehe, on secreen offset x, on screen offset y
        window_experiment.geometry("1000x750")
        window_experiment.option_add(
            "Helvetica", '10')  # Frischart und groesse
        window_experiment.resizable(
            width=False, height=False)  # False = no resize

        self.frame_path_view = tk.Frame(self, bg='grey')
        self.frame_measure.grid(row=0, column=0, padx=frame_boarder,
                                pady=frame_boarder, sticky="nsew")

        self.strukture_title = tk.Label(
            frame_path_view, text="Set Experiment Strukture ")
        self.strukture_title.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5)

        self.strukture_sampel = tk.Label(
            frame_path_view, text="Sample:  \n Example: Puls shaping")
        self.strukture_sampel.grid(row=1, column=0, padx=5, pady=5)

        self.strukture_experiment = tk.Label(
            frame_path_view, text="Experiment: \n Example: Bismut ")
        self.strukture_experiment.grid(row=1, column=0, padx=5, pady=5)

        self.strukture_data = tk.Label(
            frame_path_view, text="Data: \n Example: FID,Echo ")
        self.strukture_data .grid(row=1, column=0, padx=5, pady=5)

        self.frame_path_set = tk.LabelFrame(
            self, text="storage path", bg='grey')
        self.frame_measure.grid(row=1, column=0, padx=frame_boarder,
                                pady=frame_boarder, sticky="nsew")

        self.sampel_label = tk.Label(
            self.frame_path, text="Sample:  \n Example: Puls shaping")
        self.sampel_label.grid(row=1, column=0, padx=5, pady=5)

        self.experiment_label = tk.Label(
            self.frame_path, text="Experiment: \n Example: Bismut ")
        self.experiment_label.grid(row=1, column=0, padx=5, pady=5)

        self.frame_path_set = tk.Label(
            self.frame_path, text="Data: \n Example: FID,Echo ")
        self.frame_path_set.grid(row=1, column=0, padx=5, pady=5)

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
        experiment_lable.place(x=50, y=150, width=500,
                               height=text_input_height)

        data_text = "Seq. for data: "+data
        data_lable = tk.Label(
            window_experiment, text=data_text, background="gray50")
        data_lable.place(x=50, y=200, width=500, height=text_input_height)

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
        experiment = tk.Entry(
            window_experiment, fg="black", bg="white", width=40)
        experiment.place(x=350, y=350, width=200, height=40)

        data_lable_input = tk.Label(
            window_experiment, text="Set Seq. data: ", background=gray_light)
        data_lable_input.place(x=50, y=400, width=300, height=40)
        data = tk.Entry(window_experiment, fg="black", bg="white", width=40)
        data.place(x=350, y=400, width=200, height=40)

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

        def save_experiment():

            self.button_last_run.grid(row=7, column=0,
                                      padx=5, pady=5, sticky="ew")
            print("save all parameters to .cfg file")
            status_lable = tk.Label(
                window_experiment, text="updated sequence !!")
            status_lable.place(x=10, y=250, width=500,
                               height=text_input_height)

            # global experiment = {}
            experiment_dict["data"] = data.get()
            experiment_dict["experiment"] = experiment.get()
            experiment_dict["data"] = data.get()

            print(experiment_dict)

            path_lable.config(text="Seq. for data: "+experiment_dict["data"])
            experiment_lable.config(
                text="Seq. for experiment: "+experiment_dict["experiment"])
            data_lable.config(text="Seq. for data: "+experiment_dict["data"])

            save_values(
                experiment_dict["data"], experiment_dict["experiment"], experiment_dict["data"])
            print("end of save_experiment")


#    colour http://www.science.smith.edu/dftwiki/images/thumb/3/3d/TkInterColorCharts.png/700px-TkInterColorCharts.png
if __name__ == "__main__":
    # for testing
    print("-_____start import puls_win")
    import os
    import configparser
    import PIL.Image as image

    import logging  # DEBUG INFO WARNING ERROR
    from logging.handlers import QueueHandler
    # logger = logging.basicConfig(filename="logging.log", level=logging.DEBUG, # <- set logging level
    #          format="%(asctime)s:%(levelname)s:%(message)s"  ) # set level

    logger_win_load_seq = logging.getLogger(__name__)
    logger_win_load_seq.setLevel(logging.DEBUG)  # <- set logging level
    log_handler = logging.FileHandler("log_file.log")
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    log_handler.setFormatter(formatter)
    logger_win_load_seq.addHandler(log_handler)

    logger_win_load_seq.info("set upp logger in puls_win.py")

    import function

    print("-_____start puls_win")

    path = os.getcwd()
    print("The current working directory is %s" % path)

    print("__testrun_save_1__")

    win = windows_file(
        path="test_data", experiment="test_experiment_3", data="test_data_3")
    print("start")
    # win.mainloop()

    a, b, *c = (1, 2, 3, 4, 5)

    print("__ end pre_file.py__")
