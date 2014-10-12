#!/usr/bin/python
#script provided "as-is" with no guarantees.
import sys, datetime

now = datetime.datetime.now()

try:
    temp_value = int(sys.argv[1])
except:
    temp_value = None

try:
    temp_unit = (sys.argv[2])
except:
    temp_unit = 'F'
    
try:
    log_format = sys.argv[3]
except:
    log_format = 'RAW'

temp_min=32
temp_max=99

logfile='C:/temp/test.json'


status='ERROR'
#if temp_check is None:

def write_log(timestamp, temp_value, temp_unit):
    timestamp = str(timestamp)
    temp_value = str(temp_value)
    f = open(logfile,'a')
    if log_format == 'JSON':
        f.write("{'timestamp':'" + timestamp + "','temp_value':'" + temp_value + "','temp_unit':'" + temp_unit + "'}\r\n")
    else:
        f.write(timestamp + '\t' + temp_value + '\t' + temp_unit + '\r\n')
    
write_log(now, temp_value, temp_unit)

def check_temp(temp_value):
    if temp_value > temp_max:
        print("too hot")
    elif temp_value < temp_min:
        print("too cold")
    else:
        print("normal")

check_temp(temp_value)
