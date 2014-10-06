#!/bin/bash
#Derived from script @ http://www.linuxjournal.com/content/temper-pi
#script provided "as-is" with no guarantees.

FORMAT="JSON" #Formats: RAW | JSON
TEMP_MIN="32"
TEMP_MAX="99"

LOGFILE='/var/log/temper.json'
TIME=`date +"%b %d %T"`
TEMPERATURE=`/usr/local/bin/temper-poll 2>/dev/null | tail -n1 | cut -f4 -d ' ' | sed 's/.F$//'`

STATUS='ERROR'
if [[ $TEMPERATURE == "" ]]; then

	if [[ $FORMAT ==  "RAW" ]]; then
		echo  -e "$TIME\t$TEMPERATURE\t$STATUS" >> $LOGFILE
	elif [[ $FORMAT == "JSON" ]]; then
		echo -e "{'timestamp':'$TIME','value':'$TEMPERATURE','status':'$STATUS'}" >> $LOGFILE
	fi
  exit 1
fi


STATUS='NORMAL'
if [[ $TEMPERATURE < $TEMP_MIN ]]; then  #too cold
	STATUS='COLD'
elif [[ $TEMPERATURE > $TEMP_MAX ]]; then #too hot
	STATUS='HOT'
fi

if [[ $FORMAT == 'RAW' ]]; then
	echo -e "$TIME\t$TEMPERATURE\t$STATUS" >> $LOGFILE
elif [[ $FORMAT == 'JSON' ]]; then
	echo -e "{'timestamp':'$TIME','value':'$TEMPERATURE','status':'$STATUS'}" >> $LOGFILE
fi

exit 0
