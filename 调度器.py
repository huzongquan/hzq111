# -*- coding：utf-8 -*-
# @Time  : 2019/8/26 17:16
# @Author: huzongquan
# @File  : 调度器.py
# @Describe :this is describe

import schedule
import time


def job():
    print("I'm working...")


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
schedule.every(1).to(10).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)