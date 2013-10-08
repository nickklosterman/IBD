#!/usr/bin/env/python
# -*- python -*- 
import sqlite3

"""
This script determines the avg number of days on each of the four IBD lists that I look at.
If the stock is still on the list but hasn't exited the list, it isn't taken into acct.

"""

from datetime import date


def diffInDays(date1,date2):
    #print(date1[0:4],date1[5:7],date1[8:10])
    #    print(date1,date2)
    #   print(type(date1),type(date2))
    delta=""
    if date2 is not None:
        d0 = date(int(date1[0:4]),int(date1[5:7]),int(date1[8:10]))
        d1 = date(int(date2[0:4]),int(date2[5:7]),int(date2[8:10]))
        if d0>d1:
            delta = d0 - d1
        else:
            delta = d1 - d0
    #print delta.days
    return delta.days

def setMinMax(min_,max_,value):
    if min_ > value:
        min_=value
    if max_ < value:
        max_ = value
    return min_,max_

class  StockAverageDaysForContinuousRunOnList:
    datesList=[]
    counter=0
    totalDaysOnList=0
    minDays=9999999
    maxDays=0
    def __init__(self,table):
        self.table=table
        self.queryGetDatesList()
        for dates in self.datesList:
            #print(type(dates))
            #print(dates[0],dates[1])
            beginDate=dates[0]
            endDate=dates[1]
            daysOnList=diffInDays(beginDate,endDate)
            if daysOnList ==1:
                print(beginDate,endDate)
            self.minDays,self.maxDays=setMinMax(self.minDays,self.maxDays,daysOnList)            
            self.totalDaysOnList+=daysOnList
            self.counter+=1
        avgDaysOnList=-1
        if self.counter> 0:    
            avgDaysOnList=self.totalDaysOnList/self.counter
        print("Average days on list for %s os %0.2f." % (table,avgDaysOnList))
        print("Minimum days on list: %d; Maximum days on list: %d."%(self.minDays,self.maxDays))


    def queryGetDatesList(self):
        Query='SELECT begindate,enddate from  '+self.table+' '
        querycursor=connection.cursor()
        querycursor.execute(Query)
        while True:
            row=querycursor.fetchone()
            if row[1] is  None:
                break
            if row[1][0] != "2": #enforce that we are looking at year 2XXX data
                break
            self.datesList.append(row)

def usage():
    print("")
 

#-----------------MAIN-------------------------

""" 
"""
print("need usage and getopt")

database="IBDdatabase.sqlite.continuousrun"
database="IBDTestDatabase.sqlite"

inputList=[ "IBD50ContinuousRun","BC20ContinuousRun","IBD8585ContinuousRun","Top200CompositeContinuousRun"]
inputList=["BC20ContinuousRun"]
for item in inputList:
    connection=sqlite3.connect(database)
    ContinuousRun=StockAverageDaysForContinuousRunOnList(item)

quit()
