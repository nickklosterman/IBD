#!/usr/bin/env/python
# -*- python -*- 
import sqlite3
import datetime 
"""

"""


class  AnalyzeContinuousRunPerformance:
    table=""
    continousRunTable=""
    runReturnAccumulator=0
    untilTodayReturnAccumulator=0
    counter=0

    def __init__(self,table):
        self.table=table
        self.continuousRunTable=self.table+"ContinuousRun"
        Query='SELECT * FROM  '+self.table+' ORDER BY DATE ASC'
        querycursor=connection.cursor()
        querycursor.execute(Query)
        while True:
            row=querycursor.fetchone()
            if row == None:
                break
            
            
            ticker=row[1]
            beginDate=row[2]
            endDate=row[4]
            beginOpenPrice=queryGetTickerOpenPrice("StockData",ticker,beginDate)
            endOpenPrice=queryGetTickerOpenPrice("StockData",ticker,endDate)
            today=date.today()
            todaysCurrentPrice=0 #will need to call get todays open price/currentprice
            
            
            percentGainBeginDateEndDate=percentGain(beginOpenPrice,endOpenPrice)
            percentGainBeginDateToday=percentGain(beginOpenPrice,todaysCurrentPrice)
            
            #I should enter this data into a dbase or output as csv so that I can easily analyze the min/max

            #should I also keep track of ups vs downs? I.e. see how many went up and how many went down? see if more went up but only fractionally or a few went down, but went down hard.
            self.runReturnAccumulator+=percentGainBeginDateEndDate
            self.untilTodayReturnAccumulator+=percentGainBeginDateToday
            counter+=1

            if todaysOpenPrice >  0:
                print("%s ( %s %0.2f) (%s %0.2f) -> %0.2f ( %s %0.2f ) -> %0.2f " % (ticker,beginDate,beginOpenPrice,endDate,endOpenPrice,percentGainBeginDateEndDate,todaysDate,))
            else:
                print("%s ( %s %0.2f ) ( %s %0.2f ) -> %0.2f " % (ticker,beginDate,beginOpenPrice,endDate,endOpenPrice,percentGain))
        print("Average run return %0.2f." % (self.runReturnAccumulator/self.counter))
        print("Average return if held until today %0.2f." % (self.untilTodayReturnAccumulator/self.counter))

def percentGain(A,B):
    if A > 0:
        return (B-A)/A
    else :
        return -1



def queryGetTickerOpenPrice(table,ticker,date):
    """

    """
    queryCursor=connection.cursor()

    Query='SELECT Open from '+table
    queryCursor.execute(Query+'  WHERE StockTicker=? and Date = ?', (ticker,date))
    queryCursor.close()
    while True:
        row=queryCursor.fetchone()
        if row == None:
            break
        openPrice=row[0]

    return openPrice



def usage():
    print("")



#-----------------MAIN-------------------------

""" 
"""

database="IBDdatabase.sqlite"


inputList=[ "IBD50"] #,"BC20","IBD8585","Top200Composite"]
inputList=[ "BC20"]
inputList=[ "IBD50","BC20","IBD8585","Top200Composite"]
for item in inputList:
    connection=sqlite3.connect(database)
    Performance=AnalyzeContinuousRunPerformance(item)
    connection.commit()
quit()
