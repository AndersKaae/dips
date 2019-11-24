from flask import Flask, render_template, redirect, request
from webfunctions import *

app = Flask(__name__)

mostRecentDate = str(datetime.today() - timedelta(days=1))[:10]

@app.route("/", methods=['GET', 'POST'])
def home():
	formdata = ""
	try:
		formdata = request.form['email']
	except:
		print('Running first time?')	
	db = Database()
	dayRevenue = db.Period(mostRecentDate, mostRecentDate)
	monthToDate = db.Period(mostRecentDate, mostRecentDate[:-2]+'01')
	startdate, enddate = PreviousMonthToDate()
	previousMonthToDate = db.Period(startdate, enddate)
	lastThirtyDays = db.Period(mostRecentDate, str(datetime.today() - timedelta(days=30))[:10])
	if formdata != "":
		noOfDays = int(formdata)
	else:
		noOfDays = 7	
	lastweek = LastXDays(noOfDays)
	previousLastThirtyDays = db.Period(str(datetime.today() - timedelta(days=30))[:10], str(datetime.today() - timedelta(days=60))[:10])

	result = db.ListPayments()
	return render_template('home.html', posts = result, dayRevenue = dayRevenue, monthToDate = monthToDate, previousMonthToDate = previousMonthToDate, lastThirtyDays = lastThirtyDays, previousLastThirtyDays = previousLastThirtyDays, lastweek= lastweek)

if __name__ == '__main__':
	app.run(debug=True)