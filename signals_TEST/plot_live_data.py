import csv
import numpy as np
import matplotlib.pyplot as plt

file = "signals_TEST/live_scan_data.csv"
# file_name = os.path.join(folder_signal, file)

with open(file, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    data = [data for data in spamreader]
# print("data .csv\n", *data)
# print("data firt list ", data[0])
del data[0]  # ['frequency', 'amplitude'] remove description from colems
data_fequency = [float(data[i][0]) for i, val in enumerate(data)]
data_amplitude = [float(data[i][1]) for i, val in enumerate(data)]
# print("data_feq", *data_fequency, sep="\n")
print("test", float(data_amplitude[0]), type(data_amplitude[0]))

# fig = plt.figure(figsize=(1, 2))
fig = plt.figure()
fig.set_size_inches(6, 4.0, forward=True)
# fig.savefig('test2png.png', dpi=100)
# fig.set_canvas(self)
# set the spacing between subplots
plt.subplots_adjust(left=0.07, bottom=0.06, right=0.99,
                    top=0.9, wspace=0.4, hspace=0.4)
time_plot = plt.subplot(211)
plt.plot(data_amplitude)
time_plot.title.set_text("Time")
plt.grid()

feq_plot = plt.subplot(212)
plt.plot(data_fequency, data_amplitude)
feq_plot.title.set_text("Frequency")
plt.grid()


plt.show()
