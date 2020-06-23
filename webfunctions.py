import sqlite3
from decimal import Decimal
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.con = sqlite3.connect('dips1.db')
        self.cur = self.con.cursor()

    def ListPayments(self):
            self.cur.execute('SELECT orderNo, amount, fullfillTime FROM transactions ORDER BY fullfillTime DESC')
            result = self.cur.fetchall()
            return result

    def Period(self, fromDate, toDate):
            sum = 0
            relevant = False
            toDate = str(datetime.strptime(toDate, '%Y-%m-%d') - timedelta(days=1))[:10]
            self.cur.execute('SELECT orderNo, amount, fullfillTime FROM transactions ORDER BY fullfillTime DESC')
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

def LastYears(NumberofYears, today):
    db = Database()
    revenuePerYear = []
    currentYear = int(str(today)[:4])
    i = 1
    while i <= NumberofYears:
        if i == 1:
            startDate = str(today)[:10]
        else:
            startDate = str(currentYear) + "-12-31"
        revenue = db.Period(startDate, str(currentYear) + "-01-01")
        tempList = [currentYear, revenue]
        revenuePerYear.append(tempList)
        currentYear -= 1
        i += 1
    return(revenuePerYear)

def LastXDays(NumberOfDays):
    totalDays = NumberOfDays
    db = Database()
    revenuePerDay = []
    while NumberOfDays >= 0:
        tempList = []
        day = str(datetime.today() - timedelta(days=NumberOfDays))[:10]
        tempList.append(db.Period(day, day))
        day = datetime.strptime(day, '%Y-%m-%d')
        day = day.strftime("%A, %d %b %Y")
        tempList.append(day)
        # We are including the current day, but only displaying if revenue is > 0
        if tempList[0] > 0:
            revenuePerDay.append(tempList)
        # Since we are unsure of wether to show current day, we remove the oldest day if today is included
        if len(revenuePerDay) > totalDays:
            revenuePerDay.remove(revenuePerDay[0])
        NumberOfDays = NumberOfDays - 1
    return revenuePerDay

def PreviousMonthToDate(endDate):
    # Should probably refactor.... endDate input is not used....
    endDate = datetime.today()
    day = endDate.day
    lastDayOfLastMonth = endDate - timedelta(days=day)
    startDate = lastDayOfLastMonth - timedelta(days=lastDayOfLastMonth.day - 1)
    # This is done to make last month stop if it is shorter than current month
    if day > lastDayOfLastMonth.day:
        day = lastDayOfLastMonth.day
    endDate = startDate + timedelta(days=day - 1)
    return startDate, endDate

def LastXMonths(NumberOfMonths):
    db = Database()
    monthPairs = []
    tempMonthPair = []
    monthMoney = []
    # Setting up first month which might be a partial month
    endDate = datetime.today()
    # Checking if endDate revenue is > 0
    if db.Period(str(endDate)[:10], str(endDate)[:10]) == 0:
        endDate = endDate - timedelta(days=1)
    startDate = datetime.today() - timedelta(days=datetime.today().day - 1)
    tempMonthPair.append(str(startDate)[:10])
    tempMonthPair.append(str(endDate)[:10])
    monthPairs.append(tempMonthPair)
    #print(tempMonthPair)
    tempMonthPair = []
    while NumberOfMonths > 1:
        endDate = startDate - timedelta(days=1)
        startDate = endDate - timedelta(days=endDate.day - 1)
        tempMonthPair.append(str(startDate)[:10])
        tempMonthPair.append(str(endDate)[:10])
        monthPairs.append(tempMonthPair)
        #print(tempMonthPair)
        tempMonthPair = []
        NumberOfMonths = NumberOfMonths - 1

    # Passing the month pairs through the periode function
    db = Database()
    for item in monthPairs:
        tempMonthPair = []
        tempMonthPair.append(datetime.strptime(item[0], '%Y-%m-%d').strftime("%B %Y"))
        tempMonthPair.append(db.Period(item[1], item[0]))
        monthMoney.append(tempMonthPair)
    return monthMoney

def TopX():
    data = LastXDays(365)
    data.sort()
    last_10_slice = slice(-10, None)
    data = data[last_10_slice]
    return data