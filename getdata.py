from sqlalchemy.sql.functions import count
from database import *
import configparser
from os import listdir
import os

## Creates the necessarry directory structure
def CheckDirectoryStructure():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "reports/")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "reports/"))
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "temp/")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "temp/"))

def ReadFile(filepath):
    linesInFile = []
    with open(filepath, 'rb') as fp:
        line = fp.readline()
        for line in enumerate(fp):
            line = line[1]
            line = line.decode("utf-8")
            line = line.strip('\r\n')
            linesInFile.append(line)  
    return linesInFile

def StartingLine(linesInFile):
    i = 1
    line = 0
    for item in linesInFile:
        item = item.split(",")
        if len(item) > 1:
            line = i + 1
            break
        i += 1
    return line

def ReformatDate(date):
    newDate = date.split("T")
    return newDate

def ReadData(file):
    print(file)
    # Gets list of lines in file
    linesInFile = ReadFile(file)
    n = 1
    # Checks if any lines in file
    if len(linesInFile) > 0:
        # Checks if Danish or Swedish file
        country = linesInFile[0].split(",")[3]
        # Removed "" from the string
        country = country.replace('"', '')

        for item in linesInFile:
            item = item.split(",")
            item = RemoveQuotes(item)
            date = ReformatDate(item[1])
            amount = ReformatAmount(item[2])
            #           OrderNo, TransNo, Amount,  currency, CardType, autTime, date, aquirer
            insertOrder(item[0], item[9], amount, item[3], item[7], "not used", datetime.strptime(date[0], '%Y-%m-%d'), item[5], country)

def RemoveQuotes(line):
    lenght_of_list = len(line)
    counter = 0
    while counter < lenght_of_list:
        line[counter] = line[counter].replace('"', '')
        counter +=1
    return line

def ReformatAmount(amount):
    decimal = amount[-2:]
    whole_number = amount[:-2]
    return whole_number + "." + decimal

def allowedFiles(filename):
    allowed = True
    if not "." in filename:
        allowed =  False
        return allowed
    if not "transactionsettlements" in filename:
        allowed =  False
        return allowed        
    ext = filename.rsplit(".", 1)[1]    
    if ext.upper() != "CSV":
        allowed =  False
    return allowed