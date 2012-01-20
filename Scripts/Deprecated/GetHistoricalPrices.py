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
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data
#end def get_historical_prices_plus_one_day
def insert_data(symbol,date,data):
    connection=sqlite3.connect(database)
    cursor=connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS IBD50StockData (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close)')
    cursor.execute('INSERT INTO IBD50StockData VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
#end def insert_data

if (len(sys.argv) > 1):
    database=sys.argv[1]
else:
    database="IBDdatabase.sqlite"


connection=sqlite3.connect(database)
cursor=connection.cursor()
cursor.execute('select distinct(StockTicker) from IBD50 order by StockTicker ASC limit 1')
#for row in cursor.fetchall():
#    print row[0]
data=cursor.fetchall()
#print data
for item in data:
    ticker=item[0]
    print ticker
    cursor.execute('select Date from IBD50 where Stockticker=? order by Date ASC limit 5', [ticker])
    TimeData=cursor.fetchall()
    for row in TimeData:
#        print "%s" % (row["Date"])
   #     print row[0] #give 2011-11-28 without teh [0] we get (u'2011-11-28',)
        Date=row[0]

  #      print Date, year, month, day
        output=get_historical_prices(ticker, Date )
 #       print output#v,output[1[2]]#,output["High"]
        if output[0][4]=='Close':
            date=output[1][0]
            closingprice=output[1][4]
            print date,closingprice

#        print output[0][0]#need to make sure that the format doesn't change. ie. put if output[0][2]='Open' then enter data otherwise throw error
#        print row #gives (u'2011-11-28',)

    
#    print TimeData["Date"]
#cur = conn.execute("select age from people where first=? and last=?", [first, last]) example for properly constructing queries with variables

#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
        #year=Date[0:4]
        #month=Date[5:7]
        #day=Date[8:10]
