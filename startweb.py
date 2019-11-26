from flask import Flask, render_template, redirect, request, Markup, flash, url_for
from webfunctions import *
from getdata import *
import os

app = Flask(__name__)
app.secret_key = "d4bb81b1-2038-4f56-8bec-9e35472c4826"

mostRecentDate = str(datetime.today() - timedelta(days=1))[:10]

@app.route("/", methods=['GET', 'POST'])
def home():
	formdata = ""
	# This is needed to avoid error on first load since the form contains no data
	if request.method == 'POST': 
		formdata = request.form['days']
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

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
	message = ''
	if request.method == "POST":
		if request.files:
			csvFile = request.files["inputField"]
			if allowedFiles(csvFile.filename) == True:
				csvFile.save(os.path.join(os.path.dirname(__file__), config["DEFAULT"]["TempFilePath"], csvFile.filename))
				message = Markup("<span>Files saved</span>")
				ReadData(os.path.join(os.path.dirname(__file__), config["DEFAULT"]["TempFilePath"], csvFile.filename))
				return redirect(url_for('home'))
			else:
				message = Markup("<span>Invalid file type</span>")
			flash(message)
			return redirect(request.url)
	return render_template("upload.html")

if __name__ == '__main__':
	app.run(debug=True)