#!/usr/bin/python3
# -*- python -*-
#adding the above line will enable  python-mode when reading this file since it doesn't recognize the .py3 extension
#M-x python-mode

"""
This program outputs a csv matrix of data
Various data is output;
a matrix of dates x ranks, each cell holds the ticker for that date & rank
a matrix of dates x stocks, each cell holds the stock price on taht date & stock
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
        print(',',end="") #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,%s.price,' % (s,s),end="")
        print('')
    def PrintStockRankHeader(self):
        print(',',end="") #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,%s.price,' % (s,s),end="")
        print('')

    def PrintStockHeader(self):
        print(',',end="") #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.stockprice,' % (s),end="")
        print('')
    def PrintRankHeader(self):
        print(',',end="") #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,' % (s),end="")
        print('')

    def StockRankMatrixTransposed(self): 
        self.PrintStockRankHeader()
        for d in self.Dates:
            print('%s,' % (d),end="")
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    sys.stdout.write('%s' % (rank))
                print(',',end="")
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                #if stockprice!=0.0:
                if stockprice>0.0:
                    sys.stdout.write('%s' % (stockprice)) 
                print(',',end="")                 
            print('')

    def StockRankMatrix(self): 
        print("not done, not sure if worthwhile")
        # print("I don't think this works properly. There needs to be a,  ")
        # self.PrintStockRankHeader()
        # for d in self.Dates:
        #     print('%s' % (d),end="")
        #     for s in self.Stocks:
        #         rank=self.GetRankForStockDate(s,d)
        #         if rank!=-1:
        #             sys.stdout.write('%s' % (rank))
        #         print(',',end="")
        #         stockprice=self.GetStockOpenPriceForStockDate(s,d)
        #         if stockprice!=0.0:
        #             sys.stdout.write('%s' % (stockprice)) 
        #         print(',',end="")                 
        #     print('')

    def RankMatrixTransposed(self): 
        self.PrintRankHeader()
        for d in self.Dates:
            print('%s,' % (d),end="")
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    sys.stdout.write('%s' % (rank))
                print(',',end="")
            print('')

    def StockMatrixTransposed(self):
        self.PrintStockHeader()
        for d in self.Dates:
            print('%s,' % (d),end="")
            for s in self.Stocks:
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) 
                print(',',end="")                 
            print('')



    def RankMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print('%s,' % (s),end="") #start new line with  the stock
            for d in self.Dates:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    #print('%s' % (rank)),
                    sys.stdout.write('%s' % (rank)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting. http://codingrecipes.com/print-without-a-new-line-or-space-in-python
            #if not at end of list then output ,
                print(',',end="") #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL


    def StockMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print('%s,' % (s),end="") #start new line with  the stock
            for d in self.Dates:
                stockprice=self.GetStockOpenPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) 
            #if not at end of list then output ,
                print(',',end="") #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL
                
    """
    Print the dates out 
    leave first column empty as the stock tickers will occupy this column 
    """
    def PrintDates(self):
        print(",",end="")
        for d in self.Dates:
            print("%s," % (d),end="")



def RunTest(inputTable):
    print(inputTable)
    RM=RankMatrix(database,inputTable)
    #RM.PrintDates()
    RM.RankMatrix() #this will be the fastest since no calls are made to get prices.
    #RM.StockMatrix()
    print("")
    RM.RankMatrixTransposed()
    #RM.StockMatrixTransposed()
    #RM.StockRankMatrixTransposed()
    print("")   
    print("")

########### MAIN ############

import sys

import sqlite3
import getopt


tableList=["BC20","IBD50","IBD8585","Top200Composite"]
database="IBDdatabase.sqlite"
database="IBDTestDatabase.sqlite"
outputFormat=1
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
for table in tableList:
    RunTest(table)
#print(inputfilename,outputfilename,loginfile,table,database)
if 0:
    RM=RankMatrix(database,tableList[0])
    #RM.PrintDates()
    
    #RM.RankMatrix()
    RM.StockMatrix()
    RM.RankMatrixTransposed()

