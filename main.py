"""
stores how much I spent time on PC in a log file (CAN) DONE
every 30 minutes it gives notification to get off of my chair and do eye exercise (CAN) DONE
and dims the whole screen to 0% brightness for 30 seconds (CAN) DONE
every 1 hour it gives notification of the screentime (CAN) NO
logs previous screentimes(CAN) DONE
everytime I boot up my PC, it will give notification of how much time I spent off of PC (CAN) DONE
the software runs on boot (CAN)
"""


# # # import psutil
# # # from datetime import datetime
# # # time = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
# # # print(time)
# # # # from subprocess import call
# # # # test = call( ["powershell", "-command", "(gcim Win32_OperatingSystem).LastBootUpTime"] )

# # # # print(test)

# # # importing the module
# # import screen_brightness_control as sbc
 
# # # get current brightness  value
# # current_brightness = sbc.get_brightness()
# # print(current_brightness)
 
# # # get the brightness of the primary display
# # primary_brightness = sbc.get_brightness(display=0)
# # print(primary_brightness)

# # importing the module
# import screen_brightness_control as sbc
 
# # get current brightness value
# print(sbc.get_brightness())
 
# #set brightness to 50%
# sbc.set_brightness(0)
 
# print(sbc.get_brightness())
 
import os
from plyer import notification
import asyncio
import screen_brightness_control as sbc
import psutil
from datetime import datetime, date
import sqlite3

conn = sqlite3.connect('db.db')

c = conn.cursor()


def monthToNum(name):
    num =  {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9, 
            'October': 10,
            'November': 11,
            'December': 12
    }[name]
    return str(num)

    

"""
Function to show the time the user was away
"""
async def time_off():
	shut_time = os.popen('powershell.exe Get-WinEvent  -FilterHashtable  @{logname = ‘System’; id = 1074}').read()
	shut_time = shut_time.split('\n')[6][0:22]
	if len(shut_time.split(' ')) == 4:
		only_date, only_time, am_pm, none = shut_time.split(' ')
	else:
		only_date, only_time, am_pm, none, none1 = shut_time.split(' ')


	boot_time = os.popen('powershell.exe (gcim Win32_OperatingSystem).LastBootUpTime').read()
	boot_time = boot_time.split('\n')[1]

	day, month, day_num, year, only_time1, am_pm1 = boot_time.split(' ')
	day = day[:-1]
	day_num = day_num[:-1]
	month = monthToNum(month)
	only_date1 = f"{month}/{day_num}/{year}"


	boot_time = f"{only_date1} {only_time1} {am_pm1}"
	shut_time = f"{only_date} {only_time} {am_pm}"

	off_time = datetime.strptime(boot_time, '%m/%d/%Y %I:%M:%S %p') - datetime.strptime(shut_time, '%m/%d/%Y %I:%M:%S %p')
	final = f"You were away for: {off_time}"

	notification.notify(
				title = "Off time",
				message = final
			)
	

 

"""
Function to show notification to get off my chair and do eye exercise and dim the screen's brightness to 20 (every 30 minutes)
"""
async def notification_brightness():
	while True:
		await asyncio.sleep(1800)

		notification.notify(
				title = "Reminder",
				message = "Don't forget to take a break, and do eye exercises"
			)

		prev = (sbc.get_brightness())
		sbc.set_brightness(20)

		await asyncio.sleep(30)

		sbc.set_brightness(prev)

		


"""
Function to log the time spent on PC
"""
async def logs():
	while True:
		time = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
		time = time.total_seconds()

		today = date.today()
		result = c.execute("SELECT uptime FROM time WHERE thedate=?", (today,)).fetchone()
		if result is None:
			c.execute("INSERT INTO time VALUES(?, ?)", (time, today))
			conn.commit()
		elif result is not None:
			c.execute("UPDATE time SET uptime=? WHERE thedate=?", (time, today))
			conn.commit()

		await asyncio.sleep(60)
		


if __name__ == "__main__":
	print("WARNING: Still under dev.")
	loop = asyncio.get_event_loop()
	asyncio.ensure_future(time_off())
	asyncio.ensure_future(notification_brightness())
	asyncio.ensure_future(logs())
	loop.run_forever()