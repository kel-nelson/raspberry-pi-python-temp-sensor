#!/usr/bin/python
#script provided "as-is" with no guarantees.
import os, sys, datetime, configparser
from funcs import *

print('Runmode: ' + app_mode)
try:
    temp_value = int(sys.argv[1])
except:
    temp_value = None

try:
    temp_unit = (sys.argv[2])
except:
    temp_unit = 'F'

try:
    write_log_data(int(temp_value), temp_unit)
except:
    handle_error('unable to read temp value.')
    sys.exit()

if(waited_long_enough(int(app_config.get('notifications','report_wait_hours')), app_path + '/last_report_notice.dat')):
    check_temp(int(temp_value))

