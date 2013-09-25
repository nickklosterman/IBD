#!/usr/bin/env/python
# -*- python -*- 
import sqlite3
#sqlite3 IBDdatabase.sqlite "select distinct(StockTicker) from IBD50 order by StockTicker ASC"

#curl -s "http://ichart.finance.yahoo.com/table.csv?s=YHOO&a=11&b=2&c=2005&d=11&e=2&f=2005&g=d&f=sl1&ignore=.csv"

MonthsWith31Days = [1,3,5,7,8,10,12]
MonthsWith30Days = [4,6,9,11]
import datetime #for date and timedelta
import sys #for cmd line arguments
import urllib.request, urllib.parse, urllib.error #for getting quotes from net

def get_next_date(date):
    month=int(date[5:7])
    day=int(date[8:10]) 
    year=int(date[0:4])
    date_conv=datetime.date(year,month,day)
    oneday=datetime.timedelta(1)
    dateplusone=date_conv+datetime.timedelta(days=1)
    return dateplusone


def get_date(date):
    month=int(date[5:7])
    day=int(date[8:10]) 
    year=int(date[0:4])
    date_conv=datetime.date(year,month,day)
    return date_conv
    
#
def get_historical_prices(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    date=get_date(date)

#the date goes month(jan=0) day year
    # url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
    #       'd=%s&' % str(int(date[5:7]) - 1) + \
    #       'e=%s&' % str(int(date[8:10])) + \
    #       'f=%s&' % str(int(date[0:4])) + \
    #       'g=d&' + \
    #       'a=%s&' % str(int(date[5:7]) - 1) + \
    #       'b=%s&' % str(int(date[8:10])) + \
    #       'c=%s&' % str(int(date[0:4])) + \
    #       'ignore=.csv'
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date.month) - 1) + \
          'e=%s&' % str(int(date.day)) + \
          'f=%s&' % str(int(date.year)) + \
          'g=d&' + \
          'a=%s&' % str(int(date.month) - 1) + \
          'b=%s&' % str(int(date.day)) + \
          'c=%s&' % str(int(date.year)) + \
          'ignore=.csv'

    days = urllib.request.urlopen(url).readlines()
    data=[] #python3 method , 
    for day in days: #day[0] holds the fields names, day[1+] holds the data values
#        print(day) 
        dayStr = str(day, encoding='utf8')
        data.append( dayStr[:-2].split(','))
#    print(data)  #this is what 'data' looks like --> [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], ['2013-09-24', '110.09', '111.08', '108.15', '110.42', '596200', '110.4']]
    return float(data[1][4])
#end def get_historical_prices

_CounterSentinel = 5 #max possible holidays in a row where markets might be closed so we look at next day.
#we could avoid all this by just using the day of instead of day +1
def get_historical_prices_plus_one_day(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Returns a nested list.
    """
  #  print(date)
    done=False
    counter=0
    while not done:
        date=get_next_date(str(date))
 ## I NEED TO AVOID ANY DATE THAT THE MARKET IS CLOSED
 #   print(date)
#the date goes month(jan=0) day year
        url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
            'd=%s&' % str(int(date.month) - 1) + \
            'e=%s&' % str(int(date.day) ) + \
            'f=%s&' % str(int(date.year)) + \
            'g=d&' + \
            'a=%s&' % str(int(date.month) - 1) + \
            'b=%s&' % str(int(date.day) ) + \
            'c=%s&' % str(date.year) + \
            'ignore=.csv'
        print( url)
        try:
            days = urllib.request.urlopen(url).readlines()
            done=True
            data=[] #python3 method
            for day in days: #day[0] holds the fields names, day[1+] holds the data values
#        print(day) 
                dayStr = str(day, encoding='utf8')
                data.append( dayStr[:-2].split(','))
        except urllib.error.HTTPError as err:
            if err.code == 404: #try incrementing date again
                counter+=1
                if (counter > _CounterSentinel) :
                    print("uh oh")
                    done=True
                    data=[["error"]]
                    #days = urllib.request.urlopen('http://www.djinnius.com').readlines() #get some byte data that will fail and throw an error. This is awful that I'm relying on an outside source to help set an error. I should hand define the error (I tried using buffer() and memoryview() since using str(,encoding) expects a vuffer,bytearray or byte object but no dice. I also could try to move the 
            else:
                raise
    return data
#end def get_historical_prices_plus_one_day


def query_for_entry(table,date,symbol,rank):
    querycursor=connection.cursor()
    Query='SELECT COUNT(*) FROM  '+table+' WHERE stockticker LIKE "'+symbol+'" AND date LIKE "'+date+'" and rank = '+str(rank)
    querycursor.execute(Query)
    row=querycursor.fetchone()
    numrecords=int(row[0])
    return numrecords

def insert_error_data(table,date,symbol,rank):
    errorcursor=connection.cursor()
    Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
    errorcursor.execute(Query)
    Query='INSERT INTO '+table
    errorcursor.execute(Query+' VALUES(null, ?, ?, ?)', (date,symbol,rank))
    errorcursor.close()
#end def insert_error_data

def check_tables_exist(table):
    cursor=connection.cursor()
    Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
    print(Query)
    cursor.execute(Query)
    row=cursor.fetchone()
    if row == None or int(row[0]==0):
        if table=="tablelist[1]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[1]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
        if table=="tablelist[2]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[2]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
        cursor.execute(Query)
    else:
        print("returned None")
                
    cursor.close()


def query_for_data(table):
    check_tables_exist(table)    
    Query='SELECT distinct(date) FROM '+table
    querycursor1=connection.cursor()
    querycursor1.execute(Query)
    while True: #needed so we can use the 'break' in case a row is empty
        row=querycursor1.fetchone()
        if row == None:
            break
        date=row[0]
        Query2="Select stockticker,rank from "+table+" where date=\""+date+"\""
        print(" {\"portfolioName\":\"%s %s\", \"display\":\"yes\", \"portfolioStocks\":[" % (table,date))
        querycursor2=connection.cursor()
        querycursor2.execute(Query2)
        while True: #needed so we can use the 'break' in case a row is empty
            row2=querycursor2.fetchone()
            if row2 == None:
                break
            ticker=row2[0]
            rank=row2[1]
            dateSplit=date.split('-')
            purchaseprice=get_historical_prices(ticker,date)*10 #buy 10 shares
            if table=="IBD50" and rank!=50:
                print('{ "ticker": "%s", "shares": 10, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":7,"commissionToSell":7,rank:%i}, ' % ( ticker,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],rank))
            else:
                print('{ "ticker": "%s", "shares": 10, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":7,"commissionToSell":7,rank:50} ' % ( ticker,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0]))
        print("]},")
        querycursor2.close()
    querycursor1.close()
#end def query_for_data

#-----------------MAIN-------------------------
if (len(sys.argv) > 1):
    database=sys.argv[1]
else:
    database="IBDdatabase.sqlite"
    inputList=["IBD50","BC20","IBD8585","Top200Composite"]
    for item in inputList:
        connection=sqlite3.connect(database)
        query_for_data(item)
        connection.commit()

quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
