# Creates a Plot of Voltage and current over time 
import re
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime
import sys
import json
import time
import argparse
import numpy

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--continuous', action='store_true', required=False)
parser.add_argument('-b', '--best-fit-enabled', action='store_true', required=False)
parser.add_argument('-s', '--single-plot', required=False, nargs=2)
parser.add_argument('-t', '--title', required=False, default='')
parser.add_argument('-m', '--markers', required=False, action='store_true')
parser.add_argument('-i', '--interval', required=False, type=int, default=10)
parser.add_argument('file')
args = parser.parse_args()

elapsed_time = []
voltages = []
currents = []
level = []
timestamps = []


# Returns times and levels at the point when the batter level changes (makes for a smoother graph)
def unique_battery_levels(time, level):
    unique_times = [time[0]]
    unique_levels = [level[0]]

    last_level = level[0]
    for i in range(len(level)):
        if level[i] != last_level:
            unique_times.append(time[i])
            unique_levels.append(level[i])
            last_level = level[i]

    return (unique_times, unique_levels)


def plot(x, y, ylabel, x_is_date = False, best_fit = False):
    plt.gcf().clear()
    if args.markers:
        style = 'bo-'
    else:
        style = 'b'
    plt.plot(x, y, style, markersize = 4,linewidth = 1)
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.grid(True, linestyle = 'dotted', linewidth = '1')
    plt.title(args.title)

    if x_is_date:
        plt.gcf().autofmt_xdate()
        fmt = matplotlib.dates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=args.interval))
        plt.gca().xaxis.set_major_formatter(fmt)
    if best_fit:
        if x_is_date:
            start_time = x[0]
            elapsed_sec = list(map(lambda el: (el - start_time).seconds, x))
        else:
            elapsed_sec = x
        coeffs = numpy.polyfit(elapsed_sec, y, 1)
        print('y =', coeffs[0], 'x +', coeffs[1])
        y_vals = list(map(lambda el: el * coeffs[0] + coeffs[1], elapsed_sec))
        plt.plot(x, y_vals, 'r', linewidth = 1)

    plt.pause(0.0001)
    plt.show(block = True)


def plot_all(freeze = False):
    plt.gcf().clear()

    plt.subplot(2, 2, 1)
    plt.ylabel('Current (mA)')
    plt.xlabel('Time')
    plt.plot_date(timestamps, currents, 'g')

    plt.subplot(2, 2, 2)
    plt.ylabel('Voltage (mA)')
    plt.xlabel('Time')
    plt.plot_date(timestamps, voltages, 'b')

    plt.subplot(2, 2, 3)
    plt.ylabel('Battery Level (%)')
    plt.xlabel('Time')
    x, y = unique_battery_levels(timestamps, level)
    plt.plot_date(x, y, 'r')

    plt.pause(0.0001)
    plt.show(block=freeze)

def add_datapoint(line):
    data = json.loads(line)
    elapsed_time.append(data[0])
    voltages.append(data[1])
    currents.append(data[2])
    level.append(data[3])
    timestamps.append(datetime.strptime(data[4].strip('"'), '%H:%M:%S.%f'))


file = open(args.file, 'r')
# Initially, load all the file contents into arrays
for line in file:
    add_datapoint(line)

# Find which plot to show (default is all the plots)
if args.single_plot == None:
    plot_all(not args.continuous)
else:
    x_val = args.single_plot[1]
    date = False
    if x_val == 'elapsed':
        xdata = elapsed_time
    elif x_val == 'time':
        xdata = timestamps
        date = True

    y_val = args.single_plot[0]
    y_label = 'Unknown'
    if y_val == 'voltage':
        ydata = voltages
        y_label = 'Voltage (mV)'
    elif y_val == 'current':
        ydata = currents
        y_label = 'Current (mA)'
    elif y_val == 'level':
        xdata, ydata = unique_battery_levels(xdata, level)
        y_label = 'Battery Level (%)'

    plot(xdata, ydata, y_label, date, args.best_fit_enabled)


if args.continuous:
    # waiting for more input
    print('continuous mode')
    quit_counter = 0
    while(quit_counter < 300):
        line = file.readline()
        if not line:
            time.sleep(0.1)
            quit_counter += 1
        else:
            quit_counter = 0
            add_datapoint(line)
            plot_all(False)

print('Ended program')

# # determine what to plot
# xdata = elapsed_time
# ydata = currents
# if len(sys.argv) > 2:
#     y_val = sys.argv[2]
#     if y_val == 'voltage':
#         ydata = voltages
#     elif y_val == 'current':
#         ydata = currents
#     elif y_val == 'level':
#         ydata = level

#     x_val = sys.argv[3]
#     date = False
#     if x_val == 'elapsed':
#         xdata = elapsed_time
#     elif x_val == 'time':
#         xdata = timestamps
#         date = True

#     # Initial plot (freeze window)
#     plot(xdata, ydata, True, date)