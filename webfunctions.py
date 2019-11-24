import pymysql
import sqlite3
from decimal import Decimal
from datetime import datetime, timedelta
from urllib.request import urlopen

class Database:
    def __init__(self):
        #host = "127.0.0.1"
        #user = "root"
        #password = "SOMETHING"
        #db = "dips1"
        #self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.con = sqlite3.connect('dips1.db')
        self.cur = self.con.cursor()

    def ListPayments(self):
            self.cur.execute('SELECT orderNo, amount, fullfillTime FROM bigmoney ORDER BY fullfillTime DESC')
            result = self.cur.fetchall()
            return result

    def Period(self, fromDate, toDate):
            sum = 0
            relevant = False
            toDate = str(datetime.strptime(toDate, '%Y-%m-%d') - timedelta(days=1))[:10]
            self.cur.execute('SELECT orderNo, amount, fullfillTime FROM bigmoney ORDER BY fullfillTime DESC')
            total = self.cur.fetchall()
            for item in total:
                if str(item[2]) == str(fromDate):
                    relevant = True
                if str(item[2]) == str(toDate):
                    relevant = False
                    break
                if relevant == True:
                    sum = sum + Decimal(item[1])
            return sum

def LastXDays(NumberOfDays):
    db = Database()
    revenuePerDay = []
    while NumberOfDays > 0:
        tempList = []
        day = str(datetime.today() - timedelta(days=NumberOfDays))[:10]
        tempList.append(db.Period(day, day))
        day = datetime.strptime(day, '%Y-%m-%d')
        day = day.strftime("%A, %d %b %Y")
        tempList.append(day)
        revenuePerDay.append(tempList)   
        NumberOfDays = NumberOfDays - 1
    return revenuePerDay

def PreviousMonthToDate():
    mostRecentDate = str(datetime.today() - timedelta(days=1))[:10]
    dateAsString = str(mostRecentDate)
    dateAsString = dateAsString.split('-')
    dateAsString[1] = str(int(dateAsString[1]) - 1)
    startdate = dateAsString[0] + "-" + dateAsString[1].zfill(2) + "-" + dateAsString[2]
    dateAsString[2] = '01'
    enddate = dateAsString[0] + "-" + dateAsString[1] + "-" + dateAsString[2]
    db = Database()
    mostRecentDate = db.Period(startdate, enddate)
    return startdate, enddate

