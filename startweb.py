from flask import Flask, render_template
from webfunctions import *

app = Flask(__name__)

mostRecentDate = str(datetime.today() - timedelta(days=1))[:10]

@app.route("/")
def home():
	db = Database()
	dayRevenue = db.Period(mostRecentDate, mostRecentDate)
	monthToDate = db.Period(mostRecentDate, mostRecentDate[:-2]+'01')
	startdate, enddate = PreviousMonthToDate()
	previousMonthToDate = db.Period(startdate, enddate)
	lastThirtyDays = db.Period(mostRecentDate, str(datetime.today() - timedelta(days=30))[:10])
	previousLastThirtyDays = db.Period(str(datetime.today() - timedelta(days=30))[:10], str(datetime.today() - timedelta(days=60))[:10])

	result = db.ListPayments()
	return render_template('home.html', posts = result, dayRevenue = dayRevenue, monthToDate = monthToDate, previousMonthToDate = previousMonthToDate, lastThirtyDays = lastThirtyDays, previousLastThirtyDays = previousLastThirtyDays)

if __name__ == '__main__':
	app.run(debug=True)