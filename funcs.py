import os, sys, ConfigParser, datetime, time, smtplib
#from dateutil.parser import *

_now = datetime.datetime.now()

app_path = os.path.dirname(os.path.realpath(__file__))
app_config = ConfigParser.RawConfigParser()
app_config.read(app_path + '/settings.cfg')
app_mode = 'Debug' if app_config.get('production', 'debug_mode').lower()=='true' else 'Production'

def waited_long_enough(wait_hours, last_datestamp_file):
    def read_last_notice():
        try:
            with open(last_datestamp_file, "r") as f:
                return datetime.datetime.fromtimestamp(float(str(f.readline()).strip())) #read in timestamp format.
        except:
            pass
        return None

    def write_last_notice():
        try:
            with open(last_datestamp_file, "w") as f:
                f.write(str(time.mktime(_now.timetuple()))) #timestamp format, easier to read.
                f.truncate()                                    
        except:
            pass

    #figure out last timestamp
    last_notice = read_last_notice()
    if(last_notice is None):
        write_last_notice()

    last_notice = read_last_notice()
    
    if(last_notice is None): #unable to figure out last timestamp.
        send_notice_message("Error", 'unable to read last_error_notice.dat and figure out last time notification has been sent.')
        return True
    
    duration = _now - last_notice
    #return True
    if((duration.total_seconds()/60/60)>wait_hours): #after x hrs, have waited long enough.
        write_last_notice()
        return True
    else:
        return False

def handle_error(message):
                
    with open(app_path + '/errors.log', "a") as f:
        f.write(str(_now) + '\t' + message + '\t' + app_mode + '\r\n')
    
    def send_notice_error(message):
        send_notice_message("Error", message)

    if(waited_long_enough(int(app_config.get('notifications','error_wait_hours')), app_path + '/last_error_notice.dat')):
        send_notice_message("Error", message)

def write_log_data(temp_value, temp_unit):
    timestamp = str(_now)
    temp_value = str(temp_value)
    
    try:
        log_format = app_config.get('logs', 'data_format')
    except:
        log_format = 'RAW'

    file_path = app_config.get('logs', 'data_directory')
    if(file_path[0] != '/'):
        file_path = app_path + "/" + file_path

    if log_format == 'JSON':
        row = "{'timestamp':'" + timestamp + "','temp_value':'" + temp_value + "','temp_unit':'" + temp_unit + "'}\r\n"
    else:
        row = timestamp + '\t' + temp_value + '\t' + temp_unit + '\r\n'

    if(app_mode == 'Debug'):
        print("Sending data to console instead of data file.")
        print(row)
        return
	
    with open(file_path + "/" + str(_now.year) + "-" + str(_now.month) + "-" + str(_now.day) + "." + log_format + ".dat" , "a") as f:        
        f.write(row)
        
def check_temp(temp_value):
    try:
        temp_min = int(app_config.get('temp_sensor', 'temp_min'))
        temp_max = int(app_config.get('temp_sensor', 'temp_max'))
    except:
        handle_error(_now, 'unable to read temp_min and/or temp_max from settings.cfg file.')

    status = "Temp Ok"
    if temp_value > temp_max:
        status = "Too Hot"
    elif temp_value < temp_min:
        status = "Too Cold"

    send_notice_message(status, "The current temp reading is: " + str(temp_value))
    
def send_notice_message(subject, message):
    print(subject + ": " + message)
    if(app_mode == 'Debug'):
        print("Halted sending via email due to Debug mode.")
        return
    
    session = smtplib.SMTP(app_config.get('notification_from', 'mail_server_smtp'), app_config.get('notification_from', 'mail_server_smtp_port'))
    session.ehlo()
    session.starttls()
    session.login(app_config.get('notification_from', 'mail_username'), app_config.get('notification_from', 'mail_password'))

    headers = "\r\n".join(["from: " + app_config.get('notification_from', 'mail_username'),
                           "subject: Message from Temp Sensor: " + app_config.get('temp_sensor', 'sensor_name') +  " " + subject,
                           "to: " + app_config.get('notification_to', 'mail_recipients'),
                           "mime-version: 1.0",
                           "content-type: text/html"])

    # body_of_email can be plaintext or html!                    
    content = headers + "\r\n\r\n" + message
    session.sendmail(app_config.get('notification_from', 'mail_username'), app_config.get('notification_to', 'mail_recipients'), content)
