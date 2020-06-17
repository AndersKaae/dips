from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from secrets import *

def selenium(url):
	options = Options()
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
	options.add_experimental_option("detach", True)
	browser = webdriver.Chrome('./chromedriver', chrome_options=options)
	browser.get(url=url)

	# Finding the loging and password fields
	username = browser.find_element_by_id("doLogin_username")
	password = browser.find_element_by_id("doLogin_password")

	# Sending data to the fields
	username.send_keys(dibsUser)
	password.send_keys(dibsPass)

	# Click submit
	browser.find_element_by_id("doLogin_loginbox_login").click()

	# Navigate to report page
	browser.get("https://payment.architrade.com/admin/order_report.pfml?shop=5327740")
	
	# Click radio option
	browser.find_element_by_css_selector("input[type='radio'][value='captured']").click()

	# Find drop down and select option
	selected = Select(browser.find_element_by_id("sendtypeid"))
	selected.select_by_index(1)

	# Enter FTP info
	ftp = browser.find_element_by_id("recipientid")
	ftp.send_keys(ftplogin)

	# Click Submit
	browser.find_element_by_class_name('button').click()    

	return browser.page_source

browser = selenium("https://payment.architrade.com/login/login.action")
