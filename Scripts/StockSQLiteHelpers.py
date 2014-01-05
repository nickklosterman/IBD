'''
contains helper functions:
queryDatabaseForOpenPrice : get the Open price for a stock on a particular date
queryDatabaseForCount :  get the count of data for a stock on a particular date (used by getHistoricalData to see if the database contains any data for that stock/date pair)
getHistoricalData :   
insertStockData : inserts ticker,rank,date and historical stock data into a table.
getHistoricalOpenPrice : first checks for the data in the database, otherwise performs a call to the yahoo api

'''
from YahooStockQuotes import getHistoricalStockData  

import sqlite3

def queryDatabaseForOpenPrice(symbol,date):
    connection=sqlite3.connect('IBDdatabase.sqlite')
    table="StockData"
    #check_tables_exist(table)    
    Query='SELECT Open FROM '+table
    Query='SELECT Open FROM  '+table+' WHERE  date LIKE "'+date+'" AND StockTicker LIKE "'+symbol+'"'
    querycursor1=connection.cursor()
    querycursor1.execute(Query)
    openPrice=-1
    while True: #needed so we can use the 'break' in case a row is empty
        row=querycursor1.fetchone()
        if row == None:
            break
        openPrice=row[0]
    return openPrice/100 #the price is stored in cents since the sqlite doesn't have a decimal data type.

def queryDatabaseForCount(symbol,date):
    connection=sqlite3.connect('IBDdatabase.sqlite')
    table="StockData"
    #check_tables_exist(table)    
    Query='SELECT count(*) FROM  '+table+' WHERE  date LIKE "'+date+'" AND StockTicker LIKE "'+symbol+'"'
    querycursor1=connection.cursor()
    querycursor1.execute(Query)
    existence=0
    while True: #needed so we can use the 'break' in case a row is empty
        row=querycursor1.fetchone()
        if row == None:
            break
        existence=row[0]
    return existence



def getHistoricalData(symbol,date):
    if (queryDatabaseForCount(symbol,date)>0):
        #we should get the data from Yahoo and return that
        return 0 
    else:
        return getHistoricalStockData(symbol,date)

def getHistoricalOpenPrice(symbol,date):
    openPrice=queryDatabaseForOpenPrice(symbol,date)
    if openPrice!=-1:
        return openPrice
    else:
        data=getHistoricalStockData(symbol,date)
        if data!="None":
            #we should also save the data in the database 
            return data[1][4]
        else:
            return 0

def insertStockData(table,date,symbol,rank,data):
    """
    insert dollar values as cent values (integers) since sqlite doesn't have a decimal datatype
    No longer has QuoteDate field
    """
    connection=sqlite3.connect('IBDdatabase.sqlite')
    insertcursor=connection.cursor()
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
