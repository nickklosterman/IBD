#!/usr/bin/env/python
# -*- python -*- 
import sqlite3

#curl -s "http://ichart.finance.yahoo.com/table.csv?s=YHOO&a=11&b=2&c=2005&d=11&e=2&f=2005&g=d&f=sl1&ignore=.csv"

import sys #for cmd line arguments
import urllib.request, urllib.parse, urllib.error #for getting quotes from net

from YahooStockQuotes import getHistoricalStockPrices 


def queryForExistenceOnTableDateSymbol(table,date,symbol):
    """
    QQuery the database for the number of records present for a particular ticker on a given date with a certain rank with a certain quotedate
    """
    querycursor=connection.cursor()
    Query='SELECT COUNT(*) FROM  '+table+' WHERE stockticker LIKE "'+symbol+'" AND date LIKE "'+date+'"'
    querycursor.execute(Query)
    numrecords=0
    while True:
        row=querycursor.fetchone()
        if row == None:
            break
        numrecords=int(row[0])
    return numrecords


def insertData(table,date,symbol,rank,data):
    """
    insert dollar values as cent values (integers) since sqlite doesn't have a decimal datatype
    No longer has QuoteDate field
    """
    insertcursor=connection.cursor()
    #Table created in check_tables_exist
    #Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER,  Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
    #insertcursor.execute(Query)
    Open=int(round(float(data[1][1])*100))
    High=int(round(float(data[1][2])*100))
    Low=int(round(float(data[1][3])*100))
    Close=int(round(float(data[1][4])*100))
    Adj_Close=int(round(float(data[1][6])*100))
    Query='INSERT INTO '+table
    insertcursor.execute(Query+' VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date,symbol,rank,Open,High,Low,Close,data[1][5],Adj_Close))
    insertcursor.close()
    connection.commit()
    return 0
#end def insert_data

def insert_error_data(table,date,symbol,rank):
    """
    Insert the date symbol and rank of any stock that an error was produced on
    """
    errorcursor=connection.cursor()
    Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
    errorcursor.execute(Query)
    Query='INSERT INTO '+table
    errorcursor.execute(Query+' VALUES(null, ?, ?, ?)', (date,symbol,rank))
    errorcursor.close()
    #connection.commit()
#end def insert_error_data

def dropStockDataStockDataErrorTable():
    """

    """
    errorcursor=connection.cursor()
    Query='DROP TABLE IF EXISTS StockData'
    errorcursor.execute(Query)
    Query='DROP TABLE IF EXISTS StockDataError'
    errorcursor.execute(Query)
    errorcursor.close()
    #connection.commit()
#end def insert_error_data

def check_tables_exist(tablelist):
    cursor=connection.cursor()
    for table in tablelist:
        Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
        #print(Query)
        cursor.execute(Query)
        row=cursor.fetchone()
        if row == None or int(row[0]==0):
            if table==tablelist[1]:
                #                Query='CREATE TABLE IF NOT EXISTS '+tablelist[1]+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
                Query='CREATE TABLE IF NOT EXISTS '+tablelist[1]+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
            if table==tablelist[2]:
                Query='CREATE TABLE IF NOT EXISTS '+tablelist[2]+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
            cursor.execute(Query)
        else:
            print("returned None")
                
    cursor.close()



def query_for_data(tablelist):
    """
    Loop over all rows in the provided table and get the historical price plus one day and insert that data into our data table
    """
    check_tables_exist(tablelist)    
    """ table we are querying """
    tablequery=tablelist[0]
    """ table we will insert stock data  into """ 
    tabledata=tablelist[1] 
    """ table that error ticker/data/rank will be placed in """
    tableerror=tablelist[2] 

    Query='SELECT * FROM '+tablequery

    
    dateTickerRankCursor=connection.cursor()
    dateTickerRankCursor.execute(Query)

    while True: #needed so we can use the 'break' in case a row is empty
        row=dateTickerRankCursor.fetchone()
        if row == None:
            break

        ID=row[0] #not used/needed
        date=row[1]
        ticker=row[2]
        rank=row[3]
        """
        repeat the operation, but get the data for the present day
        """
        numrecords= queryForExistenceOnTableDateSymbol(tabledata,date,ticker)
        if (numrecords==0): #retrieve and insert data if record isn't present
            output=getHistoricalStockPrices(ticker, date )
            #print(date,ticker,output)
            if len(output)!=2 or output[0][0]!="Date": # a simple error check since this first field should be "Date"
                print("ERROR for ",ticker) #enter this data into an errors database
                print(row,output)
                insert_error_data(tableerror,date,ticker,rank)
            else:
                if float(output[1][4])>0: #make sure field for closing price is a number
                    error=insertData(tabledata,date,ticker,rank,output)
    dateTickerRankCursor.close()
#end def query_for_data

def queryForData(table):
    """
    Loop over all rows in the provided table and get the historical price and insert that data into our data table
    All stock data goes into StockData and StockDataError
    The ContinuousRun tables are subsets of the full tables and therefore they don't need to be processed.
    Each list happens on a separate day so we don't need to check for duplicate entries as that *shouldn't* ever happen.
    """

    """ table we are querying """
    tablequery=table
    """ table we will insert stock data  into """ 
    tabledata="StockData"
    """ table that error ticker/data/rank will be placed in """
    tableerror="StockDataError"

    tablelist=[]
    tablelist.append(tablequery)
    tablelist.append(tabledata)
    tablelist.append(tableerror)

    check_tables_exist(tablelist)    

    Query='SELECT * FROM '+tablequery
    
    dateTickerRankCursor=connection.cursor()
    dateTickerRankCursor.execute(Query)

    while True: #needed so we can use the 'break' in case a row is empty
        row=dateTickerRankCursor.fetchone()
        if row == None:
            break

        ID=row[0] #not used/needed
        date=row[1]
        ticker=row[2]
        rank=row[3]
#        print(row)
        """
        repeat the operation, but get the data for the present day
        """
        numrecords= queryForExistenceOnTableDateSymbol(tabledata,date,ticker)
        if (numrecords==0): #retrieve and insert data if record isn't present
            output=getHistoricalStockPrices(ticker, date )
            #print(date,ticker,output)
            if len(output)!=2 or output[0][0]!="Date": # a simple error check since this first field should be "Date"
                print("ERROR for ",ticker) #enter this data into an errors database
                print(row,output)
                insert_error_data(tableerror,date,ticker,rank)
            else:
                if float(output[1][4])>0: #make sure field for closing price is a number
                    error=insertData(tabledata,date,ticker,rank,output)
        #else:
        #    print('There are %s duplicate records.' % numrecords)




    dateTickerRankCursor.close()
#end def query_for_data



#-----------------MAIN-------------------------
if (len(sys.argv) > 1):
    database=sys.argv[1]
else:
    database="IBDTestDatabase.sqlite"
    inputList=[["IBD50","IBD50StockData","IBD50StockDataError"],["BC20","BC20StockData","BC20StockDataError"],["IBD8585","IBD8585StockData","IBD8585StockDataError"],["Top200Composite","Top200CompositeStockData","Top200CompositeStockDataError"]]



#enter all data into "StockData" table ....hmmm  I don't benefit from eliminating redundant values so how much of a performance hit am I willing to take to keep all data in one table?
    inputList=[["IBD50","StockData","StockDataError"],["BC20","BC20StockData","BC20StockDataError"],["IBD8585","IBD8585StockData","IBD8585StockDataError"],["Top200Composite","Top200CompositeStockData","Top200CompositeStockDataError"]]
    inputList=[["BC20","BC20StockData","BC20StockDataError"]]
#    print("Using restricted set")
#    inputList=[["Top200Composite","Top200CompositeStockData","Top200CompositeStockDataError"]]
    for item in inputList:
        connection=sqlite3.connect(database)
        
        if 0:
            print("DROPPING Table StockData and StockDataError!!!!!!!!!!!")
            dropStockDataStockDataErrorTable()

        if 0:
            query_for_data(item)
        if 1:
            queryForData(item[0])

quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
