from database import *
from ftplib import FTP
import configparser

# Reading config file
config = configparser.ConfigParser()
config.read('config.ini')

def ConnectFTP():
    print('Connecting to FTP...')
    ftp = FTP(config["DEFAULT"]["ServerAdress"])
    ftp.login(user= config["DEFAULT"]["UserName"], passwd = config["DEFAULT"]["Password"])
    ftp.cwd('data/dibs')
    filelist=[]
    ftp.retrlines('LIST', filelist.append)
    for item in filelist:
        item = item.split(' ')
        item = item[len(item)- 1]
        print('Downloading: ' + item)
        download(ftp,item)
    return item

def download(ftp, filename):
    ftp.retrbinary("RETR " + filename, open(filename, "wb").write, 8*1024)
    
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
    newDate = date.split("/")
    newDate[2] = newDate[2].split(" ")
    newDate = newDate[2][0] + '-' + newDate[1] + '-' + newDate[0]
    return newDate

def ReadData(file):
    linesInFile = ReadFile(file)
    line = StartingLine(linesInFile)
    n = 1
    for item in linesInFile:
        n += 1
        if n > line:
            item = item.split(",")
            date = ReformatDate(item[6])
            insertOrder(item[0], item[1], item[2], item[3], item[4], item[5], date, item[7])

def OldMethod():
    manualMode = True
    if manualMode == False:
        # Getting file from FTP
        filename = ConnectFTP()
        # Creating an array from file
        print('Parsing data from FTP')
        linesInFile = ReadFile(filename)
    else:
        # Used to manually pull in data from file
        print('Parsing data from file using manual mode')
        #linesInFile = ReadFile('5327740__captured__09_10_2019_21_00_02.txt')
        #linesInFile = ReadFile('5327740__captured__10_10_2019_10_00_04.txt')
        linesInFile = ReadFile('test.txt')

    # Figuring out which part of the array contains relevant data
    line = StartingLine(linesInFile)

    # Loop through array starting from relevant place and saving to DB
    n = 1
    print('Storing data in database.')
    for item in linesInFile:
        n += 1
        if n > line:
            item = item.split(",")
            date = ReformatDate(item[6])
            insertOrder(item[0], item[1], item[2], item[3], item[4], item[5], date, item[7])
    