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
    output=-1.0
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
    try:
        days = urllib.request.urlopen(url).readlines()
        data=[] #python3 method , 
        for day in days: #day[0] holds the fields names, day[1+] holds the data values
            #        print(day) 
            dayStr = str(day, encoding='utf8')
            data.append( dayStr[:-2].split(','))
            #    print(data)  #this is what 'data' looks like --> [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], ['2013-09-24', '110.09', '111.08', '108.15', '110.42', '596200', '110.4']]
        output=float(data[1][4])
    except urllib.error.HTTPError as err:
        if err.code == 404: #try incrementing date again
            import traceback
            errorLog.append(err)
                #days = urllib.request.urlopen('http://www.djinnius.com').readlines() #get some byte data that will fail and throw an error. This is awful that I'm relying on an outside source to help set an error. I should hand define the error (I tried using buffer() and memoryview() since using str(,encoding) expects a vuffer,bytearray or byte object but no dice. I also could try to move the 
    except urllib.error.URLError as err:
        import traceback
        errorLog.append(err)
    except Exception as err:
        import traceback
        errorLog.append(err)
    else:
        #raise
        import traceback
        

    return output
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


def check_tables_exist(table):
    cursor=connection.cursor()
    Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
    cursor.execute(Query)
    row=cursor.fetchone()
    if row == None or int(row[0]==0):
        if table=="tablelist[1]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[1]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
        if table=="tablelist[2]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[2]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
        cursor.execute(Query)
    #else:
    #    print("returned None")
                
    cursor.close()


def queryTableDateForCount(table,date):
    """
    QQuery the database for the number of records present for a particular ticker on a given date with a certain rank
    """
    querycursor=connection.cursor()
    Query='SELECT COUNT(*) FROM  '+table+' WHERE  date LIKE "'+date+'"'
    querycursor.execute(Query)
    row=querycursor.fetchone()
    numrecords=int(row[0])
    return numrecords


def query_for_data(table):
    check_tables_exist(table)    
    Query='SELECT distinct(date) FROM '+table
    querycursor1=connection.cursor()
    querycursor1.execute(Query)
    sharesToBuy=10
    commissionToBuy=7.0
    commissionToSell=7.0
    leftoverInvestmentAmount=0.0
    while True: #needed so we can use the 'break' in case a row is empty
        row=querycursor1.fetchone()
        if row == None:
            break
        date=row[0]
        recordCountForDate=queryTableDateForCount(table,date)
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
            sharePrice=get_historical_prices(ticker,date)
            """
            Rest the commissions
            """
            commissionToBuy=7.0
            commissionToSell=7.0

            if (sharePrice != -1.0):
                if(leftoverInvestmentAmountFlag):
                    sharesToBuy=math.floor((investmentAmount-commissionToBuy+leftoverInvestmentAmount)/sharePrice)
                else :
                    sharesToBuy=math.floor((investmentAmount-commissionToBuy)/sharePrice)
                leftoverInvestmentAmount=investmentAmount-sharesToBuy*sharePrice+leftoverInvestmentAmount

                purchaseprice=sharePrice*sharesToBuy+commissionToBuy
                #  print(sharesToBuy,leftoverInvestmentAmount,purchaseprice,sharePrice)
            else:
                sharesToBuy=0
                purchaseprice=0
                commissionToBuy=0
                commissionToSell=0
                sharePrice=0
            if rank!=recordCountForDate: 
                #                print(rank,recordCountForDate)
                print('{ "ticker": "%s", "shares": %d, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":%0.2f,"commissionToSell":%0.2f,"rank":%i,"sharePurchasePrice":%0.2f}, ' % ( ticker,sharesToBuy,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],commissionToBuy,commissionToSell,rank,sharePrice))
            else:
                #print(rank,recordCountForDate)
                print('{ "ticker": "%s", "shares": %d, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":%0.2f,"commissionToSell":%0.2f,"rank":%i,"sharePurchasePrice":%0.2f} ' % ( ticker,sharesToBuy,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],commissionToBuy,commissionToSell,rank,sharePrice))

        """output ending elements to enclose the json array and element"""
        print("],\"uninvestedMoney\":%0.2f}," % (leftoverInvestmentAmount)) 
        leftoverInvestmentAmount=0.0
        querycursor2.close()
    querycursor1.close()
#end def query_for_data


def usage():
    print("")
    print("i investment-amount=")
    print("o output=")
    print("leftover-investment-amount")
    print("s spillover")
    print("d database=")
    print("a alert=")


#-----------------MAIN-------------------------
import getopt  #for command line options
#import sys
import math #for floor


""" 
investmentAmount is the amount that is used to calculate the number of shares to purchase. Fractional shares are not allowed. Any unused money can then cascade to the next investment purchase, being added to the investment amount. This is enabled with the leftoverInvestmentAmountFlag  
using the leftoverInvestmentAmountFlag will mean that the 1st stock will be always a bit artificially low since it wont' have any leftover amounts to take advantage of.
if the investmentAmount is less than the max price of any of the shares of stock then you won't buy any!!!

I was contemplating adding the option to specify the number of stock shares to buy, but that seems a bit ridiculous.....although for some reason that idea intrigues me.
"""
investmentAmount=1000
investmentAmountFlag=False
#leftoverInvestmentAmount=0.0
leftoverInvestmentAmountFlag=False
database="IBDdatabase.sqlite"

errorLog=[]

#print(sys.argv[1:])

#pretty much straight from : http://docs.python.org/release/3.1.5/library/getopt.html
#took me a while to catch that for py3k that you don't need the leading -- for the long options
#sadly optional options aren't allowed. says it in the docs :( http://docs.python.org/3.3/library/getopt.html
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:a:i:lsd:', ['investment-amount=',
                                                                        'output=',
                                                                        'leftover-investment-amount',
                                                                        'spillover',
                                                                        'database=',
                                                                        'alert='
                                                                ])
except getopt.GetoptError as err:
    print( str(err)) # will print something like "option -a not recognized"                                         
    usage()                                                                                                  
    sys.exit(2)

for opt, arg in options:
    if opt in ('-i', '--investment-amount'):
        investmentAmount=float(arg)
        investmentAmountFlag=True
    elif opt in ('-o', '--output'):
        outputfilename=arg
    elif opt in ('-d', '--database'):
        database=arg
    elif opt in ('-s', '--spillover'):
        leftoverInvestmentAmountFlag=True
    elif opt in ('-a', '--alert'): #check for stocks where loss is > 8 %
        alertflag=True
        try:
            alertPercent=float(arg) #will it break if an opt isn't specified?
        except ValueError:
            alertPercent=8
        if alertPercent > 1:
            alertPercent=alertPercent/100;
    else:
        assert False, "unhandled option"

print("{\"portfolio\":  [")
#inputList=["IBD50","BC20","IBD8585","Top200Composite"]
inputList=["BC20","IBD8585","Top200Composite"]
for item in inputList:
    connection=sqlite3.connect(database)
    query_for_data(item)
    connection.commit()
print("]}")
quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
