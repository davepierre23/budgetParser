from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import logging
import csv

import logging as log
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

fileName = 'pcbanking.csv'
fileName2 = 'pcbanking.xlsx'
wb = Workbook()
ws = wb.active
with open(fileName, 'r') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save(fileName2)
wb = load_workbook(fileName2,"rb")
ws = wb.active

def findMaxRows(ws):
    maxRow = 1
    while (True):
        char = get_column_letter(1)
        value = ws[char +str(maxRow)].value
        log.debug(value)
        if(None == value):
            maxRow-=1
            log.debug(maxRow)
            return maxRow
        maxRow+=1

def findColRows(ws):
    maxCol = 1
    while (True):
        char = get_column_letter(maxCol)
        value = ws[char +str(1)].value
        log.debug(value)
        if(None == value):
            maxCol-=1
            log.debug(maxCol)
            return maxCol
        maxCol+=1

def printEveryLine(ws):
    for row in  range (1,findMaxRows(ws)):
        for col in range (1,findColRows(ws)):
            char = get_column_letter(col)
            log.info(ws[char +str(row)].value)
        log.info("")

def checkForInvalidCols(ws):
    row =1
    for col in range (1,findColRows(ws)):
        char = get_column_letter(col)
        gridValue=char +str(row)
        value = ws[gridValue].value
        if(value == '-'):
            log.debug("Invalid col ",gridValue,value)

# def parseFile(ws):
#     for row in  range (1,findMaxRows(ws)):

def printEveryLine(ws):
    for row in  range (1,findMaxRows(ws)):
        print("DAVE")
        for col in range (1,findColRows(ws)):
            char = get_column_letter(col)
            log.info(ws[char +str(row)].value)
        log.info("")
def deleteCol(ws,col):
    ws.delete_cols(col)
  
printEveryLine(ws)
# def createRow(row,ws) :
#     for col in range (1,findColRows(ws)):
#             char = get_column_letter(col)
#             log.info(ws[char +str(row)].value)
#         log.info("")
#     transactonDate = 
#     transactonDescript = 
#     bankAction = 
#     other = 

#     {
#     "transactonDate":,
#     "transactonDescript":,
#     "bankAction":,
#     "other": }

#wb.save(fileName2)