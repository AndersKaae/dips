from database import ProductsPrDay, QueryPriceTable
from datetime import datetime

def GetproductsPrDay(days, revenue_productconter):
    # Getting data from database from relevant period
    query, product_names = ProductsPrDay(days)
    # Determining which kinds of products are sold in period
    unique_product = []
    unique_dates = []
    complete_matrix = []

    # Getting our ranges both in terms of which dates and which products are in the query
    for item in query:
        if item.product not in unique_product:
            unique_product.append(item.product)
        if item.date not in unique_dates:
            unique_dates.append(item.date)

    # Contrstructing the matrix which we will populate with data. 
    for date in unique_dates:
        date_row = []
        date_row.append(date)
        for item in unique_product:
            date_row.append(0)
        complete_matrix.append(date_row)

    # Checking to see if we want revenue or product count
    if revenue_productconter == 'revenue':
        prices = QueryPriceTable()

    # Now we loop through the query and determine the placement of each value
    for item in query:
        placement_date = unique_dates.index(item.date)
        placement_product = unique_product.index(item.product)
        if revenue_productconter == 'revenue':
            complete_matrix[placement_date][placement_product + 1] += float(GetPrice(item.product, prices))
        if revenue_productconter == 'products':
            complete_matrix[placement_date][placement_product + 1] += 1

    # Converting the dates to strings
    for item in complete_matrix:
        item[0] = str(item[0])

    return complete_matrix, unique_product

def CreateProductPrDayString(complete_matrix):
    string = ""
    list_of_strings = []
    # Need to look like this: ['2010', 10, 24, 20, 32, 18, 5, '']
    for item in complete_matrix:
        i = 0
        while i < len(item):
            if i == 0:
                string = string + "'" + datetime.strptime(item[i], '%Y-%m-%d').strftime("%A, %d %b %Y") + "'"
            elif i != len(item):
                string = string + ", " + str(item[i])
            i+=1
        #if n != len(complete_matrix) -1:
        #    string = string + ", ''],['"
        else:
            string = string + ", ''"
        list_of_strings.append(string)
        string = ""
    return list_of_strings

def GetPrice(product_name, prices):
    placement_price = prices.index(product_name) + 1
    return prices[placement_price].replace(",", ".")
