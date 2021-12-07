import os
import time
import schedule


def job():
    os.system('python main.py')


# 创建定时
schedule.every().monday.at("17:30").do(job)
schedule.every().tuesday.at("17:30").do(job)
schedule.every().wednesday.at("17:30").do(job)
schedule.every().thursday.at("17:30").do(job)
schedule.every().friday.at("17:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
