import sqlite3
database="/home/arch-nicky/IBDdatabase.sqlite"
connection=sqlite3.connect(database)
cursor=connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS IBD50 (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)')
#connection.commit() #needed otherwise dbase not created


IBD50 = open("/home/arch-nicky/IBD50.txt")
counter=0
countermod=0
for line in IBD50:
    if countermod == 0:
        Date=line[:-1] #chop off the newline at the end
    elif countermod == 1:
        String=line[:-1].split(',')#split variable on delimiter ','
        counter2=0
        for each in String: #strip to strip out whitespace
            print Date.strip(),',',String[counter2].strip().upper(),',',counter2+1
            cursor.execute('INSERT INTO IBD50 VALUES(null, ?, ?, ?)', (Date.strip(),String[counter2].strip().upper(),counter2+1)) 

            counter2+=1
    elif countermod == 2: # this is the blank line that I'm just skipping over
        print ''
    #print(line)

    counter+=1
    countermod=counter%3
connection.commit()
cursor.close()
quit()
print "is the quit needed?"
IBD50.close()
