import sqlite3
#sqlite3 IBDdatabase.sqlite "select distinct(StockTicker) from IBD50 order by StockTicker ASC"
print "This script takes the stock ticker change list generated from GetStockTickerChanges.sh and puts them into a sqlite3 database. This checks to see if a particular symbol is all ready entered to prevent multiples."
#curl -s "http://ichart.finance.yahoo.com/table.csv?s=YHOO&a=11&b=2&c=2005&d=11&e=2&f=2005&g=d&f=sl1&ignore=.csv"

import sys #for cmd line arguments
import urllib #for getting quotes from net

def CreateDatabaseAndTableIfNotExist(database,table):
    print "Creating table if it doesn't all ready exist"
    insertcursor.execute('CREATE TABLE IF NOT EXISTS StockTickerChangeData (Id INTEGER PRIMARY KEY, Date TEXT, StockTickerOld TEXT, StockTickerNew TEXT)')
#end def get_historical_prices_plus_one_day
def insert_data(database,table,oldsymbol,newsymbol,date):
#    cursor.execute('DROP TABLE IF EXISTS IBD50StockData') #FOR SOME REASON YOU CAN'T USE A VARIABLE FOR THE TABLE NAME
# NEEDED ANOTHER CURSOR OTHERWISE IT WOULD DESTROY THE RESULT SET WE HAD
    insertcursor.execute('INSERT INTO StockTickerChangeData VALUES(null, ?, ?, ?)', (date,oldsymbol,newsymbol))
    return 0
#end def insert_data

if (len(sys.argv) > 2):
    database=sys.argv[1]
    table=sys.argv[2]
    ChangeListFile=sys.argv[3]
else:
    print "Not enough arguments, using default database,database table, stockticker change list."
    database="IBDdatabase.sqlite"
    table="StockTickerChangeData"
    ChangeListFile=open("Data/StockTickerChangeList.txt")#data is expected to be oldticker,newticker,dateofchange. one field per line
connection=sqlite3.connect(database)
selectcursor=connection.cursor()
insertcursor=connection.cursor()

linecounter=0
modlinecounter=linecounter%3
CreateDatabaseAndTableIfNotExist(database,table)#since we know the table exists we can query it to get results
for line in ChangeListFile:
#    print line
    if line.strip(): 
#get the old,new ticker,and date into variables
        if modlinecounter == 0:
            oldticker=line.strip()
        if modlinecounter == 1:
            newticker=line.strip()
        if modlinecounter == 2:
            changedate=line.strip()
#            selectcursor.execute('SELECT StockTickerOld,StockTickerNew,Date FROM StockTickerChangeData WHERE StockTickerOld=\":oldticker\"',({"oldticker" : oldticker}))
            ot=(oldticker,)
            selectcursor.execute('SELECT Id,StockTickerOld,StockTickerNew,Date FROM StockTickerChangeData WHERE StockTickerOld=?',(ot))
#            selectcursor.execute('SELECT Id,StockTickerOld,StockTickerNew,Date FROM StockTickerChangeData WHERE StockTickerOld="%s"'%oldticker) #this method is vulnerable to sql injection attacks
#place into database, checking to see if all ready entered.
            row=selectcursor.fetchone()
            if row == None: #if no record present then enter it in
                print "entering in data",database,table,oldticker,newticker,changedate
                error=insert_data(database,table,oldticker,newticker,changedate)
            else:
                print "record contaning %s all ready present"%oldticker
        linecounter+=1
        modlinecounter=linecounter%3

#commit changes and close dbase connections
connection.commit()
selectcursor.close()
insertcursor.close()
if connection:
    connection.close()
quit()


#http://www.comp.mq.edu.au/units/comp249/pythonbook/pythoncgi/pysqlite.html
#http://docs.python.org/library/sqlite3.html http://zetcode.com/db/sqlitepythontutorial/
