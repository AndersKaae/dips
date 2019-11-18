import pymysql
from decimal import Decimal
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "miro12sd"
        db = "dips1"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
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
                #print(relevant)
                #print(item['fullfillTime'])
                if str(item['fullfillTime']) == str(fromDate):
                    relevant = True
                    #print(relevant)
                if str(item['fullfillTime']) == str(toDate):
                    relevant = False
                    #print(relevant)
                    break
                if relevant == True:
                    sum = sum + Decimal(item['amount'])
            return sum

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

mostRecentDate = str(datetime.today() - timedelta(days=1))[:10]
db = Database()
dayRevenue = db.Period(mostRecentDate, mostRecentDate)
dayRevenue = f'{dayRevenue:,}'
monthToDate = db.Period(mostRecentDate, mostRecentDate[:-2]+'01')
monthToDate = f'{monthToDate:,}'
startdate, enddate = PreviousMonthToDate()
previousMonthToDate = db.Period(startdate, enddate)
previousMonthToDate = f'{previousMonthToDate:,}'
lastThirtyDays = db.Period(mostRecentDate, str(datetime.today() - timedelta(days=30))[:10])
lastThirtyDays = f'{lastThirtyDays:,}'