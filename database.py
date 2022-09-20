from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, UnicodeText, func, Date, Float, desc, asc, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://root:4nrHCngtGYWzLACZeRYt@containers-us-west-80.railway.app:7103/railway')

Base = declarative_base()

class Transactions(Base):
	__tablename__ = 'transactions'
	orderNo = Column(String(100), primary_key=True)
	transactionNo = Column(String(30), nullable=False)
	amount = Column(Float, nullable=False)
	currency = Column(String(30), nullable=False)
	cardType = Column(String(50), nullable=False)
	authTime = Column(String(200), nullable=False)
	fullfillTime = Column(Date, nullable=True)
	aquirer = Column(String(30), nullable=False)

class TransactionsSE(Base):
	__tablename__ = 'transactions_se'
	orderNo = Column(String(100), primary_key=True)
	transactionNo = Column(String(30), nullable=False)
	amount = Column(Float, nullable=False)
	currency = Column(String(30), nullable=False)
	cardType = Column(String(50), nullable=False)
	authTime = Column(String(200), nullable=False)
	fullfillTime = Column(Date, nullable=True)
	aquirer = Column(String(30), nullable=False)

class Refunds(Base):
	__tablename__ = 'refunds'
	orderNo = Column(String(100), primary_key=True)
	amount = Column(String(30), nullable=False)

class GA_medium_device(Base):
    __tablename__ = 'ga_medium_device'
    transactionNo = Column(String(30), primary_key=True)
    medium = Column(String(30), nullable=False)
    device = Column(String(30), nullable=False)
    date = Column(Date, nullable=False)

class GA_product(Base):
    __tablename__ = 'ga_product'
    transactionNo = Column(String(30), primary_key=True)
    product = Column(String(30), nullable=False)
    date = Column(Date, nullable=False)

class GA_prices(Base):
    __tablename__ = 'ga_prices'
    product = Column(String(30), primary_key=True)
    price = Column(String(30), nullable=False)

class LastUpdate(Base):
    __tablename__ = 'lastupdate'
    date = Column(String(20), primary_key=True)
    failed = Column(Boolean, nullable=False)

Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)
session.commit()

def insertOrder(orderNo, transactionNo, amount, currency, cardType, authTime, fullfillTime, aquirer, country):
    if country == "DKK":
        isItUnique = session.query(Transactions).filter_by(orderNo = orderNo).first()
    if country == "SEK":
        isItUnique = session.query(TransactionsSE).filter_by(orderNo = orderNo).first()
    if str(isItUnique) ==  "None":
        if country == "DKK":
            transactions = Transactions(orderNo = orderNo, transactionNo = transactionNo, amount = amount, currency = currency, cardType = cardType, authTime = authTime, fullfillTime = fullfillTime, aquirer = aquirer)
        if country == "SEK":
            transactions = TransactionsSE(orderNo = orderNo, transactionNo = transactionNo, amount = amount, currency = currency, cardType = cardType, authTime = authTime, fullfillTime = fullfillTime, aquirer = aquirer)
        session.add(transactions)
        session.commit()
        session.close()

def GetLastUpdate():
	query = session.query(LastUpdate).first()
	return query

def SetLastUpdate(date, failed):
    query = session.query(LastUpdate).first()
    # If data base is empty it returns "None". Therefore the first tine we add and on subsequent updates we just modify value
    if query != None:
        query.date = date
        query.failed = failed
    else:
        lastUpdate = LastUpdate(date = date, failed = failed)
        session.add(lastUpdate)
    session.commit()

def insertRefund(orderNo, amount):
    isItUnique = session.query(Refunds).filter_by(orderNo = orderNo).first()
    if str(isItUnique) ==  "None":
        refunds = Refunds(orderNo = orderNo, amount = amount)
        ## Deducting refund if not seen before
        order = session.query(Transactions).filter_by(orderNo = orderNo).first()
        order.amount = str(Decimal(order.amount) - Decimal(amount))
        session.add(refunds)
        session.commit()
        session.close()

def PeriodRefactor(fromDate, toDate, country):
    if country == "DK":
        query = session.query(Transactions).filter(Transactions.fullfillTime.between(fromDate, toDate)).order_by(asc(Transactions.fullfillTime))
    if country == "SE":
        query = session.query(TransactionsSE).filter(TransactionsSE.fullfillTime.between(fromDate, toDate)).order_by(asc(TransactionsSE.fullfillTime))
    sum = 0
    for i in query:
        sum = sum + float(i.amount)
    return sum

