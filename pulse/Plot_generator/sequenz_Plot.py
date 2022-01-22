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

puls = [5, 2, 10]
offset = [20, 10, 5]
delay = 11
window = 20
rest = 10  # end of puls

duration = []

for count, value in enumerate(puls):
    duration.extend([0 for i in range(0, offset[count])])
    duration.extend([1 for i in range(0, puls[count])])

duration.extend([0 for i in range(0, delay)])
duration.extend([1 for i in range(0, window)])
duration.extend([0 for i in range(0, rest)])

amplitude = 1
frequency = 100
start_time = 0
end_time = len(duration)
sample_rate = 100

time = np.arange(start_time, end_time, 1/sample_rate)

sinus = amplitude * np.sin(2 * np.pi * frequency * time)
#sinus = sinus * np.repeat(duration, sample_rate)


print("duration", duration)
print("time", time)
print("sinus", sinus)


#data = [0, 0, 0, 1, 1, 0, 1, 0]
x_puls = np.repeat(range(len(duration)), 2)
time = np.repeat(duration, 2)
x_puls = x_puls[1:]
time = time[:-1]
x_puls = np.append(x_puls, x_puls[-1] + 1)
time = np.append(time, time[-1])

#plt.plot(x_puls, time)
plt.plot(x_puls, time)
#plt.ylim(-0.5, 1.5)
plt.show()
