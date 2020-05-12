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
    newDate = date.split("/")
    newDate[2] = newDate[2].split(" ")
    newDate = newDate[2][0] + '-' + newDate[1] + '-' + newDate[0]
    return newDate

def ReadData(file):
    print(file)
    linesInFile = ReadFile(file)
    line = StartingLine(linesInFile)
    n = 1
    for item in linesInFile:
        n += 1
        if n > line:
            item = item.split(",")
            if 'captured' in file:
                date = ReformatDate(item[6])
                insertOrder(item[0], item[1], item[2], item[3], item[4], item[5], date, item[7])
            if 'refunded' in file:
                insertRefund(item[0], item[2])

def allowedFiles(filename):
    allowed = True
    if not "." in filename:
        allowed =  False
        return allowed
    if not "captured" in filename and not "refunded" in filename:
        allowed =  False
        return allowed        
    ext = filename.rsplit(".", 1)[1]    
    if ext.upper() != "TXT":
        allowed =  False
    return allowed

#ReadData('/Users/anders/Downloads/5327740__captured__10_05_2020_22_20_01.txt')
ReadData('/Users/anders/Downloads/5327740__refunded__12_05_2020_21_50_02.txt')