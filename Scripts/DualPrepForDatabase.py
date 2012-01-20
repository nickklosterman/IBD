import sqlite3
import sys #for cmd line arguments
from datetime import date #for .weekday() function

def read_file_build_database(table,errortable,file,reportdayofweek):
    Query="DROP TABLE IF EXISTS "+table
    print Query
    cursor.execute(Query)
    Query="CREATE TABLE IF NOT EXISTS "+table+" (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)"
    print Query
    cursor.execute(Query)

    Query="DROP TABLE IF EXISTS "+errortable
    print Query
    cursor.execute(Query)
    Query="CREATE TABLE IF NOT EXISTS "+errortable+" (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)"
    print Query
    cursor.execute(Query)

    counter=0
    countermod=0
    for line in file:
        if not line.strip():# (len(line)<5):#check for blank lines
            counter=-1
            countermod=3
 #           print "--",line,"--"
        
        if line[0]=='#':
            counter=-1
            countermod=3
            print "Comment",line[1:].strip()
        if countermod == 0:
            Date=line[:-1].strip() #chop off the newline at the end
            print Date
        elif countermod == 1:
#        String=line[:-1].split(',')#split variable on delimiter ','
            String=line[:-1].split()#split variable on delimiter
            counter2=0
            year=Date[0:4]
            month=Date[5:7]
            day=Date[8:10]
            for each in String: 
                Ticker=String[counter2].strip().upper()
                Rank=counter2+1
                dayofweek=date(int(year),int(month),int(day)).weekday()
                #perform a date check on teh data being entered. BC20 is published on Tuesday IBD50 on Monday except when bank holiday falls on Monday then it falls on a Tuesday
                if reportdayofweek==dayofweek:
                    Front='INSERT INTO '+table
                    cursor.execute(Front+' VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
                elif reportdayofweek==0 and dayofweek==1:#case of IBD50 bumped on a Tuesday
                    Front='INSERT INTO '+table
                    cursor.execute(Front+' VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
                    Front='INSERT INTO '+errortable #enter it into the error dbase just in case
                    cursor.execute(Front+' VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
                else:
#                if reportdayofweek!=dayofweek:
                    print "Date doesn't fall on appropriate day of week, Entering into Error Database:",errortable
                    Front='INSERT INTO '+errortable #enter it into the error dbase just in case
                    cursor.execute(Front+' VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
                #cursor.execute(Query) Using this method I don't think the strnigs were being quoted when they needed to
                counter2+=1
        counter+=1
        countermod=counter%2
#end def read_file_build_database

if (len(sys.argv) > 2):
    database=sys.argv[1]
    IBD50 = open(sys.argv[2])
else:
    database="IBDdatabase.sqlite"
    table1="IBD50"
    file1 = open("Data/IBD50.txt")
    errortable1="IBD50Error"
    reportDayOfWeek1=0#monday
    table2="BC20"
    file2 = open("Data/BC20.txt")
    errortable2="BC20Error"
    reportDayOfWeek2=1#tuesday

connection=sqlite3.connect(database)
cursor=connection.cursor()
#from http://greeennotebook.com/2010/06/how-to-use-sqlite3-from-python-introductory-tutorial/
read_file_build_database(table1,errortable1,file1,reportDayOfWeek1)
read_file_build_database(table2,errortable2,file2,reportDayOfWeek2)





connection.commit()
cursor.close()
quit()
print "is the quit needed?"
IBD50.close()
