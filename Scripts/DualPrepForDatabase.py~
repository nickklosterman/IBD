import sqlite3
import sys #for cmd line arguments


if (len(sys.argv) > 2):
    database=sys.argv[1]
    IBD50 = open(sys.argv[2])
else:
    database="IBDdatabase.sqlite"
    IBD50 = open("Data/IBD50.txt")

connection=sqlite3.connect(database)
cursor=connection.cursor()
cursor.execute('DROP TABLE IBD50')
cursor.execute('CREATE TABLE IF NOT EXISTS IBD50 (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)')
#from http://greeennotebook.com/2010/06/how-to-use-sqlite3-from-python-introductory-tutorial/

counter=0
countermod=0
for line in IBD50:
    if not line.strip():# (len(line)<5):#check for blank lines
        counter=-1
        countermod=3
        print "--",line,"--"
        
    if line[0]=='#':
            counter=-1
            countermod=3
            print "Comment",line
    if countermod == 0:
        Date=line[:-1].strip() #chop off the newline at the end
    elif countermod == 1:
#        String=line[:-1].split(',')#split variable on delimiter ','
        String=line[:-1].split()#split variable on delimiter
        counter2=0
        for each in String: 
            print Date,',',String[counter2].strip().upper(),',',counter2+1
            cursor.execute('INSERT INTO IBD50 VALUES(null, ?, ?, ?)', (Date,String[counter2].strip().upper(),counter2+1))
            counter2+=1

#Previously I was planning on their being a blank line separating the each successive date/data entry. Now I handle it smarter.

    counter+=1
    countermod=counter%2
connection.commit()
cursor.close()
quit()
print "is the quit needed?"
IBD50.close()
