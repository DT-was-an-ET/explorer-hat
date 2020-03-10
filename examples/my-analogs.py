#!/usr/bin/env python

# File: my-analogs.py based on the pimorini sensor.py
# david Torrens March 10th 2020
# original Author; James Carlson, https://github.com/jxxcarlson
# Date: Feb 21, 2016
# Derived from code by Gisky

import time

import explorerhat

from datetime import datetime

# Local application imports
from utility import pr,make_time_text,send_by_ftp
from text_buffer import class_text_buffer
from config import class_config

config = class_config()

headings = ["Date_time","Time Diff","Reading","Average","ac","AC_Max","Current"]
analog_buffer = class_text_buffer(headings,config)


delay = 2
rc_max = 1000
reading = [0.0]*(rc_max + 1)
reading_average = [2.475]*(rc_max + 1)
reading_ac = [0.0]*(rc_max + 1)
reading_ac_max = [0.0]*(rc_max + 1)
current = [0.0]*(rc_max + 1)
reading_time = [datetime.now()]*(rc_max + 1)

start_time = datetime.now()

for rc in range(1,rc_max,1):
	reading[rc] = explorerhat.analog.one.read()
	reading_time[rc] = datetime.now()

end_time = datetime.now()

read_time = (end_time - start_time).total_seconds()

for rc in range(0,rc_max,1):
	if rc >=1:
		reading_average[rc] = reading_average[rc-1] + 0.05*(reading[rc] - reading_average[rc-1])
		reading_ac[rc] = abs(reading[rc]- reading_average[rc])
		if reading_ac[rc]>reading_ac_max[rc-1]:
			reading_ac_max[rc] = reading_ac[rc]
		else:
			if reading_ac_max[rc-1]>0.001: 
				reading_ac_max[rc] = reading_ac_max[rc-1] - 0.001
			elif reading_ac_max[rc-1] <= 0.001:
				reading_ac_max[rc] = 0
		current[rc] = 15.686 * reading_ac_max[rc]

	analog_buffer.line_values[0] = make_time_text(reading_time[rc])
	analog_buffer.line_values[1] = str((reading_time[rc]- reading_time[rc-1]).total_seconds())
	analog_buffer.line_values[2] = str(reading[rc])
	analog_buffer.line_values[3] = str(reading_average[rc])
	analog_buffer.line_values[4] = str(reading_ac[rc])
	analog_buffer.line_values[5] = str(reading_ac_max[rc])
	analog_buffer.line_values[6] = str(current[rc])
	analog_buffer.just_log(True,0,reading_time[rc],1234)

end_file_time = datetime.now()

file_time = (end_file_time - end_time).total_seconds()

print("Read Time",read_time)
print("File Time",file_time)
