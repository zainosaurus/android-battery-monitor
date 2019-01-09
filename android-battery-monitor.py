# This Script Uses adb commands to poll the status of the phone battery.
# It then uses matplotlib to plot the voltage and current over time.

import subprocess
import re
import sys
import json

import time
import matplotlib.pyplot as plt

DELAY = 2
VOLTAGE_STR = r'^ *voltage: (\d+)'
CURRENT_STR = r'^ *current now: (-?\d+)'
BATTERY_LEVEL = r'^ *level: (\d+)'

# def replot(x_data, c_data, v_data):
# 	plt.gcf().clear()
# 	plt.plot(x_data, c_data, 'g')
# 	plt.xlabel('Time Elapsed (s)')
# 	plt.ylabel('Current (mA)')
# 	plt.pause(0.0001)
# 	plt.show(block=False)

# Holds plot data
timestamps = []
voltages = []
currents = []

battery_setpoint = 100
if len(sys.argv) > 2 :
	battery_setpoint = int(sys.argv[2])

logged_time = 0
while (True):
	start_time = time.time()
	# Get battery info by using a system call
	battery_stats = subprocess.check_output(['adb', '-s', sys.argv[1], 'shell', 'dumpsys', 'battery']).decode('utf-8')
	
	# Find info to write to file (relevant batter stats)
	voltage = float(re.search(VOLTAGE_STR, battery_stats, re.MULTILINE).group(1))
	current = float(re.search(CURRENT_STR, battery_stats, re.MULTILINE).group(1))
	battery_level = float(re.search(BATTERY_LEVEL, battery_stats, re.MULTILINE).group(1))

	# Break if desired battery level is reached
	if battery_level >= battery_setpoint:
		break

	# Ensure loop runs at specified intervals
	elapsed_time = time.time() - start_time
	time.sleep(DELAY - elapsed_time)
	logged_time += DELAY

	# print output to stdout as json
	f = open('datafile.json', 'a')
	f.write(','.join([str(logged_time), str(voltage), str(current)]))

f.close()


	# battery_stat = list(map(lambda el: el.strip(), battery_stat.split('\n')))

	# timestamps.append(cur_time)
	# # Find voltage and current & push to array
	# for element in battery_stat:
	# 	v = re.match(r'voltage: *(\d+)', element)
	# 	c = re.match(r'current now: *(-?\d+)', element)

	# 	if v != None:
	# 		voltage = v.group(1)
	# 		voltages.append(float(voltage))
	# 	elif c != None:
	# 		current = c.group(1)
	# 		currents.append(float(current))
	# # print(timestamps, currents, voltages)
	# # print(str(cur_time) + '\t\t' + str(voltage) + '\t\t' + str(current))
	# replot(timestamps, currents, voltages)
	# cur_time += DELAY
	# time.sleep(DELAY)


