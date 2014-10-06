#!/bin/bash
#Derived from script @ http://www.linuxjournal.com/content/temper-pi
#script provided "as-is" with no guarantees.

TEMP_MIN="32"
TEMP_MAX="99"

LOGFILE='/var/log/temper.log'
TIME=`date +"%b %d %T"`
TEMPERATURE=`temper-poll 2>/dev/null | tail -n1 | cut -f4 -d ' ' | sed 's/.F$//'`

if [[ $TEMPERATURE == "" ]]; then
  echo ERROR
  exit 1
fi

if [[ $TEMPERATURE < $TEMP_MIN ]]; then  #too cold
  echo -e "$TIME\t$TEMPERATURE\tCOLD" >> $LOGFILE
  exit 0
elif [[ $TEMPERATURE > $TEMP_MAX ]]; then #too hot
  echo -e "$TIME\t$TEMPERATURE\tHOT" >> $LOGFILE
  exit 0
fi
echo -e "$TIME\t$TEMPERATURE\tNormal" >> $LOGFILE
exit 0
