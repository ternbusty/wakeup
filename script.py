from crontab import CronTab
from datetime import datetime, timedelta
import webiopi
import time

webiopi.setDebug()

def setup():
    webiopi.debug("Script with macros - Setup")

def loop():
    webiopi.sleep(5)

def destroy():
    webiopi.debug("Script with macros - Destroy")

def createNewCron(myCron, execDate, comment):
    job = myCron.new(command='python /usr/share/webiopi/htdocs/wakeup/rotate.py ' + comment, comment=comment)
    job.setall(execDate)
    myCron.write()

@webiopi.macro
def updateCron(dataStr):
	hour = int(dataStr.split(":")[0])
	minute = int(dataStr.split(":")[1])
	now = datetime.now()
	lockDate = datetime(now.year, now.month, now.day, hour, minute)
	if lockDate < now:
	    lockDate = lockDate + timedelta(days=1)
	unlockDate = lockDate + timedelta(hours=3)
	myCron = CronTab(user='pi')
	for (execDate, comment) in zip([lockDate, unlockDate], ['lock', 'unlock']): 
		for job in myCron:
		    if job.comment == comment:
		        job.setall(execDate)
		        myCron.write()
		        break
		else:
			createNewCron(myCron, execDate, comment)

@webiopi.macro
def clearCron():
	myCron = CronTab(user='pi')
	for job in myCron:
	    if job.comment in ['lock', 'unlock']:
	        myCron.remove(job)
	        myCron.write()

@webiopi.macro
def getCurrentSetting():
	myCron = CronTab(user='pi')
	for job in myCron:
		if job.comment == 'lock': 
			strJob = str(job)
			minute = strJob.split(" ")[0].zfill(2)
			hour = strJob.split(" ")[1].zfill(2)
			return(hour + ':' + minute)
			break
	else:
		return('')


