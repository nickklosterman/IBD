#!/usr/bin/python


'''
NOTE: there isn't a mysql-python port for python3
I therefore believe this .py3 file to not work. It appears from diff
to have the python3 versions of print. However without a working
mysql-python, the script won't work

http://dev.mysql.com/doc/connector-python/en/connector-python-install.html
'''

class MovementMatrix:

    def __init__(self,database,table,limit_number,offset_number):
        self.database=database
        self.table=table
        self.limit_number=limit_number #limit number used for query
        self.offset_number=offset_number
        self.Dates=self.GetDateList()
        self.Stocks=self.GetStockList()
        self.Ranks=self.GetRankList()


    def GetDateList(self):
        dates=[]
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT DISTINCT(Date) from %s ORDER BY DATE DESC LIMIT %s OFFSET %s" % (self.table,self.limit_number,self.offset_number)) #Desc New->Old, ASC Old->New i.e. new=most recent date, old=least recent date
            rows = cur.fetchall()
            for row in rows:
                dates.append(row["Date"])
        con.commit()
        cur.close()
        con.close()
        return dates

    def GetRankList(self):
        ranks=[]
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
#            cur.execute("SELECT DISTINCT(Rank) from %s ORDER BY Rank ASC LIMIT %s OFFSET %s" % (self.table,self.limit_number,self.offset_number)) 
            cur.execute("SELECT DISTINCT(Rank) from %s ORDER BY Rank ASC " % (self.table)) 
            rows = cur.fetchall()
            for row in rows:
                ranks.append(row["Rank"])
        con.commit()
        cur.close()
        con.close()
        return ranks

       
    def GetStockList(self):
        StockTickers=[]
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            query=self.BuildQueryFromDates()
            rowcount=int(cur.execute(query))
            rows = cur.fetchall()
            for row in rows:
                StockTickers.append(row["StockTicker"])
                
        con.commit()
        cur.close()
        con.close()
        return StockTickers
    def BuildQueryFromDates(self):
        dictlength=len(self.Dates)
        query="SELECT DISTINCT(StockTicker) FROM "+self.table+" WHERE "
        for i in range(0,dictlength,1):
            query+="DATE='" +self.Dates[i] + "' OR "  
        query=query[:-3] #clip off the final " AND" which is unneeded
        query+=" ORDER BY StockTicker ASC " 
        return query

    def BuildQueryFromDate(self,week):
        query="SELECT StockTicker FROM "+self.table+" WHERE DATE='" +self.Dates[week] + "' ORDER BY StockTicker ASC " 
        return query


    def GetRankForStockDate(self,StockTicker,Date):
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            resultcount=int(cur.execute("SELECT Rank from %s WHERE Date='%s' AND StockTicker='%s' " % (self.table,Date,StockTicker)) )
#            resultcount=cur.row_count() got an error when tried to use this
            if resultcount==1:
                row=cur.fetchone()
                rank=int(row['Rank'])
            elif resultcount==0:
                rank=-1    
            else: #multiple entries (which shouldn't happen)
                rank=-2
        con.commit()
        cur.close()
        con.close()
        return rank

    def GetStockTickerForRankDate(self,Rank,Date):
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            resultcount=int(cur.execute("SELECT StockTicker from %s WHERE Date='%s' AND Rank='%s' " % (self.table,Date,Rank)) )
#            resultcount=cur.row_count() got an error when tried to use this
            if resultcount==1:
                row=cur.fetchone()
                stock=row['StockTicker']
            elif resultcount==0:
                stock="unknown"
            else: #multiple entries (which shouldn't happen)
                stock="unknown2"
        con.commit()
        cur.close()
        con.close()
        return stock

    def GetStockPriceForStockDate(self,StockTicker,Date):
#        StockPrice=get_historical_prices(StockTicker,Date)
        StockData=get_historical_prices_plus_one_day(StockTicker,Date)

        closingprice=0.0
        quotedate=0
        if StockData[0][0]!="Date": # a simple error check since this first field should be "Date"   
            print(("ERROR for %s" % (StockTicker))) #enter this data into an errors database                    
#            insert_error_data(tableerror,date,ticker,rank)
        else:
             if StockData[0][4]=='Close':
                quotedate=StockData[1][0]
                closingprice=StockData[1][4]
        StockPrice=closingprice
        return StockPrice

    def GetStockFromDate(self,week):
        StockTickers=[]
        con = mdb.connect('localhost', 'nicolae', 'ceausescu', self.database)
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            query=self.BuildQueryFromDate(week)
            rowcount=int(cur.execute(query))
            rows = cur.fetchall()
            for row in rows:
                StockTickers.append(row["StockTicker"])
                
        con.commit()
        cur.close()
        con.close()
        return StockTickers
        
        #Movers:
    #WeekA and WeekB are indices for the Dates[] list.
    #the stocks on the list for Dates[WeekA] are compared to the stocks on the list for Dates[WeekB]
                
    def Movers(self,weekA,weekB): 
        New=self.GetStockFromDate(weekA)
        Old=self.GetStockFromDate(weekB)
        print("Tickers from weekB no longer on list at weekA")
        for old in Old:
            if old not in New:
