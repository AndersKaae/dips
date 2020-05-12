from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, UnicodeText, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

engine = create_engine('sqlite:///dips1.db', connect_args={'check_same_thread': False})

Base = declarative_base()

class Transactions(Base):
	__tablename__ = 'transactions'
	orderNo = Column(String(100), primary_key=True)
	transactionNo = Column(String(30), nullable=False)
	amount = Column(String(30), nullable=False)
	currency = Column(String(30), nullable=False)
	cardType = Column(String(50), nullable=False)
	authTime = Column(String(200), nullable=False)
	fullfillTime = Column(String(200), nullable=True)
	aquirer = Column(String(30), nullable=False)

class Refunds(Base):
	__tablename__ = 'refunds'
	orderNo = Column(String(100), primary_key=True)
	amount = Column(String(30), nullable=False)

class LastUpdate(Base):
	__tablename__ = 'lastupdate'
	date = Column(String(20), primary_key=True)

Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)
session.commit()

def insertOrder(orderNo, transactionNo, amount, currency, cardType, authTime, fullfillTime, aquirer):
    isItUnique = session.query(Transactions).filter_by(orderNo = orderNo).first()
    if str(isItUnique) ==  "None":
        transactions = Transactions(orderNo = orderNo, transactionNo = transactionNo, amount = amount, currency = currency, cardType = cardType, authTime = authTime, fullfillTime = fullfillTime, aquirer = aquirer)
        session.add(transactions)
        session.commit()
        session.close()

def GetLastUpdate():
	query = session.query(LastUpdate).first()
	date = query.date
	return date

def SetLastUpdate(date):
	query = session.query(LastUpdate).first()
	query.date = date
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