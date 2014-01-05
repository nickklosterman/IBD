#!/usr/bin/env/python
# -*- python -*- 
'''
This script attempts to perform bulk import of csv data
into a SQLite database.
It globs all csv files in the current directory and 
sticks the data in a StockData.sqlite database.
'''

import sqlite3
import glob
import os
import csv
from math import ceil
import sys
# for filez in fileList:
#     print(filez)

#     #make sure the file size isn't 0 
#     if (os.stat(filez).st_size!=0):
#         with open(filez,'rt') as csvfile:
#             dataReader=csv.DictReader(csvfile,delimiter=',')
#             #dataReader=csv.reader(csvfile,delimiter=',')
#             for row in dataReader:
#                 #print( '-=-=- '.join(row))
#                 #open=float(row["Open"])*100
#                 print("")
#                 print(row["Open"])
#                 print(float(row["Open"]))
#                 print(int(float(row["Open"])*100))
#                 print(int(ceil(float(row["Open"])*100)))

class ImportYahooStockCSVData:
    
    def __init__(self,database,table,directory):
        self.fileList=""
        self.database=database
        self.table=table
        self.directory=directory
        #        print(self.database,self.table,self.directory)
        self.connection=sqlite3.connect(self.database)
        self.getCSVFileList()
        self.databasePrep()
        self.loopOverFiles()
        self.connection.commit()

    def getCSVFileList(self):
        os.chdir(self.directory) 
        self.fileList=glob.glob("*.csv")
            
    def insertData(self,csvDictionary,symbol):
        insertCursor=self.connection.cursor()
        Open=int(round(float(csvDictionary["Open"])*100))
        High=int(round(float(csvDictionary["High"])*100))
        Low=int(round(float(csvDictionary["Low"])*100))
        Close=int(round(float(csvDictionary["Close"])*100))
        Adj_Close=int(round(float(csvDictionary["Adj Close"])*100))
        Query='INSERT INTO '+self.table
        insertCursor.execute(Query+' VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?)', (csvDictionary["Date"],symbol,Open,High,Low,Close,int(csvDictionary["Volume"]),Adj_Close))
        insertCursor.close()

    def databasePrep(self):
        cursor=self.connection.cursor()
        Query="DROP TABLE IF EXISTS "+self.table
        cursor.execute(Query)
        Query='CREATE TABLE IF NOT EXISTS '+self.table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
        cursor.execute(Query)
        cursor.close()
        
    def loopOverFiles(self):
        for csvfile in self.fileList:
            print(csvfile)
            # ticker=(csvfile.split('.'))[0] #extract ticker if file is named ticker.csf
            # ticker=ticker.strip()
            ticker=csvfile[12:-12] #extract ticker if file is named table.csv?s=TICKER&ignore=.csv
            print(ticker)
            #csvfile sure the file size isn't 0       
            if (os.stat(csvfile).st_size!=0):
                with open(csvfile,'rt') as csvFileHandle:
                    csvDataReader=csv.DictReader(csvFileHandle,delimiter=',')
                    for row in csvDataReader:
                        self.insertData(row,ticker)
        


#def main
import getopt

if 1:
    database="StockData.sqlite" 
    table="StockData"
    directory="YahooCSVStockDataFiles"
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:l:t:d:f:', ['--input=',
                                                                          '--output=',
                                                                          '--loginfile=',
                                                                          '--table=',
                                                                          '--database=',
                                                                          '--format='
                                                                        ])
except getopt.GetoptError as err:
    # print help information and exit:                                                                        
    print(err) # will print something like "option -a not recognized"                                         
        #usage()                                                                                                  
    sys.exit(2)

for opt, arg in options:
    if opt in ('-o', '--output'):
        outputfilename = arg
    elif opt in ('-i', '--input'):
        inputfilename = arg
    elif opt in ('-t', '--table'):
        table = arg
    elif opt in ('-d', '--database'):
        database = arg
    elif opt in ('-f', '--format'):
        outputFormat = arg
    elif opt == '--version':
        version = arg
        
Importer=ImportYahooStockCSVData(database,table,directory)
