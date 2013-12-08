#!/bin/bash
echo "
This program pulls all the tickers from the IBD50,BC20,IBD8585, and Top200Composite
tables and downloads the latest historical data from yahoo and places the data in 
a database with each ticker having its own table. The table name is the ticker.
"
if [ $# -ne 2 ]
then 
    echo "Please supply a database to use."
    echo "$0 DatabaseWithTickerLists.sqlite OutputHistoricalStockDatabase.sqlite"
else
    inputDatabase="${1}"
    outputDatabase="${2}"
    echo "Pulling all unique tickers from IBD50,BC20,IBD8585, and Top200Composite"
    #pull all over the unique tickers from each table
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from IBD50 ORDER BY stockticker asc;' > /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from BC20 ORDER BY stockticker asc;' >> /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from IBD8585 ORDER BY stockticker asc;' >> /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from Top200Composite ORDER BY stockticker asc;' >> /tmp/tickers.txt

    echo "Sorting and obtaining unique tickers"
    #sort the tickers
    sort /tmp/tickers.txt -u > /tmp/uniquetickers.txt

    echo "Unique tickers in uniquetickers.txt"

    #remove temp file
    rm /tmp/tickerurlfile.txt

    echo "Creating file of urls for downloading"
    while read symbol
    do
	#echo "\"http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv\" -O ${symbol}.csv" >> /tmp/tickerurlfile.txt
	echo "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" >> /tmp/tickerurlfile.txt
    done < /tmp/uniquetickers.txt

    echo "Downloading data files from Yahoo"
    cat /tmp/tickerurlfile.txt | parallel "wget {}" #this really doesn't seem to do it in parallel. still quite slow.

    echo "Removing files of size 0"
    # Remove files of length/size 0; this will complain if no files are found. How to trap that occurrence?
    find . -type f -size 0 -print0 | xargs -0 rm 


    echo -e ".mode csv\n.separator ','" > /tmp/sqlitecommand.txt
#    echo ".mode csv
# .separator ',';" >> /tmp/sqlitecommand.txt

    #echo "Performing column header correction, renaming files to ticker symbol and importing data into ${database}."

    #Perform rename and column header rename
    for filename in table*.csv 
    do 
	#REMOVED: this is not used since the .import will keep the first line if the schema for the table has been defined, therefore I need to remove the first line
	#change the column name "Adj Close" to "Adj_Close" for easier access
	#sed "1 s/Adj Close/Adj_Close/" -i "${filename}"

	#remove first line (column header line)
	tail -n +2 "${filename}" > "${filename}.new" ; mv "${filename}.new" "${filename}" 
	#sed -i -e "1d" "${filename}" #sed is supposed to be slower than tail 

	newFilename=`echo $filename | sed 's/table.csv?s=//;s/&ignore=//'`
	ticker=`echo $filename | sed 's/table.csv?s=//;s/&ignore=.csv//'`
	mv "${filename}" $newFilename

	#drop database, clear out old data. 
#	sqlite3 "${database}" "DROP TABLE ${ticker}"
	echo "DROP TABLE IF EXISTS ${ticker};" >> /tmp/sqlitecommand.txt

	#define schema for data we will be importing. If the schema isn't defined, all fields are TEXT
# 	sqlite3 "${database}" "CREATE TABLE IF NOT EXISTS ${ticker} (
#   Date TEXT,
#   Open REAL,
#   High REAL,
#   Low REAL,
#   Close REAL,
#   Volume INTEGER,
#   Adj_Close REAL
# );"

	echo "CREATE TABLE IF NOT EXISTS ${ticker} (  Date TEXT,  Open REAL,  High REAL,  Low REAL,  Close REAL,  Volume INTEGER,  Adj_Close REAL);" >> /tmp/sqlitecommand.txt
	#import data into our database; sqlite automatically will create the table and use the first line as the column headers
	echo ".import ${newFilename} ${ticker} " >> /tmp/sqlitecommand.txt
	#sqlite3 "${database}" ".mode csv; .separator ','; .import ${newFilename} ${ticker}" #commands must be all issued at once since we aren't in a "sesscion" inside sqlite3. otherwise commands are reset since start a new session

	#sqlite3 "${ouptutDatabase}" "CREATE UNIQUE INDEX 'index_date' on ${ticker} " #('index_date' ASC)
	echo "CREATE UNIQUE INDEX 'index_date' on ${ticker} (Date);" >> /tmp/sqlitecommand.txt #('index_date' ASC)
    done

    #execute our queries
    sqlite3 "${outputDatabase}" < /tmp/sqlitecommand.txt
    
    # echo "Delete .csv files?"
    # read response
    # while $response not in ( 'yY' | 'nN')
    # echo "please enter y or n"
    # read response

    echo "File cleanup - creating gzipped tar archive of all .csv files"
    tar -cvzf YahooHistoricalDataFiles.tar.gz *.csv
    #file cleanup
    #    rm *.csv #damnit these are being deleted before they are being imported


    #python Scripts/ImportCSVStockDataToSQLite.py3  umm I think I want the one with bulk transactions....


    #to determine how risky an investment would've been, do a query to find the min and max of each ticker and get the dates. see how close the dates are as well.


fi
