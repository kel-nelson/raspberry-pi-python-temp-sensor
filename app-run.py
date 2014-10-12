#!/usr/bin/python
#script provided "as-is" with no guarantees.
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

if(waited_long_enough(int(app_config.get('notifications','report_wait_hours')), app_path + '/last_report_notice.dat')):
    check_temp(float(temp_value))

