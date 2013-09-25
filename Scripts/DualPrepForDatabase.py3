#!/usr/bin/env/python 
# -*- python -*-


"""
This program is used to clear out and then insert the data tables for the collected IBD lists.
The data is placed into the IBDdatabase.sqlite file.
"""


import sqlite3
import sys #for cmd line arguments
from datetime import date #for .weekday() function

def read_file_build_database(table,errortable,file)
"""
This function simply drops and then recreates the desired table and its accompanying errortable
It then inserts the data from 
"""
    Query="DROP TABLE IF EXISTS "+table
    print(Query)
    cursor.execute(Query)
    Query="CREATE TABLE IF NOT EXISTS "+table+" (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)"
    print(Query)
    cursor.execute(Query)

    Query="DROP TABLE IF EXISTS "+errortable
    print(Query)
    cursor.execute(Query)
    Query="CREATE TABLE IF NOT EXISTS "+errortable+" (Id INTEGER PRIMARY KEY, Date TEXT, StockTicker TEXT, Rank INTEGER)"
    print(Query)
    cursor.execute(Query)

    counter=0
    countermod=0
    for line in file:
        if not line.strip():""" if this is a blank line, reset our counter"""
            counter=-1
            countermod=3

        """ if processing a comment line, reset """
        if line[0]=='#': 
            counter=-1
            countermod=3

        """ countermod === 0 on the Date line, this is used to delineate the beginning of a record """
        if countermod == 0:
            Date=line[:-1].strip() #chop off the newline at the end

        """the next line *MUST* be a data line of tickers. I should perform an error check in case  """
        elif countermod == 1:
            String=line[:-1].split()#split variable on delimiter, removing newline at the end
            counter2=0
            for each in String: 
                Ticker=String[counter2].strip().upper()
                Rank=counter2+1
                #here we ignore the DotW check since they sorta have moved and I imagine that if they moved in the future it'd break a whole bunch. in the end I don't think I really care if I have the date 100% right.
                query='INSERT INTO '+table+' VALUES(null,"'+Date+'","'+String[counter2].strip().upper()+'",'+str(counter2+1)+')' #needed to quote the string for entry, also needed to quote the date or it gets chopped when its sqlite enters and validates/converts it.
                cursor.execute(query)

                counter2+=1
        counter+=1
        countermod=counter%2
#end def read_file_build_database



"""
-----------------------------------------------
MAIN
-----------------------------------------------
"""
if (len(sys.argv) > 2):
    database=sys.argv[1]
    IBD50 = open(sys.argv[2])
else:
    database="IBDdatabase.sqlite"  #need to jsut stick this stuff in an array and loop over it all
 

    TableList=[ "IBD50", "BC20","IBD8585","Top200Composite" ]
    FileList=["Data/IBD50.txt","Data/BC20.txt","Data/8585.txt","Data/Top200Composite.txt"]
    ErrorTableList=[ "IBD50Error", "BC20Error","IBD8585Error","Top200CompositeError" ]
   

connection=sqlite3.connect(database)
cursor=connection.cursor()
#from http://greeennotebook.com/2010/06/how-to-use-sqlite3-from-python-introductory-tutorial/

for index in range(len(TableList)):
    file_handler=open(FileList[index])
    read_file_build_database(TableList[index],ErrorTableList[index],file_handler)
    file_handler.close()


connection.commit()
cursor.close()
quit()
print("is the quit needed?")
IBD50.close()
