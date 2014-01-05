#!/usr/bin/python3
# -*- python -*-
#adding the above line will enable  python-mode when reading this file since it doesn't recognize the .py3 extension
#M-x python-mode

"""
This program outputs a csv matrix of data
Various data is output;
a matrix of dates x ranks, each cell holds the ticker for that date & rank
a matrix of dates x stocks, each cell holds the stock price on taht date & stock
This version "prints" the output to a file. It is using the python paradigm to print
the data not to stdout, but to a file.
"""

from StockSQLiteHelpers import getHistoricalOpenPrice

class RankMatrix:
   
    def __init__(self,database,table):
        self.database=database
        self.table=table
        self.connection=sqlite3.connect(self.database)
        self.Dates=self.GetDateList()
        self.Stocks=self.GetStockList()


    def GetDateList(self):
        dates=[]
        orderBy="A"
        queryCursor=self.connection.cursor()
        if orderBy=="A":
            queryCursor.execute("SELECT DISTINCT(Date) from %s ORDER BY DATE ASC " % (self.table)) #Desc New->Old, ASC Old->New 
        elif orderBy=="D":
            queryCursor.execute("SELECT DISTINCT(Date) from %s ORDER BY DATE DESC " % (self.table)) #Desc New->Old, ASC Old->New 
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
        queryCursor.execute("SELECT DISTINCT(StockTicker) from %s ORDER BY StockTicker ASC " % (self.table)) #ASC A->Z, Desc Z->A
        while True:
            row=queryCursor.fetchone()
            #print(row)
            if row is  None:
                break
            StockTickers.append(row[0])

        return StockTickers


    def GetRankForStockDate(self,StockTicker,Date):
        rank=-1
        queryCursor=self.connection.cursor()
        queryCursor.execute("SELECT Rank from %s WHERE Date='%s' AND StockTicker='%s' " % (self.table,Date,StockTicker)) 
        while True:
            row=queryCursor.fetchone()
            #print(row)
            if row is  None:
                break
            rank=int(row[0]) # WARNING: I'm not checking for the case when there are multiple entries. This is bad and shouldn't happen

        return rank


        """
        deprecated
        """
    def GetStockPriceForStockDate(self,StockTicker,Date):
        #print(StockTicker,Date)
        StockData=getHistoricalStockPrice(StockTicker,Date)
        #print(StockData)
        openPrice=0.0
        if StockData[0][0]!="Date": # a simple error check since this first field should be "Date"   
            #print("ERROR for %s" % (StockTicker)) #enter this data into an errors database                    
            
	    # insert_error_data(tableerror,date,ticker,rank)
            bob=0
        else:
             if StockData[0][4]=='Close':
                openPrice=StockData[1][4]

        return openPrice

    def GetStockOpenPriceForStockDate(self,StockTicker,Date):
        #print(StockTicker,Date)

        openPrice=getHistoricalOpenPrice(StockTicker,Date)

        return openPrice


    def PrintRankStockHeader(self):
        print(',',end="",file=f) #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,%s.price,' % (s,s),end="",file=f)
        print('',file=f)
    def PrintStockRankHeader(self):
        print(',',end="",file=f) #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,%s.price,' % (s,s),end="",file=f)
        print('',file=f)

    def PrintStockHeader(self):
        print(',',end="",file=f) #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.stockprice,' % (s),end="",file=f)
        print('',file=f)
    def PrintRankHeader(self):
        print(',',end="",file=f) #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,' % (s),end="",file=f)
        print('',file=f)

    def StockRankMatrixTransposed(self): 
        self.PrintStockRankHeader()
        for d in self.Dates:
            print('%s,' % (d),end="",file=f)
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    print('%s' % (rank),sep='',end="",file=f) #                    sys.stdout.write('%s' % (rank))
                print(',',end="",file=f)
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                #if stockprice!=0.0:
                if stockprice>0.0:
                    print('%s' % (stockprice),sep='',end="",file=f) #                    sys.stdout.write('%s' % (stockprice)) 
                print(',',end="",file=f)                 
            print('',file=f)

    def StockRankMatrix(self): 
        print("not done, not sure if worthwhile")

    def RankMatrixTransposed(self): 
        self.PrintRankHeader()
        for d in self.Dates:
            print('%s,' % (d),end="",file=f)
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    print('%s' % (rank),sep='',end="",file=f) #                    sys.stdout.write('%s' % (rank))
                #else:
                #    print('30',sep='',end='',file=f) #still output something even if is off list. 
                print(',',end="",file=f)
            print('',file=f)

    def StockMatrixTransposed(self):
        self.PrintStockHeader()
        for d in self.Dates:
            print('%s,' % (d),end="",file=f)
            for s in self.Stocks:
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                if stockprice!=0.0:
                    print('%s' % (stockprice),sep='',end="",file=f) #                    sys.stdout.write('%s' % (stockprice)) 
                print(',',end="",file=f)                 
            print('',file=f)



    def RankMatrix(self):
        self.PrintDates() #print header of dates
        print("",file=f ) #output EOL
        for s in self.Stocks:
            print('%s,' % (s),end="",file=f) #start new line with  the stock
            for d in self.Dates:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    #print('%s' % (rank)),
                    #sys.stdout.write('%s' % (rank)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting. http://codingrecipes.com/print-without-a-new-line-or-space-in-python
                    print('%s' % (rank),sep='',end="",file=f) 
            #if not at end of list then output ,
                print(',',end="",file=f) #OR add to string and then remove last character when done with that string of dates
            print("",file=f) #output EOL


    def StockMatrix(self):
        self.PrintDates() #print header of dates
        print("",file=f) #output EOL
        for s in self.Stocks:
            print('%s,' % (s),end="",file=f) #start new line with  the stock
            for d in self.Dates:
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                if stockprice!=0.0:
                    print('%s' % (stockprice),sep='',end="",file=f) #                    sys.stdout.write('%s' % (stockprice)) 
            #if not at end of list then output ,
                print(',',end="",file=f) #OR add to string and then remove last character when done with that string of dates
            print("",file=f) #output EOL
                
    """
    Print the dates out 
    leave first column empty as the stock tickers will occupy this column 
    """
    def PrintDates(self):
        print(",",end="",file=f)
        for d in self.Dates:
            print("%s," % (d),end="",file=f)



def RunTest(inputTable):
    print(inputTable,file=f)
    RM=RankMatrix(database,inputTable)
    #RM.PrintDates()
    #RM.RankMatrix() #this will be the fastest since no calls are made to get prices.
    #RM.StockMatrix()
    print("",file=f)
    RM.RankMatrixTransposed()
    #RM.StockMatrixTransposed()
    #RM.StockRankMatrixTransposed()
    print("",file=f)   
    print("",file=f)

########### MAIN ############

import sys

import sqlite3
import getopt

if 0:
    database="IBDdatabase.sqlite" 
    tableList=["BC20","IBD50","IBD8585","Top200Composite"]
else:
    tableList=["BC20"]
    database="IBDTestDatabase.sqlite"
outputFormat=1
outputfilename="RankMatrixOutputfile.csv"
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

with open(outputfilename,'wt') as f:
    for table in tableList:
        RunTest(table)
#print(inputfilename,outputfilename,loginfile,table,database)
if 0:
    RM=RankMatrix(database,tableList[0])
    #RM.PrintDates()
    
    #RM.RankMatrix()
    RM.StockMatrix()
    RM.RankMatrixTransposed()

