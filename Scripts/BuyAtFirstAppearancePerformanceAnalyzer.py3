#!/usr/bin/env/python
# -*- python -*- 
import sqlite3


"""
This program goes through the individual lists and 

"""


"""
TODO:
"""

sqlite3 IBDdatabase.sqlite  "select stockticker,rank,min(date) from BC20 group by stockticker"
for each entry, 

get stockprice, sp500 level on entry date
 retrieve from db or if not in db, get from yahoo and enter into db (is it 'cheaper' to just get the full historical prices, and enter into db and then query?)
get stockprice, sp500 level today


class  StockFirstAppearanceList:
    stockList=[]
    table=""
    firstAppearanceTable=""

    def __init__(self,table):
        self.table=table
        self.firstAppearanceTable=self.table+"FirstAppearance"
        self.dropFirstAppearanceDatabase()
        self.createFirstAppearanceDatabase()
        self.queryGetDateList()
        for date in self.dateList:
            self.currentDate=date
            self.queryGetTickerListforDate()
            outgoing,incoming=self.compareTickerLists()
            print(incoming,outgoing)

            for item in outgoing:
                id=self.findID(self.firstAppearanceTable,item)
                if id != -1:
                    self.insertEndData(self.firstAppearanceTable,id,self.currentDate)
            for item in incoming:
                self.insertBeginData(self.firstAppearanceTable,item,self.currentDate)


            self.moveTickerLists()
            self.previousDate=self.currentDate

    def dropFirstAppearanceDatabase(self):
        cursor=connection.cursor()
        print("Dropping continuous run table and starting anew. \n Remove after Testing")
        Query='DROP TABLE IF EXISTS  '+self.firstAppearanceTable
        cursor.execute(Query)
        

    def createFirstAppearanceDatabase(self):
        insertcursor=connection.cursor()
        Query='CREATE TABLE IF NOT EXISTS '+self.firstAppearanceTable+' (Id INTEGER PRIMARY KEY, StockTicker TEXT, Date TEXT, Rank INTEGER)'
        insertcursor.execute(Query)


    def insertBeginData(self,table,tickerRank,date):
        """
        Insert Beginning date and rank
        """
        insertcursor=connection.cursor()
        Query='CREATE TABLE IF NOT EXISTS '+table+' (Id INTEGER PRIMARY KEY, StockTicker TEXT, BeginDate TEXT, BeginRank INTEGER, EndDate TEXT, EndRank INTEGER)'
        insertcursor.execute(Query)
  
        Query='INSERT INTO '+table
        #        insertcursor.execute(Query+'(StockTicker,BeginDate) VALUES(null, ?, ?)', (symbol,date))
        insertcursor.execute(Query+'(StockTicker,BeginDate,BeginRank,EndDate,EndRank) VALUES( ?, ?,null,null,null)', (tickerRank[0],date))
        insertcursor.close()
        connection.commit()
        return 0

    def findID(self,table,tickerRank):
        #print(tickerRank) #D'oh! I previously called this variable ticker, yet it was a list. I needed just the ticker and not the rank. it was goofing up the sql query. http://stackoverflow.com/questions/12952546/sqlite3-interfaceerror-error-binding-parameter-1-probably-unsupported-type
        findcursor=connection.cursor()
        Query='SELECT Id FROM '+table + ' WHERE StockTicker="'+tickerRank[0]+'" AND EndDate is null'
        #print(Query)
        ticker='"'+tickerRank[0]+'"'
        #        findcursor.execute(Query+" WHERE StockTicker=? AND EndDate=null", (ticker,)) #need the trailing , to make it see a sequence/tuple otherwise it interprets the string as the tuple and splits teh characters of the string as teh tuple. see http://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
        
        #findcursor.execute(Query+" WHERE StockTicker=? AND EndDate is null", (ticker,)) 
        #findcursor.execute(Query+" WHERE EndDate is null")

        findcursor.execute(Query)
        data=-1
        while True:
            row=findcursor.fetchone()
            #print(row)
            if row == None:
                break
            data=row[0]
        #print(data)
        findcursor.close()        
        #data=-1
        #print("remove that")
        return data

    def insertEndData(self,table,recordID,date):
        """
        Insert Ending date and rank
        """
        insertcursor=connection.cursor()

        Query='UPDATE '+table
        insertcursor.execute(Query+' SET EndDate=? WHERE Id=?', (date,recordID))
        insertcursor.close()
        connection.commit()
        return 0


    def queryGetDateList(self,ticker):
        Query='SELECT MIN(date)  '+self.table+' WHERE stockticker LIKE "'+ticker+'"'
        querycursor=connection.cursor()
        querycursor.execute(Query)
        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            date=row[0]
            self.dateList.append(date)

    def queryGetTickerListforDate(self):
        Query='SELECT distinct(stockticker) FROM  '+self.table
        querycursor=connection.cursor()
        querycursor.execute(Query)

        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            data=row
            self.TickerList.append(data)



def usage():
    print("")
    print("i investment-amount=")
    print("o output=")
    print("leftover-investment-amount")
    print("s spillover")
    print("d database=")
    print("a alert=")


#-----------------MAIN-------------------------

""" 
"""

database="IBDdatabase.sqlite"
database="IBDTestDatabase.sqlite"


inputList=[ "IBD50"] #,"BC20","IBD8585","Top200Composite"]

inputList=[ "IBD50","BC20","IBD8585","Top200Composite"]
inputList=[ "BC20"]
for item in inputList:
    connection=sqlite3.connect(database)
    FirstAppearance=StockFirstAppearanceOnList(item)
    connection.commit()
quit()
