import sqlite3
import sys #for cmd line arguments

def read_file_build_database(table,file):
    Query="DROP TABLE IF EXISTS "+table
    print Query
    cursor.execute(Query)
    Query="CREATE TABLE IF NOT EXISTS "+table+" (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)"
    print Query
    cursor.execute(Query)

    counter=0
    countermod=0
    for line in file:
        if not line.strip():# (len(line)<5):#check for blank lines
            counter=-1
            countermod=3
            print "--",line,"--"
        
        if line[0]=='#':
            counter=-1
            countermod=3
            print "Comment",line[1:]
        if countermod == 0:
            Date=line[:-1].strip() #chop off the newline at the end
        elif countermod == 1:
#        String=line[:-1].split(',')#split variable on delimiter ','
            String=line[:-1].split()#split variable on delimiter
            counter2=0
            for each in String: 
                Ticker=String[counter2].strip().upper()
                Rank=counter2+1
                print Date,',',Ticker,',',Rank
                Query="INSERT INTO "+table+" VALUES(null,"+Date+","+Ticker+","+str(Rank)+")"
                print Query
#                cursor.execute('INSERT INTO IBD50 VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
                Front='INSERT INTO '+table
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
    table2="BC20"
    file2 = open("Data/BC20.txt")

connection=sqlite3.connect(database)
cursor=connection.cursor()
#from http://greeennotebook.com/2010/06/how-to-use-sqlite3-from-python-introductory-tutorial/
read_file_build_database(table1,file1)
read_file_build_database(table2,file2)




connection.commit()
cursor.close()
quit()
print "is the quit needed?"
IBD50.close()
