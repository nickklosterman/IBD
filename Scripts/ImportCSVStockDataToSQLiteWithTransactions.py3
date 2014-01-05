#!/usr/bin/env/python                                                                               
# -*- python -*-
'''
This script attempts to perform bulk import of csv data
into a SQLite database using transactions for improved 
performance.
'''
#http://stackoverflow.com/questions/5942402/python-csv-to-sqlite

import csv, sqlite3, time, glob, getopt, sys,os

def chunks(data, chunksize=10000):
    """ Divides the data into 10000 rows each """
    chunk=[]
    for i,line in enumerate(data):
        if ( i % chunksize == 0 and i > 0):
            yield chunk 
            del chunk[:]
        #print(line)
        chunk.append(line)
    yield chunk


class ImportYahooStockCSVDataWithTransactions:
    def __init__(self,database,directory):
        self.fileList=""
        self.database=database
        self.table=""
        self.directory=directory
        self.connection=sqlite3.connect(self.database)
        self.getCSVFileList()
        self.loopOverFiles()
        self.connection.commit()

    def getCSVFileList(self):
        os.chdir(self.directory)
        self.fileList=glob.glob("*.csv")

    def databasePrep(self):
        cursor=self.connection.cursor()
        Query="DROP TABLE IF EXISTS "+self.table
        print(Query)
        cursor.execute(Query)
        Query='CREATE TABLE IF NOT EXISTS '+self.table+' (Id INTEGER PRIMARY KEY, Date TEXT, Open INTEGER, High INTEGER, Low INTEGER, Close INTEGER, Volume INTEGER, Adj_Close INTEGER)'
        cursor.execute(Query)
        cursor.close()

    def loopOverFiles(self):
        for csvfile in self.fileList:
            #print(csvfile)
            ticker=csvfile[12:-12] #extract ticker if file is named table.csv?s=TICKER&ignore=.csv            
            #print(ticker)
            self.table=ticker
            self.databasePrep()
            cursor=self.connection.cursor()
            #be sure the file size isn't 0, we should be deleting those w a script.
            if (os.stat(csvfile).st_size!=0):
                with open(csvfile,'rt') as csvFileHandle:
                    #csvDataReader=csv.DictReader(csvFileHandle,delimiter=',')
                    #csvDataReader.next() #skip header row
                    csvData = csv.reader(csvFileHandle)
                    next(csvData) #skip header row
                    divData = chunks(csvData)
                    for chunk in divData:
                        cursor.execute('BEGIN TRANSACTION')
                        for f1,f2,f3,f4,f5,f6,f7 in chunk:
                            #Query='INSERT OR IGNORE INTO  %s (date,open,high,low,close,volume,adj_close) VALUES (%s,%s,%s,%s,%s,%s,%s) '%(self.table,f1,f2,f3,f4,f5,f6,f7)
                            Query='INSERT OR IGNORE INTO  %s (date,open,high,low,close,volume,adj_close) VALUES (%s,%s,%s,%s,%s,%s,%s) '%(self.table,f1,f2,f3,f4,f5,f6,f7)
                            #print(Query)
                            cursor.execute(Query)

                        #cursor.execute('COMMIT')
                        #cursor.commit()

#----------------------------------------------#----------------------------------------------
#----------------------------------------------#----------------------------------------------
#----------------------------------------------#----------------------------------------------
#----------------------------------------------#----------------------------------------------
if __name__ == "__main__":
    t = time.time()


    if 1:
        database="StockData.sqlite"
        directory="YahooCSVStockDataFiles"
    try:
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'i:o:l:t:d:f:', ['--input=',
                                                                              '--output=',
                                                                              '--loginfile=',
                                                                              '--table=',
                                                                              '--database=',
                                                                              '--format='
                                                                          ])
    except getopt.GetoptError as err:
        # print help information and exit:                                                               
        print(err) # will print something like "option -a not recognized"                      
        #usage()                                                                              
        sys.exit(2)

    for opt, arg in options:
        if opt in ('-o', '--output'):
            outputfilename = arg
        elif opt in ('-i', '--input'):
            inputfilename = arg
        elif opt in ('-t', '--table'):
            table = arg
        elif opt in ('-d', '--database'):
            database = arg
        elif opt in ('-f', '--format'):
            outputFormat = arg
        elif opt == '--version':
            version = arg

    Importer = ImportYahooStockCSVDataWithTransactions(database,directory)
    print("\n Time Taken: %.3f sec" % (time.time()-t)) 