def PurePeriod(fromDate, toDate, country):
    if country == "DK":
        query = session.query(Transactions).filter(Transactions.fullfillTime.between(fromDate, toDate)).order_by(asc(Transactions.fullfillTime))
    if country == "SE":
        query = session.query(TransactionsSE).filter(TransactionsSE.fullfillTime.between(fromDate, toDate)).order_by(asc(TransactionsSE.fullfillTime))
    return query

def ProductsPrDay(days):
    toDate = datetime.today().date()
    fromDate = toDate - timedelta(days=days - 1)
    # Getting all the data for the specific timefram
    query = session.query(GA_product).filter(GA_product.date.between(fromDate, toDate)).order_by(asc(GA_product.date))
    # Getting unique names
    product_names = session.query(GA_product.product).filter(GA_product.date.between(fromDate, toDate)).distinct()
    return query, product_names

def InserGoogleData(google_data):
    #print(google_data.__dict__)
    if google_data.product == "":
        isItUnique = session.query(GA_medium_device).filter_by(transactionNo = google_data.orderid).first()
        if str(isItUnique) ==  "None":
            data = GA_medium_device(transactionNo = google_data.orderid, medium = google_data.medium, device = google_data.device, date = google_data.date)
            session.add(data)
            session.commit()
    else:
        isItUnique = session.query(GA_product).filter_by(transactionNo = google_data.orderid).first()
        if str(isItUnique) ==  "None" and google_data.product.isdigit() == False:
            data = GA_product(transactionNo = google_data.orderid, product = google_data.product, date = google_data.date)
            session.add(data)
            session.commit()
    session.close()

def DeleteGoogleData():
    session.query(GA_medium_device).delete()
    session.query(GA_product).delete()
    session.commit()
    session.close()

def GetDateRangeForMissingGoogleData():
    # Getting the date range for tranactions
    date_range_transactions = []
    date_range_transactions.append(session.query(Transactions).order_by(asc(Transactions.fullfillTime)).first().fullfillTime)
    date_range_transactions.append(session.query(Transactions).order_by(desc(Transactions.fullfillTime)).first().fullfillTime)

    # Getting the date range for Google
    date_range_google = []
    gap_list = []
    if session.query(GA_medium_device).order_by(asc(GA_medium_device.date)).first() != None:
        from_date = session.query(GA_medium_device).order_by(asc(GA_medium_device.date)).first().date
        to_date = session.query(GA_medium_device).order_by(desc(GA_medium_device.date)).first().date
    else:
        from_date = datetime.today().date()
        to_date = from_date

    date_range_google.append(from_date)
    date_range_google.append(to_date)

    # Comparing from dates
    from_gap = []
    if date_range_google[0] > date_range_transactions[0]:
        from_gap.append(date_range_transactions[0])
        from_gap.append(date_range_google[0])
        gap_list.append(from_gap)

    to_gap = []
    if date_range_google[1] != date_range_transactions[1]:
        to_gap.append(date_range_google[1])
        to_gap.append(date_range_transactions[1])
        gap_list.append(to_gap)    
    return gap_list

def PopulatePriceTable():
    # First we get all the unique names from the GA_product table
    product_names = session.query(GA_product.product).distinct()
    for name in product_names:
        # If the name is not already in the price table we add it
        isItUnique = session.query(GA_prices).filter_by(product = name[0]).first()
        if str(isItUnique) ==  "None":
            data = GA_prices(product = name[0], price = "0")
            session.add(data)
    session.commit()
    session.close()

def UpdatePriceTable(data):
    session.query(GA_prices).delete()
    session.commit()
    for item in data:
        data = GA_prices(product = item[0], price = item[1])
        session.add(data)
    session.commit()
    session.close()

def QueryPriceTable():
    data = []
    query = session.query(GA_prices).all()
    for item in query:
        data.append(item.product)
        data.append(item.price)
    return data

def RetrievePriceTable():
    price_table = []
    price_line = []
    query = session.query(GA_prices).all()
    for item in query:
        if not ('Legat til' or 'Cheap' or 'Cheap test') in item.product:
            price_line.append(item.product)
            price_line.append(item.price)
            price_table.append(price_line)
            price_line = []
    return price_table