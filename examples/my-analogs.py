#!/usr/bin/env python

# File: my-analogs.py based on the pimorini sensor.py
# david Torrens March 10th 2020
# original Author; James Carlson, https://github.com/jxxcarlson
# Date: Feb 21, 2016
# Derived from code by Gisky

import time
from math import sqrt

import explorerhat

from datetime import datetime

# Local application imports
from utility import pr,make_time_text,send_by_ftp
from text_buffer import class_text_buffer
from config import class_config

config = class_config()

headings = ["Date_time","Time Step","Ch1","Ch2","ac","AC_Max","currents RMS","Current"]
analog_buffer = class_text_buffer(headings,config)


delay = 2
rc_max = 200
reading = [0.0]*(rc_max + 1)
reading_ac = [0.0]*(rc_max + 1)
reading_square_total = [0.0]*(rc_max + 1)
reading_ac_max = [0.0]*(rc_max + 1)
current_rms = [0.0]*(rc_max + 1)
current = [0.0]*(rc_max + 1)
reading_time = [0.0]*(rc_max + 1)
time_step = [0.0]*(rc_max + 1)



reference = explorerhat.analog.one.read()
rc = 0
print(reference)

not_finished = True

start_time = datetime.now()
while not_finished:
	reading[rc] = explorerhat.analog.two.read() 
	reading_time[rc] = 1000*(datetime.now() - start_time).total_seconds()
	if (reading_time[rc] >= 1000) or (rc >= rc_max):
		not_finished = False
	else:
		rc +=1
end_time = datetime.now()

rc_max = rc

reference = (reference + explorerhat.analog.one.read())/2

print( reference)


read_time = (end_time - start_time).total_seconds()

for rc in range(0,rc_max+1,1):
	if rc >=1:
		reading_ac[rc] = abs(reading[rc]-reference)
		if abs(reading_ac[rc])>reading_ac_max[rc-1]:
			reading_ac_max[rc] = abs(reading_ac[rc])
		else:
			reading_ac_max[rc] = reading_ac_max[rc-1]
		#time_step[rc] = 1000*(reading_time[rc]- reading_time[rc-1]).total_seconds()
		reading_square_total[rc] = reading_square_total[rc-1] + (reading_ac[rc] * reading_ac[rc])
		current_rms[rc] =  20.826*sqrt(reading_square_total[rc]/rc)
		current[rc] = 14.598 * reading_ac_max[rc]

	analog_buffer.line_values[0] = str(reading_time[rc])
	analog_buffer.line_values[1] = "not used"
	analog_buffer.line_values[2] = "not used" #str(reference)
	analog_buffer.line_values[3] = str(reading[rc])
	analog_buffer.line_values[4] = str(reading_ac[rc])
	analog_buffer.line_values[5] = str(reading_ac_max[rc])
	analog_buffer.line_values[6] = str(current_rms[rc])
	analog_buffer.line_values[7] = str(current[rc])
	analog_buffer.just_log(True,0,reading_time[rc],1234)

end_file_time = datetime.now()

file_time = (end_file_time - end_time).total_seconds()

print("Read Time",read_time)
print("File Time",file_time)
