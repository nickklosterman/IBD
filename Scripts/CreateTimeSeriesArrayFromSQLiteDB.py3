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

def check_tables_exist(tablelist):
    cursor=connection.cursor()
    for table in tablelist:
        Query="select case when tbl_name ='"+table+"' then 1 else 0 end  from sqlite_master where type='table' and name='"+table+"' order by name"
    #    print(Query)
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

def query_for_dates(tablelist):
    check_tables_exist(tablelist)    
    tablequery=tablelist[0]
    tabledata=tablelist[1]
   # print(tablequery,tabledata)
    Query='SELECT DISTINCT(DATE) FROM '+tablequery+' ORDER BY DATE ASC'
    querycursor=connection.cursor()
    querycursor.execute(Query)
    rowcounter=0
    DateList=[]
    while True: #needed so we can use the 'break' in case a row is empty
#        print(rowcounter)
        rowcounter+=1
        row=querycursor.fetchone()
        if row == None:
            break
        DateList.append(row[0])
    querycursor.close()
    return DateList
#end def query_for_data

def query_for_stocks(tablelist):
    check_tables_exist(tablelist)    
    tablequery=tablelist[0]
    tabledata=tablelist[1]
  #  print(tablequery,tabledata)
    Query='SELECT DISTINCT(STOCKTICKER) FROM '+tablequery+' ORDER BY STOCKTICKER ASC'
    querycursor=connection.cursor()
    querycursor.execute(Query)
    rowcounter=0
    StockList=[]
    while True: #needed so we can use the 'break' in case a row is empty
#        print(rowcounter)
        rowcounter+=1
        row=querycursor.fetchone()
        if row == None:
            break
        StockList.append(row[0])
    querycursor.close()
    return StockList


def query_for_stocks_min_occurrence(tablelist,stocklist,minoccurrence):
    print("This doesn't work")
    check_tables_exist(tablelist)    
    tablequery=tablelist[0]
    tabledata=tablelist[1]
 #   print(tablequery,tabledata)
    querycursor=connection.cursor()
    for stock in stocklist:
        Query='SELECT COUNT(DATE) FROM '+tablequery+' WHERE STOCKTICKER LIKE "'+stock+'"'
        querycursor.execute(Query)
        rowcounter=0
        StockList=[]
        while True: #needed so we can use the 'break' in case a row is empty
            #        print(rowcounter)
            rowcounter+=1
            row=querycursor.fetchone()
            if row == None: #this should never happen
                break
            if  (row[0]>=minoccurrence):
                StockList.append(stock)
    querycursor.close()
    return StockList


def query_for_ibd_rank(tablelist,datelist,stocklist):
    check_tables_exist(tablelist)    
    tablequery=tablelist[0]
    tabledata=tablelist[1]
#    print(tablequery,tabledata)
    querycursor=connection.cursor()
    RankList=[]
    for stock in stocklist:
        for date in datelist:
            Query='SELECT RANK FROM '+tablequery+' WHERE STOCKTICKER LIKE "'+stock+'" AND DATE="'+date+'"'
            querycursor.execute(Query)
#            while True: #needed so we can use the 'break' in case a row is empty
            row=querycursor.fetchone()
            if row == None:
                rank=-99
                RankList.append(-99)
            else:
                RankList.append(row[0])
                rank=row[0]
            print(stock,date,rank)
    querycursor.close()
    return RankList

#-----------------MAIN-------------------------
if (len(sys.argv) > 1):
    database=sys.argv[1]
else:
    database="IBDdatabase.sqlite"
#I could simplify this by updating the "tablequery" table with the stock data, alternately I could do a join to cut down on redundant data.
inputList=[["IBD50","IBD50StockData"],["BC20","BC20StockData"]]#,["IBD8585","IBD8585StockData"],["Top200Composite","Top200CompositeStockData"]]
for item in inputList:
    connection=sqlite3.connect(database)
    datelist=query_for_dates(item)
    stocklist=query_for_stocks(item)
    stocklist2=query_for_stocks_min_occurrence(item,stocklist,3)
    print(stocklist2)
#    ranklist=query_for_ibd_rank(item,datelist,stocklist2)
#    print(datelist,stocklist,stocklist2)
    connection.commit()
quit()
#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
