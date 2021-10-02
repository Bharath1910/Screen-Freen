import sqlite3
# from plyer import notification
# import asyncio
# import screen_brightness_control as sbc
# import psutil
# from datetime import datetime, date

conn = sqlite3.connect('db.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS time (
	uptime INTEGER, 
	thedate TIMESTAMP 
  	)""")


#int
#str

# time = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
# time = time.total_seconds()

# today = date.today()
# print((today))
# result = c.execute("SELECT uptime FROM time WHERE thedate=?", (today,)).fetchone()
# if result is None:
# 	c.execute("INSERT INTO time VALUES(?, ?)", (time, today))
# 	conn.commit()
# elif result is not None:
# 	c.execute("UPDATE time SET uptime=? WHERE thedate=?", (time, today))
# 	conn.commit()

conn.close()