#                print(old,self.GetRankForStockDate(old,self.Dates[weekA])) can't use weekA herebecuase the stock is off the list by then!
                print(("%s %s" % (old,self.GetRankForStockDate(old,self.Dates[weekB]))))
        print("Tickers from weekA not on list at weekB")
        for new in New:
            if  new not in Old:
                print(("%s %s" % (new,self.GetRankForStockDate(new,self.Dates[weekA]))))


    def RankMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print(('%s,' % (s)), end=' ') #start new line with  the stock
            for d in self.Dates:
                rank=self.GetRankForStockDate(s,d)
                if rank!=-1:
                    #print('%s' % (rank)),
                    sys.stdout.write('%s' % (rank)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting. http://codingrecipes.com/print-without-a-new-line-or-space-in-python
                else:
                    nine=9
#                    print("-"),
            #if not at end of list then output ,
                print((','), end=' ') #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL


    def StockTickerMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for r in self.Ranks:
            print(('%s,' % (r)), end=' ') #start new line with  the stock
            for d in self.Dates:
                stockticker=self.GetStockTickerForRankDate(r,d)
                if stockticker!="":
                    #print('%s' % (rank)),
                    sys.stdout.write('%s' % (stockticker)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting. http://codingrecipes.com/print-without-a-new-line-or-space-in-python
                else:
                    nine=9
#                    print("-"),
            #if not at end of list then output ,
                print((','), end=' ') #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL


    def StockMatrix(self):
        self.PrintDates() #print header of dates
        print("") #output EOL
        for s in self.Stocks:
            print(('%s,' % (s)), end=' ') #start new line with  the stock
            for d in self.Dates:
                stockprice=self.GetStockPriceForStockDate(s,d)
                if stockprice!=0.0:
                    sys.stdout.write('%s' % (stockprice)) #the print was adding a padding space, this was causing OOCalc to then interpret the numbers as strings, preventing proper charting.
            #if not at end of list then output ,
                print((','), end=' ') #OR add to string and then remove last character when done with that string of dates
            print("") #output EOL
                
    def PrintDates(self):
        print((","), end=' ')
        for d in self.Dates:
            print(("%s," % (d)), end=' ')



########### MAIN ############

import sys
import MySQLdb as mdb # in mysql-python package
import getopt
#import YahooStockQuotes #http://stackoverflow.com/questions/714881/how-to-include-external-python-code-to-use-in-other-files
from YahooStockQuotes import get_historical_prices_plus_one_day
inputfilename="RealEstateSalesData/MontgomeryCountyOhio/temp.csv" #SALES_2012_RES.csv"                            
inputfilename="RealEstateSalesData/MontgomeryCountyOhio/SALES_2012_RES.csv"
outputfilename="RealEstateSalesMontgomeryCtyOhiooutput.txt"
loginfile="/home/nicolae/.mysqllogin"
table="BC20"
database="StockMarketData"
limit_num=2
offset=0
try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:l:t:d:m:f:', ['input=',   #py3k got rid if requiring the leading --stuff for long options
                                                                        'output=',
                                                                        'loginfile=',
                                                                        'table=',
                                                                        'database=',
                                                                        'limit=',
                                                                            'offset=',
                                                                        ])
except getopt.GetoptError as err:
    # print help information and exit:                                                                        
    print(str(err)) # will print something like "option -a not recognized"                                         
        #usage()                                                                                                  
    sys.exit(2)

for opt, arg in options:
    if opt in ('-o', '--output'):
        outputfilename = arg
    elif opt in ('-i', '--input'):
        inputfilename = arg
    elif opt in ('-l', '--loginfile'):
        loginfile = arg
    elif opt in ('-t', '--table'):
        table = arg
    elif opt in ('-d', '--database'):
        database = arg
    elif opt in ('-m', '--limit'):
        limit_num = arg
    elif opt in ('-f', '--offset'):
        offset = arg
    elif opt == '--version':
        version = arg


#print(inputfilename,outputfilename,loginfile,table,database)
MM=MovementMatrix(database,table,limit_num,offset)
MM.RankMatrix()
MM.Movers(0,1) #must call program as such : python MovementMatrix.py -m 9 -t IBD50 , otherwise we get an index out of range.
MM.StockTickerMatrix()
MM.StockMatrix()
