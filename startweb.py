from flask import Flask, render_template, redirect, request, Markup, flash, url_for
from sqlalchemy.sql.expression import false
from webfunctions import *
from getdata import *
import os
from database import PeriodRefactor, insertOrder
from productsFunctions import GetproductsPrDay, CreateProductPrDayString


app = Flask(__name__)
app.secret_key = "d4bb81b1-2038-4f56-8bec-9e35472c4826"

CheckDirectoryStructure()

lastUpdateTime = ""

@app.route("/", methods=['GET', 'POST'])
def home():
	# Get argument from URL. If there is no argument we default to DK
	country = request.args.get('country')
	noOfDays = request.args.get('days')
	if noOfDays != None:
		noOfDays = int(noOfDays)
	else:
		noOfDays = 7

	# This is needed to avoid error on first load since the form contains no data
	if request.method == 'POST': 
		formdata = request.form['days']
		country = request.form['country']
		return redirect("/?country=" + country +"&days=" + formdata)

	if country == None:
		return redirect("/?country=DK&days=" + str(noOfDays))

	# Figuring out what the latest date with data is
	if PeriodRefactor(str(datetime.today())[:10], str(datetime.today())[:10], country) == 0:
		endDate = datetime.today() - timedelta(days=1)
	else:
		endDate = datetime.today()

	# From current lastest date to the first in the month
	startDate = endDate - timedelta(days=endDate.day - 1)
	monthToDate = PeriodRefactor(str(startDate)[:10], str(endDate)[:10], country)
	previousMonthStart, previousMonthEnd  = PreviousMonthToDate(endDate)
	previousMonthToDate = PeriodRefactor(str(previousMonthStart)[:10], str(previousMonthEnd)[:10], country)
	lastThirtyDays = PeriodRefactor(str(endDate - timedelta(days=29))[:10], str(endDate)[:10], country)
	lastweek = LastXDays(noOfDays, country)
	previousLastThirtyDays = PeriodRefactor(str(datetime.today() - timedelta(days=59))[:10], str(datetime.today() - timedelta(days=30))[:10], country)
	monthlyRevenue = LastXMonths(24, country)
	projectedRevenue = round((monthToDate / datetime.today().day) * DaysThisMonth(), 2)
	return render_template('home.html', monthToDate = monthToDate, previousMonthToDate = previousMonthToDate, lastThirtyDays = lastThirtyDays, previousLastThirtyDays = previousLastThirtyDays, lastweek = lastweek, monthlyRevenue = monthlyRevenue[::-1], lastUpdateTime = GetLastUpdate(), formdata = noOfDays, country = country, projectedRevenue = projectedRevenue)

@app.route("/products", methods=['GET', 'POST'])
def products():
	# This is needed to avoid error on first load since the form contains no data
	days = 7
	if request.method == 'POST': 
		days = request.form['days']
	if days != "":
		noOfDays = int(days)
	else:
		noOfDays = 7	
	products_pr_day, unique_product = GetproductsPrDay(int(days), "products")
	revenue_pr_day, unique_product = GetproductsPrDay(int(days), "revenue")
	string_revenue_pr_day = CreateProductPrDayString(revenue_pr_day)
	string_products_pr_day = CreateProductPrDayString(products_pr_day)
	return render_template('products.html', string_products_pr_day = string_products_pr_day, string_revenue_pr_day = string_revenue_pr_day, unique_product = unique_product, days = days)

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
				failed = False
				SetLastUpdate(datetime.today().strftime("%d-%m-%Y %H:%M"), failed)
				return redirect(url_for('home'))
			else:
				message = Markup("<span>Invalid file type</span>")
			flash(message)
			return redirect(request.url)
	return render_template("upload.html")

@app.route("/top", methods=["GET", "POST"])
def top():
	resultDK = TopX("DK")
	resultSE = TopX("SE")
	resultNO = TopX("NO")
	return render_template('top.html', toplistDK = resultDK, toplistSE = resultSE, toplistNO = resultNO)

@app.route("/config", methods=['GET', 'POST'])
def config():
	price_data = RetrievePriceTable()
	if request.method == 'POST': 
		for item in price_data:
			item[1] = request.form[item[0]]
		UpdatePriceTable(price_data)
		return redirect(url_for('config'))
	return render_template('config.html', price_data = price_data)

@app.route("/reepayhook", methods=['GET', 'POST'])
def reepayhook():
	if request.method == 'POST':
		if request.json['event_type'] == 'invoice_settled':
			
			# Getting the country from the URL
			country = request.args.get('country')

			# Constructing URL and retrieving data
			invoice_no = request.json['invoice']
			json_data = GetInvoiceDataFromAPI(invoice_no, country)
			try:
				orderNo, transactionNo, amount, currency, cardType, authTime, fullfillTime, aquirer = ParseInvoiceData(json_data)
				insertOrder(orderNo, transactionNo, amount, currency, cardType, authTime, fullfillTime, aquirer, country)
				print('Data updated with webhook')
				SetLastUpdate(datetime.today().strftime("%d-%m-%Y %H:%M"), False)
			except Exception as e:
				print(e)
				print('Failed to parse invoice_no: ' + invoice_no)
	return "Data recieved"

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True, threaded=True)
    app.secret_key = 'super secret key'