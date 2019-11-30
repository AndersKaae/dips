from flask import Flask, render_template, redirect, request, Markup, flash, url_for
from webfunctions import *
from getdata import *
import os

app = Flask(__name__)
app.secret_key = "d4bb81b1-2038-4f56-8bec-9e35472c4826"

CheckDirectoryStructure()

@app.route("/", methods=['GET', 'POST'])
def home():
	checkForFile()
	formdata = ""

	# This is needed to avoid error on first load since the form contains no data
	if request.method == 'POST': 
		formdata = request.form['days']
	if formdata != "":
		noOfDays = int(formdata)
	else:
		noOfDays = 7	

	# Figuring out what the latest date with data is
	db = Database()
	if db.Period(str(datetime.today())[:10], str(datetime.today())[:10]) == 0:
		endDate = datetime.today() - timedelta(days=1)
	else:
		endDate = datetime.today()

	# From current lastest date to the first in the month
	monthToDate = db.Period(str(endDate)[:10], str(endDate - timedelta(days=endDate.day - 1))[:10])
	previousMonthToDate = LastXMonths(24)[1][1]
	lastThirtyDays = db.Period(str(endDate)[:10], str(endDate - timedelta(days=29))[:10])
	lastweek = LastXDays(noOfDays)
	previousLastThirtyDays = db.Period(str(datetime.today() - timedelta(days=30))[:10], str(datetime.today() - timedelta(days=59))[:10])
	result = db.ListPayments()
	monthlyRevenue = LastXMonths(24)
	return render_template('home.html', posts = result, monthToDate = monthToDate, previousMonthToDate = previousMonthToDate, lastThirtyDays = lastThirtyDays, previousLastThirtyDays = previousLastThirtyDays, lastweek = lastweek, monthlyRevenue = monthlyRevenue[::-1])

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
	message = ''
	if request.method == "POST":
		if request.files:
			csvFile = request.files["inputField"]
			if allowedFiles(csvFile.filename) == True:
				csvFile.save(os.path.join(os.path.dirname(__file__), "temp/", csvFile.filename))
				message = Markup("<span>Files saved</span>")
				ReadData(os.path.join(os.path.dirname(__file__), "temp/", csvFile.filename))
				return redirect(url_for('home'))
			else:
				message = Markup("<span>Invalid file type</span>")
			flash(message)
			return redirect(request.url)
	return render_template("upload.html")

if __name__ == '__main__':
	app.run(debug=True)