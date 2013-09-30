#!/usr/bin/env/python
# -*- python -*- 
import sqlite3



"""
TODO:
get the proper update syntax working
make a small test case for easier/faster testing
Entries should never have the same begindate and enddate. This is happening so there is a flaw in the logic, perform outgoing before incoming?
"""


class  StockContinuousRunOnList:
    dateList=[]
    previousTickerList=[]
    currentTickerList=[]
    table=""
    continousRunTable=""
    currentDate="somedate"
    previousDate="somedate"

    def __init__(self,table):
        self.table=table
        self.continuousRunTable=self.table+"ContinuousRun"
        self.dropContinuousRunDatabase()
        self.createContinuousRunDatabase()
        self.queryGetDateList()
        for date in self.dateList:
            self.currentDate=date
            self.queryGetTickerListforDate()
            outgoing,incoming=self.compareTickerLists()
            print(incoming,outgoing)
            """
            perform outgoing beffore incoming so you don't hit on the ercord you just inserted.
            """
            print("swap these two")
            for item in incoming:
                self.insertBeginData(self.continuousRunTable,item,self.currentDate)
            for item in outgoing:
                id=self.findID(self.continuousRunTable,item)
                if id != -1:
                    self.insertEndData(self.continuousRunTable,id,self.currentDate)


            self.moveTickerLists()
            self.previousDate=self.currentDate

    def dropContinuousRunDatabase(self):
        cursor=connection.cursor()
        Query='DROP TABLE IF EXISTS  '+self.continuousRunTable
        cursor.execute(Query)
        

    def createContinuousRunDatabase(self):
        insertcursor=connection.cursor()
        Query='CREATE TABLE IF NOT EXISTS '+self.continuousRunTable+' (Id INTEGER PRIMARY KEY, StockTicker TEXT, BeginDate TEXT, BeginRank INTEGER, EndDate TEXT, EndRank INTEGER)'
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
        print(tickerRank) #D'oh! I previously called this variable ticker, yet it was a list. I needed just the ticker and not the rank. it was goofing up the sql query. http://stackoverflow.com/questions/12952546/sqlite3-interfaceerror-error-binding-parameter-1-probably-unsupported-type
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
            print(row)
            if row == None:
                break
            data=row[0]
        print(data)
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

    def compareTickerLists(self):
        outgoing=[ i for i in self.previousTickerList if i not in self.currentTickerList ] 
        incoming=[ i for i in self.currentTickerList if i not in self.previousTickerList ]
        return outgoing,incoming


    def queryGetDateList(self):

        Query='SELECT DISTINCT(DATE) FROM  '+self.table+' ORDER BY DATE ASC'
        querycursor=connection.cursor()
        querycursor.execute(Query)
        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            date=row[0]
            self.dateList.append(date)

    def queryGetTickerListforDate(self):
        Query='SELECT stockticker,rank FROM  '+self.table+' WHERE DATE LIKE "'+self.currentDate+'"'
        querycursor=connection.cursor()
        querycursor.execute(Query)

        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            data=row
            self.currentTickerList.append(data)

    def moveTickerLists(self):
        """
        Move the new list to the old list, clear out the new list.
        This is done in preparation for getting the new list
        """
        self.previousTickerList=self.currentTickerList
        self.currentTickerList=[]



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

database="IBDdatabase.sqlite.copy"

inputList=[ "IBD50","BC20","IBD8585","Top200Composite"]
inputList=[ "IBD50"] #,"BC20","IBD8585","Top200Composite"]
inputList=[ "BC20"]
for item in inputList:
    connection=sqlite3.connect(database)
    ContinuousRun=StockContinuousRunOnList(item)
    connection.commit()
quit()
