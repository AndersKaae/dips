from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, UnicodeText, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///dips1.db', connect_args={'check_same_thread': False})

Base = declarative_base()

class BigMoney(Base):
	__tablename__ = 'bigmoney'
	orderNo = Column(String(100), primary_key=True)
	transactionNo = Column(String(30), nullable=False)
	amount = Column(String(30), nullable=False)
	currency = Column(String(30), nullable=False)
	cardType = Column(String(50), nullable=False)
	authTime = Column(String(200), nullable=False)
	fullfillTime = Column(String(200), nullable=True)
	aquirer = Column(String(30), nullable=False)

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
    isItUnique = session.query(BigMoney).filter_by(orderNo = orderNo).first()
    if str(isItUnique) ==  "None":
        bigmoney = BigMoney(orderNo = orderNo, transactionNo = transactionNo, amount = amount, currency = currency, cardType = cardType, authTime = authTime, fullfillTime = fullfillTime, aquirer = aquirer)
        session.add(bigmoney)
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