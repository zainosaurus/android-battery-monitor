# Creates a Plot of Voltage and current over time 
import re
import matplotlib.pyplot as plt
import sys
import json
import time

timestamps = []
voltages = []
currents = []

def plot():
  plt.gcf().clear()
  plt.plot(timestamps, currents, 'g')
  plt.xlabel('Time Elapsed (s)')
  plt.ylabel('Current (mA)')
  plt.pause(0.0001)
  plt.show(block=False)

def add_datapoint(line):
    data = json.loads(line)
    timestamps.append(data[0])
    voltages.append(data[1])
    currents.append(data[2])

file = open(sys.argv[1], 'r')
# Initially, load all the file contents into arrays
for line in file:
    add_datapoint(line)

plot()
# waiting for more input
while(1):
    line = file.readline()
    if not line:
        time.sleep(0.1)
    else:
        add_datapoint(line)
        plot()