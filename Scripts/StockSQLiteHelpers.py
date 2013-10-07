
from YahooStockQuotes import getHistoricalStockPrices 

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
    return openPrice

def getHistoricalOpenPrice(symbol,date):
    openPrice=queryDatabaseForOpenPrice(symbol,date)
    if openPrice!=-1:
        return openPrice
    else:
        data=getHistoricalStockPrices(symbol,date)
        if data!="None":
            return data[1][4]
        else:
            return 0
