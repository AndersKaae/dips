import os
from database import *
from getdata import ReadData
from autobrowse import selenium
import time
from datetime import datetime

firstRun = True

while True:
    if firstRun != True:
        print('Waiting for 20 minutes to fetch report...')
        time.sleep(1200)
    print('Getting data with Selenium')
    selenium("https://payment.architrade.com/login/login.action")
    print('Waiting for 10 minutes for report to arrive...')
    time.sleep(600)
    with os.scandir('reports/') as entries:
        for entry in entries:
            ReadData(os.path.join(os.path.dirname(__file__), "reports/", entry.name))
            os.remove("ChangedFile.csv")
    firstRun = False
    SetLastUpdate(datetime.today().strftime("%d-%m-%Y %H:%M"))