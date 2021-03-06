#!/usr/bin/env/python
# -*- python -*- 
import sqlite3

"""
This program loops through the provided database tables and outputs (almost) valid JSON for ingestion by my StockTrackerJSON.py3 script
the final , in the list will need to be removed to make the output valid JSON. I need to rewrite the logic so that the output is valid json.

The program allows you to specify an investment amount for each stock in the list, and the maximum number of whole shares
that can be purchased is bought with that amount. 
You can specify that any leftover money is then added to the next purchase "bucket."
"""

#sqlite3 IBDdatabase.sqlite "select distinct(StockTicker) from IBD50 order by StockTicker ASC"


#curl -s "http://ichart.finance.yahoo.com/table.csv?s=YHOO&a=11&b=2&c=2005&d=11&e=2&f=2005&g=d&f=sl1&ignore=.csv"

MonthsWith31Days = [1,3,5,7,8,10,12]
MonthsWith30Days = [4,6,9,11]
import datetime #for date and timedelta
import sys #for cmd line arguments
import urllib.request, urllib.parse, urllib.error #for getting quotes from net

from YahooStockQuotes import getHistoricalStockData #Prices 


def get_date(date):
    month=int(date[5:7])
    day=int(date[8:10]) 
    year=int(date[0:4])
    date_conv=datetime.date(year,month,day)
    return date_conv
    
#

def queryDatabaseForOpenPrice(symbol,date,table):
    #table="StockData"
    openPrice=-1
    if check_tables_exist(table+'_'+symbol+'_Master') :
        Query='SELECT Open FROM '+table
        Query='SELECT Open FROM  '+table+' WHERE  date LIKE "'+date+'" AND StockTicker LIKE "'+symbol+'"'
        Query='SELECT Open FROM '+table+'_'+symbol+'_Master WHERE date LIKE "'+date+'"'
        querycursor1=connection.cursor()
        querycursor1.execute(Query)
        while True: #needed so we can use the 'break' in case a row is empty
            row=querycursor1.fetchone()
            if row == None:
                break
            openPrice=row[0]
    return openPrice


def getHistoricalPrice(symbol,date,table):
    openPrice=queryDatabaseForOpenPrice(symbol,date,table)
    if openPrice!=-1:
        return openPrice
    else:
        # Arrg, I currently have the YahooStockQuotes.getHistoricalStockData() print the error messages ; Screw it removing the print(err) output
        data=getHistoricalStockData(symbol,date) #getHistoricalStockPrices(symbol,date)
        if data!="None":
            return float(data[1][4])
        else:
            return 0

def check_tables_exist(table):
    existsFlag=True
    cursor=connection.cursor()
    Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
    cursor.execute(Query)
    row=cursor.fetchone()
    if row == None or int(row[0]==0):
        existsFlag=False
        if table=="tablelist[1]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[1]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER, QuoteDate TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
        if table=="tablelist[2]:":
            Query='CREATE TABLE IF NOT EXISTS +tablelist[2]+ (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)'
        cursor.execute(Query)
    #else:
    #    print("returned None")
                
    cursor.close()
    return existsFlag


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
        #OutputStream((" {\"portfolioName\":\"%s %s\", \"display\":\"yes\", \"portfolioStocks\":[" % (table,date)))
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
            sharePrice=getHistoricalPrice(ticker,date,table) #get_historical_prices(ticker,date)
            """
            Rest the commissions
            """
            commissionToBuy=7.0
            commissionToSell=7.0
            if (sharePrice != -1.0 and sharePrice != 0 ):
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
                #OutputStream(('{ "ticker": "%s", "shares": %d, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":%0.2f,"commissionToSell":%0.2f,"rank":%i,"sharePurchasePrice":%0.2f}, ' % ( ticker,sharesToBuy,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],commissionToBuy,commissionToSell,rank,sharePrice)))
            else:
                #print(rank,recordCountForDate)
                print('{ "ticker": "%s", "shares": %d, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":%0.2f,"commissionToSell":%0.2f,"rank":%i,"sharePurchasePrice":%0.2f} ' % ( ticker,sharesToBuy,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],commissionToBuy,commissionToSell,rank,sharePrice))
                #OutputStream(('{ "ticker": "%s", "shares": %d, "totalPurchasePrice": %0.2f, "purchaseDate": "%s/%s/%s","commissionToBuy":%0.2f,"commissionToSell":%0.2f,"rank":%i,"sharePurchasePrice":%0.2f} ' % ( ticker,sharesToBuy,purchaseprice,dateSplit[1],dateSplit[2],dateSplit[0],commissionToBuy,commissionToSell,rank,sharePrice)))

        """output ending elements to enclose the json array and element
        --> I need a way to sstrip off that trailing , when it is the last record
        it works ok looping over all the tables, it is just the last comma needs to be stripped out to make the output fully valid json 
        """
        print("],\"uninvestedMoney\":%0.2f}," % (leftoverInvestmentAmount)) 
        #OutputStream(("],\"uninvestedMoney\":%0.2f}," % (leftoverInvestmentAmount)) )
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


#def #OutputStream(arg):
    fileOutput+=arg

#-----------------MAIN-------------------------




#def main


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
database="IBDdatabase.sqlite.copy"
outputfilename="output.json"
outputFilenameFlag=False
output=""
errorLog=[]
global fileOutput
fileOutput=""
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
        outputFilenameFlag=True
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

#OutputStream("{\"portfolio\":  [")
inputList=["IBD50","BC20","IBD8585","Top200Composite"]
#inputList=["BC20"]
#inputList=["BC20","IBD8585","Top200Composite"]
for item in inputList:
    connection=sqlite3.connect(database)
    query_for_data(item)
    connection.commit()

print("]}")


#OutputStream("]}")

if outputFilenameFlag:
    fileHandle=open(outputFilename,'w')
    fileHandle.write(output)
    fileHandle.close()


quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
