# Creates a Plot of Voltage and current over time 
import re
import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime
import sys
import json
import time

elapsed_time = []
voltages = []
currents = []
level = []
timestamps = []

def plot(x = timestamps, y = currents, x_is_date = False):
    plt.gcf().clear()
    if x_is_date:
        plt.plot_date(x, y, 'g')
    else:
        plt.plot(x, y, 'g')
    plt.xlabel('Time')
    # plt.ylabel('Current (mA)')
    # plt.pause(0.0001)
    # plt.show(block = freeze)

def plot_all():
    plt.gcf().clear()

    plt.subplot(2, 2, 1)
    plt.ylabel('Current (mA)')
    plt.plot_date(timestamps, currents, 'g')

    plt.subplot(2, 2, 2)
    plt.ylabel('Voltage (mA)')
    plt.plot_date(timestamps, voltages, 'g')

    plt.subplot(2, 2, 3)
    plt.ylabel('Battery Level (%)')
    plt.plot_date(timestamps, level, 'g')

    plt.pause(0.0001)
    plt.show(block=False)

def add_datapoint(line):
    data = json.loads(line)
    elapsed_time.append(data[0])
    voltages.append(data[1])
    currents.append(data[2])
    level.append(data[3])
    timestamps.append(datetime.strptime(data[4].strip('"'), '%H:%M:%S.%f'))

file = open(sys.argv[1], 'r')
# Initially, load all the file contents into arrays
for line in file:
    add_datapoint(line)

# determine what to plot
xdata = elapsed_time
ydata = currents
if len(sys.argv) > 2:
    y_val = sys.argv[2]
    if y_val == 'voltage':
        ydata = voltages
    elif y_val == 'current':
        ydata = currents
    elif y_val == 'level':
        ydata = level

    x_val = sys.argv[3]
    date = False
    if x_val == 'elapsed':
        xdata = elapsed_time
    elif x_val == 'time':
        xdata = timestamps
        date = True

    # Initial plot (freeze window)
    plot(xdata, ydata, True, date)


plot_all()
# waiting for more input
exit_counter = 0
while(1):
    if exit_counter > 300:
        break
    
    line = file.readline()
    if not line:
        time.sleep(0.1)
        exit_counter+= 1
    else:
        exit_counter = 0
        add_datapoint(line)
        plot_all()