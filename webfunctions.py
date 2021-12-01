import sqlite3
from decimal import Decimal
from datetime import datetime, timedelta
from database import *

def LastYears(NumberofYears, today):
    revenuePerYear = []
    currentYear = int(str(today)[:4])
    i = 1
    while i <= NumberofYears:
        if i == 1:
            startDate = str(today)[:10]
        else:
            startDate = str(currentYear) + "-12-31"
        revenue = PeriodRefactor(startDate, str(currentYear) + "-01-01")
        tempList = [currentYear, revenue]
        revenuePerYear.append(tempList)
        currentYear -= 1
        i += 1
    return(revenuePerYear)

def LastXDays(NumberOfDays, country):
    temp_revenue_per_day = []
    final_revenue_per_day = []
    start_day = str(datetime.today() - timedelta(days=NumberOfDays))[:10]
    data = PurePeriod(start_day, datetime.today(), country)
    daily_amount = 0
    for item in data:
        # This line determines if the item is the first of a new day or in the current day. If start_day == item.fullfillTime we are in the current day.
        if str(start_day) == str(item.fullfillTime):
            daily_amount = daily_amount + float(item.amount)
            latest_day = item.fullfillTime
        else:
            # This line is a new day. We save our daily amounts etc.
            temp_revenue_per_day.append(daily_amount)
            formatted_day = datetime.strptime(str(start_day), '%Y-%m-%d')
            temp_revenue_per_day.append(formatted_day.strftime("%A, %d %b %Y"))
            final_revenue_per_day.append(temp_revenue_per_day)
            # Day is reset
            temp_revenue_per_day = []
            daily_amount = 0
            daily_amount = daily_amount + float(item.amount)
            start_day = item.fullfillTime
            latest_day = item.fullfillTime

    # This is for the last day
    temp_revenue_per_day.append(daily_amount)
    formatted_day = datetime.strptime(str(latest_day), '%Y-%m-%d')
    formatted_day = formatted_day.strftime("%A, %d %b %Y")
    temp_revenue_per_day.append(formatted_day)
    final_revenue_per_day.append(temp_revenue_per_day)
    return final_revenue_per_day

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

def LastXMonths(NumberOfMonths, country):
    monthPairs = []
    tempMonthPair = []
    monthMoney = []
    # Setting up first month which might be a partial month
    endDate = datetime.today()
    # Checking if endDate revenue is > 0
    if PeriodRefactor(str(endDate)[:10], str(endDate)[:10], country) == 0:
        endDate = endDate - timedelta(days=1)
    startDate = datetime.today() - timedelta(days=datetime.today().day - 1)
    tempMonthPair.append(str(startDate)[:10])
    tempMonthPair.append(str(endDate)[:10])
    monthPairs.append(tempMonthPair)
    
    tempMonthPair = []
    while NumberOfMonths > 1:
        endDate = startDate - timedelta(days=1)
        startDate = endDate - timedelta(days=endDate.day - 1)
        tempMonthPair.append(str(startDate)[:10])
        tempMonthPair.append(str(endDate)[:10])
        monthPairs.append(tempMonthPair)
        tempMonthPair = []
        NumberOfMonths = NumberOfMonths - 1

    # Passing the month pairs through the periode function
    for item in monthPairs:
        tempMonthPair = []
        tempMonthPair.append(datetime.strptime(item[0], '%Y-%m-%d').strftime("%B %Y"))
        tempMonthPair.append(PeriodRefactor(item[0], item[1], country))
        monthMoney.append(tempMonthPair)
    return monthMoney

def TopX(country):
    data = LastXDays(10000, country)
    data.sort()
    last_10_slice = slice(-10, None)
    data = data[last_10_slice]
    return data

def DaysThisMonth():
    # Getting month and year
    current_year = datetime.today().year
    next_month = datetime.today().month + 1
    if next_month == 13:
        next_month = 1
        current_year +=1
    # Creating a string and converting to date
    date_time_str = str(current_year) + '-' + str(next_month) + '-01'
    # Substracting 1 day to get the number of days
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d') - timedelta(days=1)
    # Getting and returning number of days
    return date_time_obj.day
