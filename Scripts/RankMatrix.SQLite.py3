#!/usr/bin/env/python3

"""
This program outputs a csv matrix of data
"""

from YahooStockQuotes import getHistoricalStockPrices 



def prepprice(data):
    temp=striphtml(data.rstrip())
    temp2=temp[1:] #remove dollar sign
    temp3=temp2.strip() #remove whitespace
    p = re.compile(r',') #remove comma in price since that'll screw things up as far as outputting to csv.
    return p.sub('',temp3)

class RankMatrix:
    
    def __init__(self,database,table):
        self.database=database
        self.table=table
        self.connection=sqlite3.connect(self.database)
        self.Dates=self.GetDateList()
        self.Stocks=self.GetStockList()


    def GetDateList(self):
        dates=[]
        queryCursor=self.connection.cursor()
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

    def GetStockPriceForStockDate(self,StockTicker,Date):
        #print(StockTicker,Date)
        StockData=getHistoricalStockPrices(StockTicker,Date)
        #print(StockData)
        openPrice=0.0
        if StockData[0][0]!="Date": # a simple error check since this first field should be "Date"   
            print("ERROR for %s" % (StockTicker)) #enter this data into an errors database                    
#            insert_error_data(tableerror,date,ticker,rank)
        else:
             if StockData[0][4]=='Close':
                openPrice=StockData[1][4]

        return openPrice

    def PrintRankStockHeader(self):
        print(','), #leave blank space for stock column 
        for s in self.Stocks: #print
            print('%s.rank,%s.price,' % (s,s)),
        print('')
    def PrintStockHeader(self):
        print(','),
        for s in self.Stocks: #print
            print('%s.stockprice,' % (s)),
        print('')
    def PrintRankHeader(self):
        print(','),
        for s in self.Stocks: #print
            print('%s.rank,' % (s)),
        print('')

    def StockRankMatrixTransposed(self): #useful for outputting data in suitable format for gnuplot
        self.PrintRankStockHeader()
        for d in self.Dates:
            print('%s' % (d)),
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    sys.stdout.write('%s' % (rank))
                print(','),
                stockprice=self.GetStockPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting.
                print(','),                 
            print('')

    def RankMatrixTransposed(self): #useful for outputting data in suitable format for gnuplot
        self.PrintRankHeader()
        for d in self.Dates:
            print('%s' % (d)),
            for s in self.Stocks:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    sys.stdout.write('%s' % (rank))
                print(','),
            print('')

    def StockMatrixTransposed(self): #useful for outputting data in suitable format for gnuplot
        self.PrintStockHeader()
        for d in self.Dates:
            print('%s' % (d)),
            for s in self.Stocks:
                stockprice=self.GetStockPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting.
                print(','),                 
            print('')



    def RankMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print('%s,' % (s)), #start new line with  the stock
            for d in self.Dates:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    #print('%s' % (rank)),
                    sys.stdout.write('%s' % (rank)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting. http://codingrecipes.com/print-without-a-new-line-or-space-in-python
            #if not at end of list then output ,
                print(','), #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL


    def StockMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print('%s,' % (s)), #start new line with  the stock
            for d in self.Dates:
                stockprice=self.GetStockPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting.
            #if not at end of list then output ,
                print(','), #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL
                
    def PrintDates(self):
        print(","),
        for d in self.Dates:
            print("%s," % (d)),



########### MAIN ############

import sys

import sqlite3
import getopt
#import YahooStockQuotes #http://stackoverflow.com/questions/714881/how-to-include-external-python-code-to-use-in-other-files
from YahooStockQuotes import get_historical_prices_plus_one_day
tableList=["BC20","IBD50","IBD8585","Top200Composite"]
database="IBDdatabase.sqlite"
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:l:t:d:', ['--input=',
                                                                        '--output=',
                                                                        '--loginfile=',
                                                                        '--table=',
                                                                        '--database=',
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
    elif opt == '--version':
        version = arg

#print(inputfilename,outputfilename,loginfile,table,database)
RM=RankMatrix(database,tableList[0])
#RM.PrintDates()
#RM.RankMatrix()

RM.StockMatrix()


#RM.RankMatrixTransposed()

