#!/usr/bin/python
import os, sys, datetime, ConfigParser
from funcs import *

print('Runmode: ' + app_mode)
try:
    temp_value = float(sys.argv[1])
except:
    temp_value = None

try:
    temp_unit = (sys.argv[2])
except:
    temp_unit = 'F'

try:
    write_log_data(float(temp_value), temp_unit)
except:
    handle_error('unable to read temp value.')
    sys.exit()

waited_long_enough_hourly_value = waited_long_enough(int(app_config.get('notifications','report_wait_hours')), app_path + '/notices/last_report_hourly_notice.dat') 
waited_long_enough_daily_value = waited_long_enough(24, app_path + '/notices/last_report_daily_notice.dat')
if(waited_long_enough_hourly_value in (1,2) or waited_long_enough_daily_value != 0):
    temp_status_code = get_temp_status_code(float(temp_value))
    temp_status_text = get_temp_status_code_text(temp_status_code)
    message = "The current temp reading is: " + str(temp_value)
    
    if(waited_long_enough_hourly_value == 2):  #first run init
        send_notice_message("[Device Initialized] " + temp_status_text, message + "\r\nThis appears to be the first initialization run, this device may have just recovered from a reboot.")
    elif(waited_long_enough_daily_value != 0):
        send_notice_message("[Device Daily] " + temp_status_text, message + "\r\nDevice reporting in for daily check-in.")        
    elif(temp_status_code != 0): #hourly: not normal temp
        send_notice_message("[Device Hourly (!)] " + temp_status_text, message)
        