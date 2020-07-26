"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from database import InserGoogleData, GetDateRangeForMissingGoogleData, DeleteGoogleData, PopulatePriceTable
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'coastal-cider-284008-74dd15361b41.json'
VIEW_ID = '66097854'

class GoogleData:
    def __init__(self, orderid, medium, device, product, value, date):
        self.orderid = orderid
        self.medium = medium
        self.device = device
        self.product = product
        self.value = value
        self.date = date

def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
    An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


def get_report1(analytics, from_date, to_date):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': from_date, 'endDate': to_date}],
          'metrics': [{'expression': 'ga:transactionRevenue'}],
          'dimensions': [{'name': 'ga:transactionId'}, 
                         {"name": "ga:sourceMedium"},
                         {"name": "ga:deviceCategory"},
                         {"name": "ga:date"}
                         ]
        }]
      }
  ).execute()

def get_report2(analytics, from_date, to_date):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': from_date, 'endDate': to_date}],
          'metrics': [{'expression': 'ga:uniquePurchases'}],
          'dimensions': [{'name': 'ga:transactionId'}, 
                         {"name": "ga:productName"},
                         {"name": "ga:date"}
                         ]
        }]
      }
  ).execute()

def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
    response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])
        google_data = GoogleData("", "", "", "", "", "")
        for header, dimension in zip(dimensionHeaders, dimensions):
            #print(header + ': ', dimension)
            if header == 'ga:transactionId':
                google_data.orderid = dimension
            if header == 'ga:deviceCategory':
                google_data.device = dimension
            if header == 'ga:sourceMedium':
                google_data.medium = dimension
            if header == 'ga:productName':
                google_data.product = dimension
            if header == 'ga:date':
                google_data.date = dimension

        for i, values in enumerate(dateRangeValues):
            #print('Date range:', str(i))
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                #print(metricHeader.get('name') + ':y', value)
                if metricHeader.get('name') == 'ga:itemRevenue':
                    google_data.value = values.get('values')[0]
        #Converting google dates to correct format
        google_data.date = datetime.strptime(str(google_data.date), '%Y%m%d').date()
        
        InserGoogleData(google_data)
        google_data = GoogleData("", "", "", "", "", "")

def CreateDates(date_list, from_date, to_date):
    date_pair = []
    # The Google API returns a maximum of 1.000 records at the time. make sure that you 
    # choose so few days that no more records are produced!!
    day_limit = 7
    # If distance less than 30 days function not needed
    if (to_date - from_date).days > day_limit:
        original_from_date = from_date
        new_from_date = to_date - timedelta(days=day_limit)
        # We loop through all the dates in increments
        while original_from_date < new_from_date:
            date_pair = []
            date_pair.append(str(new_from_date)[:10])
            date_pair.append(str(to_date)[:10])
            date_list.append(date_pair)
            to_date = new_from_date - timedelta(days=1)
            new_from_date = new_from_date - timedelta(days=day_limit)
        date_pair.append(str(new_from_date)[:10])
        date_pair.append(str(to_date)[:10])
        date_list.append(date_pair)
    else:
        date_pair.append(from_date - timedelta(days=1))
        date_pair.append(to_date)
        date_list.append(date_pair)
    return date_list

def PostToAPI(date_pair, analytics):
    print(f'Processing from {date_pair[0]} to {date_pair[1]}')
    response1 = get_report1(analytics, str(date_pair[0]), str(date_pair[1]))
    response2 = get_report2(analytics, str(date_pair[0]), str(date_pair[1]))
    return response1, response2

def Google_One_Day():
    analytics = initialize_analyticsreporting()
    date_pair = ['2020-06-26','2020-07-26']
    response1, response2 = PostToAPI(date_pair, analytics)
    print_response(response1)
    print_response(response2)

def Google_API_Main():
    # Getting the date ranges for missing Google data
    gap_list = GetDateRangeForMissingGoogleData()
    if len(gap_list) > 0:
        # Deviding periods so no are longer than 30 days
        date_list =[]
        for item in gap_list:
            date_list = CreateDates(date_list, item[0], item[1])
        
        #Initializing Google API
        analytics = initialize_analyticsreporting()

        # Posting date pairs to API
        for date_pair in date_list:
            response1, response2 = PostToAPI(date_pair, analytics)
            # Parsing response and saving to DB
            print_response(response1)
            print_response(response2)
    PopulatePriceTable()

#DeleteGoogleData()
#Google_API_Main()