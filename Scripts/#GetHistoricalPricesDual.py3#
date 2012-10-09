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
    
#
def get_historical_prices(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    print(date)
    date=get_next_date(date)
    print(date)
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
    days = urllib.request.urlopen(url).readlines()
    data=[] #python3 method , 
    for day in days: #day[0] holds the fields names, day[1+] holds the data values
#        print(day) 
        dayStr = str(day, encoding='utf8')
        data.append( dayStr[:-2].split(','))
    return data
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

#insert dollar values as integers since sqlite doesn't have a decimal datatype
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

def check_tables_exist(tablelist):
    cursor=connection.cursor()
    for table in tablelist:
        Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
        print(Query)
        cursor.execute(Query)
        row=cursor.fetchone()
        if row == None or int(row[0]==0):
            if table==tablelist[1]:
                Query='CREATE TABLE IF NOT EXISTS '+tablelist[1]+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
            if table==tablelist[2]:
                Query='CREATE TABLE IF NOT EXISTS '+tablelist[2]+' (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
            cursor.execute(Query)
        else:
            print("returned None")
                
    cursor.close()


#def query_for_data(tablequery,tabledata,tableerror):
def query_for_data(tablelist):
    check_tables_exist(tablelist)    
    tablequery=tablelist[0]
    tabledata=tablelist[1]
    tableerror=tablelist[2]
    print(tablequery,tabledata,tableerror)
    Query='SELECT * FROM '+tablequery
#    Query='SELECT * FROM BC20 WHERE DATE="2012-07-31"'
#    Query='SELECT * FROM BC20 WHERE ID>735 Limit 100'
#    Query='SELECT * FROM IBD50 WHERE ID>2340 Limit 100'
    querycursor=connection.cursor()
    querycursor.execute(Query)
    rowcounter=0

    while True: #needed so we can use the 'break' in case a row is empty
        print(rowcounter)
        rowcounter+=1
        row=querycursor.fetchone()
        if row == None:
            break
    #        print row
        ID=row[0] #not used/needed
        date=row[1]
        ticker=row[2]
        rank=row[3]
    #        print(ID,date,ticker)
        numrecords=query_for_entry(tabledata,date,ticker,rank)
        if (numrecords==0): #retrieve and insert data if record isn't present
            output=get_historical_prices_plus_one_day(ticker, date )
            print(ID,date,ticker,output)
            if len(output)!=2 or output[0][0]!="Date": # a simple error check since this first field should be "Date"
                print("ERROR for ",ticker) #enter this data into an errors database
                print(row,output)
                insert_error_data(tableerror,date,ticker,rank)
            else:
                if float(output[1][4])>0: #make sure field for closing price is a number
#                if output[0][4]=='Close': #or could do if int(output[1][2])>0 
#                    quotedate=output[1][0]
 #                   closingprice=output[1][4]
                    error=insert_data(tabledata,date,ticker,rank,output)
        else:
            print('There are %s duplicate records.' % numrecords)
    querycursor.close()
#end def query_for_data

#-----------------MAIN-------------------------
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
#I could simplify this by updating the "tablequery" table with the stock data, alternately I could do a join to cut down on redundant data.
    inputList=[["IBD50","IBD50StockData","IBD50StockDataError"],["BC20","BC20StockData","BC20StockDataError"],["IBD8585","IBD8585StockData","IBD8585StockDataError"],["Top200Composite","Top200CompositeStockData","Top200CompositeStockDataError"]]
#    print("Using restricted set")
#    inputList=[["Top200Composite","Top200CompositeStockData","Top200CompositeStockDataError"]]
    for item in inputList:
        connection=sqlite3.connect(database)
        query_for_data(item)
#query_for_data(tablequery1,tableenterdata1,tableerror1)
#query_for_data(tablequery2,tableenterdata2,tableerror2)
        connection.commit()

#if connection:
#    connection.close()
quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
