# Creates a Plot of Voltage and current over time 
import re
import matplotlib.pyplot as plt
import sys
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--continuous', action='store_true', required=False)
parser.add_argument('file', nargs=1)
args = parser.parse_args()

timestamps = []
voltages = []
currents = []

def plot(freeze=False):
  plt.gcf().clear()
  plt.plot(timestamps, currents, 'g')
  plt.xlabel('Time Elapsed (s)')
  plt.ylabel('Current (mA)')
  plt.pause(0.0001)
  plt.show(block=freeze)

def add_datapoint(line):
    data = json.loads(line)
    timestamps.append(data[0])
    voltages.append(data[1])
    currents.append(data[2])

file = open(sys.argv[1], 'r')
# Initially, load all the file contents into arrays
for line in file:
    add_datapoint(line)

if args.continuous:
    # waiting for more input
    quit_counter = 0
    while(quit_counter < 500):
        line = file.readline()
        if not line:
            time.sleep(0.1)
            quit_counter++
        else:
            quit_counter = 0
            add_datapoint(line)
            plot()
else:
    plot(True)

print('Ended program')