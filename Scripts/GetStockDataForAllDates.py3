#!/usr/bin/python3
# -*- python -*-
#M-x python-mode

"""
This program loops over a database table and obtains stock data for all date and stock ticker combinations
This program does work, but I believe a bulk download and insertion is faster.
"""

from StockSQLiteHelpers import getHistoricalData,insertStockData

class StockDataRetriever:
   
    def __init__(self,database,inputTable,outputTable):
        self.database=database
        self.inputTable=inputTable
        self.outputTable=outputTable
        self.connection=sqlite3.connect(self.database)
        self.Dates=self.GetDateList()
        self.Stocks=self.GetStockList()


    def GetDateList(self):
        dates=[]
        orderBy="A"
        queryCursor=self.connection.cursor()
        if orderBy=="A":
            queryCursor.execute("SELECT DISTINCT(Date) from %s ORDER BY DATE ASC " % (self.inputTable)) #Desc New->Old, ASC Old->New 
        elif orderBy=="D":
            queryCursor.execute("SELECT DISTINCT(Date) from %s ORDER BY DATE DESC " % (self.inputTable)) #Desc New->Old, ASC Old->New 
        while True:
            row=queryCursor.fetchone()
            #print(row)
            if row is  None:
                break
            if row[0][0] != "2": #enforce that we are looking at year 2XXX data
                break
            dates.append(row[0])
        return dates

    def GetStockList(self):
        StockTickers=[]
        queryCursor=self.connection.cursor()
        queryCursor.execute("SELECT DISTINCT(StockTicker) from %s ORDER BY StockTicker ASC " % (self.inputTable)) #ASC A->Z, Desc Z->A
        while True:
            row=queryCursor.fetchone()
            #print(row)
            if row is  None:
                break
            StockTickers.append(row[0])

        return StockTickers


    def StockMatrix(self):
        for s in self.Stocks:
            for d in self.Dates:
                stockData=getHistoricalData(s,d)
                print(".",end="")
                #print(stockData,end="")
                
                if stockData!=0 and stockData!="None":  #0 is returned if their is all ready data in the db, None is returned if there is an error obtaining data from Yahoo.
                    #print(stockData)
                    rank=self.GetRankForStockDate(s,d)
                    returnVal=insertStockData(self.outputTable,d,s,rank,stockData) 
                
    def GetRankForStockDate(self,StockTicker,Date):
        rank=""
        queryCursor=self.connection.cursor()
        queryCursor.execute("SELECT Rank from %s WHERE Date='%s' AND StockTicker='%s' " % (self.inputTable,Date,StockTicker)) 
        while True:
            row=queryCursor.fetchone()
            #print(row)
            if row is  None:
                break
            rank=int(row[0]) # WARNING: I'm not checking for the case when there are multiple entries. This is bad and shouldn't happen

        return rank




def RunTest():
    RM=StockDataRetriever(database,inputTable,outputTable)
    RM.StockMatrix()
    
########### MAIN ############

import sys

import sqlite3
import getopt


tableList=["BC20","IBD50","IBD8585","Top200Composite"]
inputTable=tableList[0]
database="IBDdatabase.sqlite"
database="IBDTestDatabase.sqlite"
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:d:', ['--input-table=',
                                                                        '--output-table=',
                                                                        '--database=',
                                                                        ])
except getopt.GetoptError as err:
    print(err) # will print something like "option -a not recognized"                                         
        #usage()                                                                                                  
    sys.exit(2)

for opt, arg in options:
    if opt in ('-o', '--output-table'):
        outputTable = arg
    elif opt in ('-i', '--input-table'):
        inputTable = arg
    elif opt in ('-d', '--database'):
        database = arg
    elif opt == '--version':
        version = arg

RunTest()
