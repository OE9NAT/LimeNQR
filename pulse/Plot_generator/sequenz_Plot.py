import matplotlib.pyplot as plt
import numpy as np


def my_lines(ax, pos, *args, **kwargs):
    if ax == 'x':
        for p in pos:
            plt.axvline(p, *args, **kwargs)
    else:
        for p in pos:
            plt.axhline(p, *args, **kwargs)


# bits = [0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0]
# data = np.repeat(bits, 2)
# clock = 1 - np.arange(len(data)) % 2
# manchester = 1 - np.logical_xor(clock, data)
# t = 0.5 * np.arange(len(data))
#
# # plt.hold(True)
# my_lines('x', range(13), color='.5', linewidth=2)
# my_lines('y', [0.5, 2, 4], color='.5', linewidth=2)
# plt.step(t, clock + 4, 'r', linewidth=2, where='post')
# plt.step(t, data + 2, 'r', linewidth=2, where='post')
# #plt.step(t, manchester, 'r', linewidth=2, where='post')
# plt.ylim([-1, 6])
#
# for tbit, bit in enumerate(bits):
#     plt.text(tbit + 0.5, 1.5, str(bit))
#
# # plt.gca().axis('off')
# plt.show()

puls = [5, 2, 10, 8]
offset = [20, 10, 5, 8]
delay = 11
window = 20
rest = 10  # end of puls

duration = []
duration_list = []

for count, value in enumerate(puls):
    duration.extend([0 for i in range(0, offset[count])])
    duration.extend([1 for i in range(0, puls[count])])
    duration_list.append(offset[count])
    duration_list.append(puls[count])

delay_start = len(duration)
duration.extend([0 for i in range(0, delay)])

window_start = len(duration)
duration.extend([1 for i in range(0, window)])
duration.extend([0 for i in range(0, rest)])

amplitude = 1
frequency = 10000
start_time = 0
end_time = len(duration)
sample_rate = 1000

time = np.arange(start_time, end_time, 1/sample_rate)


start_time = time[0]
end_time = time[-1]
time = np.arange(start_time, end_time, 1/sample_rate)
print(start_time, "end_time", end_time)

sinus = amplitude * np.sin(2 * np.pi * frequency * time)
sinus = amplitude * np.sin(2 * np.pi * time)
# sinus = sinus * np.repeat(duration, sample_rate)


x_puls = np.repeat(range(len(duration)), sample_rate)
y_puls = np.repeat(duration, sample_rate)
x_puls = x_puls[1:]
y_puls = y_puls[:-1]
x_puls = np.append(x_puls, x_puls[-1] + 1)
y_puls = np.append(y_puls, y_puls[-1])

time = np.append(time, time[-1]).tolist()
sinus = np.append(sinus, sinus[-1]).tolist()

sinus_puls = [sinus[count] if value ==
              1 else 0 for count, value in enumerate(y_puls)]


# with dampend responce
print("window_start,", window_start*sample_rate)
window_start_upsample = window_start*sample_rate

sinus_puls = [sinus_puls[count] * (np.exp(-(count-window_start_upsample-200)*0.0001)) if count >
              window_start_upsample else sinus_puls[count] for count, value in enumerate(sinus_puls)]


print(len(x_puls), "x_puls", x_puls[0: 15])
print(len(y_puls), "y_puls", y_puls[0: 15])
print(len(sinus_puls), "sinus_puls \n", sinus_puls[0: 5])
print(len(time), "time \n", time[0: 5])


# plt.plot(sinus, 'ro')
plt.plot(time, sinus_puls)
plt.plot(x_puls, y_puls)

# left, right or center,
# plt.text(window_start, 1, 'Window', horizontalalignment='right')

# plt.annotate(label, # this is the text
#                  (x,y), # these are the coordinates to position the label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center') # horizontal alignment can be left, right or center

off_bool = True
point_summ = 0
for count, point in enumerate(duration_list):
    if off_bool:
        plt.annotate('Offset '+str(int(count/2+1)), (point_summ, 1),
                     textcoords="offset points", xytext=(10, -20), ha='left')
        off_bool = False
    else:
        plt.annotate('Puls '+str(int((count+1)/2)), (point_summ, 1),
                     textcoords="offset points", xytext=(10, 10), ha='left')
        off_bool = True
    point_summ += point

plt.annotate('Delay', (point_summ, 1),
             textcoords="offset points", xytext=(10, -20), ha='left')
plt.annotate('Window', (window_start, 1),
             textcoords="offset points", xytext=(10, 10), ha='left')


plt.ylim(-1.2, 1.7)
plt.title("Sequenz of Pulssequenz")
plt.xlabel("Time in ms")
plt.ylabel("Amplitude")

plt.savefig('plot.jpg', dpi=300)

plt.show()
