
import h5py
import numpy as np
import matplotlib.pyplot as plt
import os


def plot(filename):
    #filename = "file.hdf5"
    #filename = "./signals/20210916_174823_setup.h5"
    #filename = "/home/pi/lukas_bararbeit/signals/11111111111_093701_setup.h5"

    folder_signal = "signals_TEST/"

    font_plot = {'family': 'serif', 'color':  'darkred',
                 'weight': 'normal', 'size': 16}

    with h5py.File(filename, "r") as f:
        # List all groups
        print("Keys: %s" % f.keys())
        a_group_key = list(f.keys())[0]

        # Get the data
        data_raw = list(f[a_group_key])
        print("\n data length: ", len(data_raw))
        print("end of import")
        print("data_raw ", type(data_raw), "\n")
        print(list(f.keys()))
        description = list(f.keys())
        data = data_raw[0]
        print(data)
        #data_1 = data_raw[1]

    #print(*data, sep="\n ")

    print("\n data description: ", description)
    print("\n legth of datasampels", len(data))
    print("\n type of datasampels", type(data))
    print("\n data: ", (data))

    samp_rate = int(30.72 * (10 ^ 6))  # Samples/s
    time_length = abs((len(data)/samp_rate)/(10 ^ (-6)))
    print((10 ^ (-6)), "time_length", samp_rate)
    time = np.linspace(0, time_length, len(
        data), endpoint=False)  # in micro sec

    # stimulus
    stimulus_data_start = 0
    stimulus_data_end = 600

    stimulus_data = data[stimulus_data_start:stimulus_data_end]
    stimulus_time = time[stimulus_data_start:stimulus_data_end]
    #print("stimulus_time ",stimulus_time)

    f = 20  # Frequency, in cycles per second, or Hertz
    f_s = 1000  # Sampling rate, or number of measurements per second
    t = np.linspace(0, 2, 2 * f_s, endpoint=False)
    #stimulus_data = np.sin(f * np.pi * t)

    stimulus_data_fft = np.fft.rfft(stimulus_data)
    stimulus_data_fft = abs(stimulus_data_fft)

    # replay
    replay_data_start = 900
    replay_data_end = 1400

    replay_data = data[replay_data_start:replay_data_end]
    replay_time = time[replay_data_start:replay_data_end]
    print("legth of replay_data", len(replay_data))

    # replay fft
    replay_data = np.asarray(replay_data, dtype=np.float32)
    replay_data_fft = np.fft.rfft(replay_data)
    replay_data_fft = abs(replay_data_fft)

    print("legth of datasampels", len(data))

    plt.figure()
    plt.plot(time[0:1000], data[0:1000])
    titel_plot = "Timedomain " + filename[45:-1]
    plt.title(titel_plot, fontdict=font_plot)
    plt.xlabel("time (ms)", fontdict=font_plot)
    plt.ylabel("voltage (mV)", fontdict=font_plot)
    text = "min: "+str(replay_data_start) + "\n max: "+str(replay_data_end)
    plt.text(150, 150, text, fontdict={
             'family': 'serif', 'weight': 'normal', 'size': 10})

    save_filename = folder_signal+"/plots/" +"sample_" + filename[42:-4] 
    print("save_filename", save_filename+ ".jpg")
    plt.savefig(save_filename+ ".jpg")
    plt.savefig(save_filename+ ".svg")

    # plt.show()

    #figure, ax = plt.subplots(nrows=2, ncols=2)
    figure, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    figure.tight_layout(pad=2.0)
    figure.set_size_inches(14, 10, forward=True)

    #ax1 = plt.subplot(211)
    # ax1.margins(0.05)

    ax1.plot(stimulus_time, stimulus_data)
    ax1.set_title("Time-domain stimulus", fontdict={'size': 10})
    ax1.set_xlabel('time in µsec', fontsize=8)
    ax1.set_ylabel('amplitude in mV', fontsize=8)

    ax2.plot(replay_time, replay_data)
    ax2.set_title("Time-domain replay", fontdict={'size': 10})
    ax2.set_xlabel('time in µsec', fontsize=8)
    ax2.set_ylabel('amplitude in mV', fontsize=8)

    ax3.plot(stimulus_data_fft)
    ax3.set_title("Frequency-domain stimulus", fontdict={'size': 10})
    ax3.set_xlabel('frequency in Hz', fontsize=8)
    ax3.set_ylabel('amplitude in mV', fontsize=8)

    ax4.plot(replay_data_fft)
    ax4.set_title("Frequency-domain replay", fontdict={'size': 10})
    ax4.set_xlabel('frequency in Hz', fontsize=8)
    ax4.set_ylabel('amplitude in mV', fontsize=8)


    plt.savefig(save_filename+".jpg")
    #plt.show()

    return figure


if __name__ == "__main__":

    files = []
    folder_signal = "signals_TEST/"

    for file in os.listdir(folder_signal):
        if file.endswith(".h5"):
            file_name = os.path.join(folder_signal, file)
            # print(file_name,"\n")
            files.append(file_name)

            file = "signals_TEST/live_scan_data.csv"
        #file_name = os.path.join(folder_signal, file)

    file = "signals_TEST/live_scan_data.csv"

    fig =plot(file)


    # exit()

    for file in files:
        print("\n \n loop", file)
        plot(file)

        break
    # plt.plot(tdx,tdy)
