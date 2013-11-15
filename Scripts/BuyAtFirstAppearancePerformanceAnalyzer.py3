#!/usr/bin/env/python
# -*- python -*- 
import sqlite3


"""
This program goes through the individual lists and 

"""


"""
TODO:
"""
"""
sqlite3 IBDdatabase.sqlite  "select stockticker,rank,min(date) from BC20 group by stockticker"
for each entry, 

get stockprice, sp500 level on entry date
 retrieve from db or if not in db, get from yahoo and enter into db (is it 'cheaper' to just get the full historical prices, and enter into db and then query?)
get stockprice, sp500 level today
"""

from YahooStockQuotes import getHistoricalStockData
#from YahooStockQuotes import get_historical_prices
class  StockFirstAppearance:
    table=""
    firstAppearanceList=[]

    def __init__(self,table):
        self.table=table
        self.queryGetStockFirstAppearanceList()

        
    def printForStockTracker(self):
        counter=1
        stopCounter=len(self.firstAppearanceList)
        print('{"portfolioName":"%s", "display:"yes", "portfolioStocks": [' % (self.table))
        for item in self.firstAppearanceList:
            #print(item)
            ticker=item[0]
            rank=item[1]
            date=item[2]
            olddate=item[2].split('-')
            newdate=olddate[1]+'/'+olddate[2]+'/'+olddate[0]
            #openPrice=get_historical_prices(item[0],date)
            stockData=getHistoricalStockData(item[0],date)
            #print(stockData)
            #print('{"ticker":"%s","shares":1,"rank":%d, totalpurchasePrice": %f, "purchaseDate":"%s","commissionToBuy":0,"commissionToSell":0}' % (ticker,rank,float(stockData[1][1]),newdate),end="")#item[2]))
            if stockData!="None":
                openPrice=stockData[1][1]
            else:
                openPrice=0
            #print('{"ticker":"%s","shares":1,"rank":%d, totalpurchasePrice": %s, "purchaseDate":"%s","commissionToBuy":0,"commissionToSell":0}' % (ticker,rank,(stockData[1][1]),newdate),end="")
            print('{"ticker":"%s","shares":1,"rank":%d, totalpurchasePrice": %s, "purchaseDate":"%s","commissionToBuy":0,"commissionToSell":0}' % (ticker,rank,openPrice,newdate),end="")
                
            if counter!=stopCounter:
                print(',')
            else:
                print('')
            counter+=1

        print(']}')

    def queryGetStockFirstAppearanceList(self):
        querycursor=connection.cursor()
        Query='SELECT stockticker,rank,min(date) from '+self.table+' GROUP BY stockticker'
        querycursor.execute(Query)
        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            data=row
            self.firstAppearanceList.append(data)


#-----------------MAIN-------------------------

""" 
"""

test=0

if test:
    
    database="IBDTestDatabase.sqlite"
    inputList=[ "IBD50"] #,"BC20","IBD8585","Top200Composite"]
    inputList=[ "BC20"]
else:
    database="IBDdatabase.sqlite"
    inputList=[ "IBD50","BC20","IBD8585","Top200Composite"]

counter=1
stopCounter=len(inputList)
print('{"portfolio":[')
for item in inputList:
    connection=sqlite3.connect(database)
    FirstAppearance=StockFirstAppearance(item)
    FirstAppearance.printForStockTracker()
    #connection.commit()
    if (counter != stopCounter):
        print(',')
    counter+=1
print(']}')
quit()
