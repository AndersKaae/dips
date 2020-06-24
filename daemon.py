import os
from database import *
from getdata import ReadData
from autobrowse import selenium
import time
from datetime import datetime

def ProcessReports():
    with os.scandir('reports/') as entries:
        for entry in entries:
            fileandpath = os.path.join(os.path.dirname(__file__), "reports/", entry.name)
            try:
                ReadData(fileandpath)
            except:
                print('Failed to read data'.)
            os.remove(fileandpath)

def RunDaemon():
    firstRun = True
    while True:
        if firstRun != True:
            print(str(datetime.today().strftime("%d-%m-%Y %H:%M")) + ': Waiting for 20 minutes to fetch report...')
            time.sleep(1200)
        print('Getting data with Selenium')
        selenium("https://payment.architrade.com/login/login.action")
        print(str(datetime.today().strftime("%d-%m-%Y %H:%M")) + ': Waiting for 10 minutes for report to arrive...')
        time.sleep(600)
        ProcessReports()
        firstRun = False
        SetLastUpdate(datetime.today().strftime("%d-%m-%Y %H:%M"))

#ProcessReports()
RunDaemon()