import sqlite3
#sqlite3 IBDdatabase.sqlite "select distinct(StockTicker) from IBD50 order by StockTicker ASC"

#curl -s "http://ichart.finance.yahoo.com/table.csv?s=YHOO&a=11&b=2&c=2005&d=11&e=2&f=2005&g=d&f=sl1&ignore=.csv"

import sys #for cmd line arguments
import urllib #for getting quotes from net
#
def get_historical_prices(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
#the date goes month(jan=0) day year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date[5:7]) - 1) + \
          'e=%s&' % str(int(date[8:10])) + \
          'f=%s&' % str(int(date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(date[5:7]) - 1) + \
          'b=%s&' % str(int(date[8:10])) + \
          'c=%s&' % str(int(date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data
#end def get_historical_prices
def get_historical_prices_plus_one_day(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Returns a nested list.
    """
#the date goes month(jan=0) day year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date[5:7]) - 1) + \
          'e=%s&' % str(int(date[8:10]) + 1) + \
          'f=%s&' % str(int(date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(date[5:7]) - 1) + \
          'b=%s&' % str(int(date[8:10]) + 1) + \
          'c=%s&' % str(int(date[0:4])) + \
          'ignore=.csv'
#    print url
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]

    return data
#end def get_historical_prices_plus_one_day
def insert_data(table,date,symbol,rank,data):
    insertcursor=connection.cursor()
    Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
    insertcursor.execute(Query)
    Open=int(round(float(data[1][1])*100))
    High=int(round(float(data[1][2])*100))
    Low=int(round(float(data[1][3])*100))
    Close=int(round(float(data[1][4])*100))
    Adj_Close=int(round(float(data[1][6])*100))
    Query='INSERT INTO '+table
    insertcursor.execute(Query+' VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (date,symbol,rank,data[1][0],Open,High,Low,Close,data[1][5],Adj_Close))
    insertcursor.close()
    return 0
#end def insert_data

def insert_error_data(table,date,symbol,rank):
    errorcursor=connection.cursor()
    Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
    errorcursor.execute(Query)
    Query='INSERT INTO '+table
    errorcursor.execute(Query+' VALUES(null, ?, ?, ?)', (date,symbol,rank))
    errorcursor.close()
#end def insert_error_data


def query_for_data(tablequery,tabledata,tableerror):
    Query='SELECT * FROM '+tablequery
    querycursor=connection.cursor()
    querycursor.execute(Query)
    while True:
        row=querycursor.fetchone()
        if row == None:
            break
#        print row
        ID=row[0] #not needed
        date=row[1]
        ticker=row[2]
        rank=row[3]
        output=get_historical_prices_plus_one_day(ticker, date )
        print date,ticker
        if output[0][0]!="Date": # a simple error check since this first field should be "Date"
            print "ERROR for ",ticker #enter this data into an errors database
            insert_error_data(tableerror,date,ticker,rank)
        else:
 #           print output
            if output[0][4]=='Close':
                quotedate=output[1][0]
                closingprice=output[1][4]
  #              print quotedate,closingprice
                error=insert_data(tabledata,date,ticker,rank,output)
    querycursor.close()
#end def query_for_data


if (len(sys.argv) > 1):
    database=sys.argv[1]
else:
    database="IBDdatabase.sqlite"
    table="IBD50StockData"
    tablequery1="IBD50"
    tableenterdata1="IBD50StockData"
    tableerror1="IBD50ErrorStockData"
    tablequery2="BC20"
    tableenterdata2="BC20StockData"
    tableerror2="BC20ErrorStockData"


connection=sqlite3.connect(database)

#query_for_data(tablequery1,tableenterdata1,tableerror1)
query_for_data(tablequery2,tableenterdata2,tableerror2)

connection.commit()

#if connection:
#    connection.close()
quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
