python-temp-sensor
===============================

Dependency on work @ https://github.com/padelt/temper-python
You will need to clone this repo and run install process before you continue.

**settings.py**

	Edit to configure logfile, notifications, temp sensor settings, and etc.

**Run as Cron Jobs**

	sudo crontab -e
	#as root add these lines: 	
	*/5 * * * * sudo /path/to/repo/cron-run-interval.sh
	@reboot sudo /path/to/repo/cron-run-reboot.sh

***FYI***
	cron-run-interval.sh: Set Cron frequency to how often you want to check temp, log, and check to send interval notifications.
	cron-run-reboot.sh: Set to re-initiate process on reboot, notifies users device may have restarted (power loss).

It's recommended to use **cron-run-interval.sh** as part of a minute-ly (x) cron job and **cron-run-reboot.sh** as part of a reboot (on-startup) cron job.

