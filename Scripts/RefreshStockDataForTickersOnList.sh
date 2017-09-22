#!/bin/bash


getStockData() {
    while read symbol
    do
	echo "Retrieving ${symbol} data from Yahoo!"
	python Scripts/yahoo_quote_download/driver.py ${symbol} > table${symbol}.csv
    done < /tmp/uniquetickers.txt
    sleep 24
    }

loopOverCSV() {
    
    echo "Loop over .csv files"
    #Perform rename and column header rename
    for filename in table*.csv 
    do 

	echo "$filename"
	#REMOVED: this is not used since the .import will keep the first line if the schema for the table has been defined, therefore I need to remove the first line
	#change the column name "Adj Close" to "Adj_Close" for easier access
	#sed "1 s/Adj Close/Adj_Close/" -i "${filename}"

	#remove first line (column header line)
	tail -n +2 "${filename}" > "${filename}.new" ; mv "${filename}.new" "${filename}" 
	#sed -i -e "1d" "${filename}" #sed is supposed to be slower than tail 

#this was needed for the old ticker names that were downloaded with junk. now just need to strip off the table....or not put it on in the first place
	newFilename=`echo $filename | sed 's/table.csv?s=//;s/&ignore=//;s/%5E/_/'`
	ticker=`echo $filename | sed 's/table//;s/.csv//
'`
	newFilename=`echo $filename | sed 's/table//'`
	echo "$newFilename $ticker"
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

#	echo "CREATE TABLE IF NOT EXISTS ${ticker} (  Date TEXT,  Open REAL,  High REAL,  Low REAL,  Close REAL,  Volume INTEGER,  Adj_Close REAL);" >> /tmp/sqlitecommand.txt  #this is the old pre-2017 yahoo format
	echo "CREATE TABLE IF NOT EXISTS ${ticker} (  Date TEXT,  Open REAL,  High REAL,  Low REAL,  Close REAL,  Adj_Close REAL, Volume INTEGER);" >> /tmp/sqlitecommand.txt   #The New Yahoo format
	#import data into our database; sqlite automatically will create the table and use the first line as the column headers
	echo ".import ${newFilename} ${ticker} " >> /tmp/sqlitecommand.txt
	#sqlite3 "${database}" ".mode csv; .separator ','; .import ${newFilename} ${ticker}" #commands must be all issued at once since we aren't in a "sesscion" inside sqlite3. otherwise commands are reset since start a new session

	#sqlite3 "${ouptutDatabase}" "CREATE UNIQUE INDEX 'index_date' on ${ticker} " #('index_date' ASC)
	#needed the "IF NOT EXISTS" otherwise it would complain that there was that index already for all but the first call; that doesn't make sense to me as I thought the indices were per table 
	echo "CREATE UNIQUE INDEX IF NOT EXISTS 'index_date' on ${ticker} (Date);" >> /tmp/sqlitecommand.txt #('index_date' ASC)
    done
}

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
#We need to make a copy of the inputDatabase to 'seed' teh outputDatabase or the outputDatabase won't have the BC20,IBD50, etc lists in them
    cp $inputDatabase $outputDatabase

    echo "Pulling all unique tickers from IBD50,BC20,IBD8585, and Top200Composite"
    #pull all of the unique tickers from each table
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from IBD50 ORDER BY stockticker asc;' > /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from BC20 ORDER BY stockticker asc;' >> /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from IBD8585 ORDER BY stockticker asc;' >> /tmp/tickers.txt
    sqlite3 "${inputDatabase}" 'SELECT distinct(stockticker) from Top200Composite ORDER BY stockticker asc;' >> /tmp/tickers.txt
    #add the nasdaq ticker
    echo "^IXIC" >> /tmp/tickers.txt
    #add the sp500 ticker
    echo "^GSPC" >> /tmp/tickers.txt
#    "^DJI" >> /tmp/tickers.txt


    echo "Sorting and obtaining unique tickers"
    #sort the tickers
    sort /tmp/tickers.txt -u > /tmp/uniquetickers.txt

    echo "Unique tickers in uniquetickers.txt"
    echo "--------------------------------Get Stock Data commented out---------------"
    #sleep 100
 #   getStockData 
    
    echo "Removing files of size 0"
    # Remove files of length/size 0; this will complain if no files are found. How to trap that occurrence?
    find . -type f -size 0 -print0 | xargs -0 rm 


    echo -e ".mode csv\n.separator ','" > /tmp/sqlitecommand.txt
#    echo ".mode csv
# .separator ',';" >> /tmp/sqlitecommand.txt

    #echo "Performing column header correction, renaming files to ticker symbol and importing data into ${database}."

    loopOverCSV
    
    #execute our queries
    sqlite3 "${outputDatabase}" < /tmp/sqlitecommand.txt
    
    # echo "Delete .csv files?"
    # read response
    # while $response not in ( 'yY' | 'nN')
    # echo "please enter y or n"
    # read response
    date=`date +%Y-%m-%d`
    echo "File cleanup - creating gzipped tar archive of all .csv files"
    tar -cvzf YahooHistoricalDataFiles${date}.tar.gz *.csv
    #file cleanup
    rm *.csv #damnit these are being deleted before they are being imported

    #python Scripts/ImportCSVStockDataToSQLite.py3  umm I think I want the one with bulk transactions....

    #to determine how risky an investment would've been, do a query to find the min and max of each ticker and get the dates. see how close the dates are as well.
    #You'd need to apply some type of window, otherwise over time the min will typically be in the past and quite old
    #also check to see if it is on a downward or upward trend

fi



getStockDataOld() {
        #remove temp file
    rm /tmp/tickerurlfile.txt

    echo "Creating file of urls for downloading"
    while read symbol
    do
	#echo "\"http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv\" -O ${symbol}.csv" >> /tmp/tickerurlfile.txt
	#echo "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" >> /tmp/tickerurlfile.txt
	#     https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=1503274263&period2=1505952663&interval=1d&events=history&crumb=K.uApIOWG5V
	echo "https://query1.finance.yahoo.com/v7/finance/download/${symbol}?period1=1503273633&period2=1505952033&interval=1d&events=history&crumb=K.uApIOWG5V" >> /tmp/tickerurlfile.txt
#	wget "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" & #this hits yahoo too fast and they block you
    done < /tmp/uniquetickers.txt

    echo "Downloading data files from Yahoo"


#    cat /tmp/tickerurlfile.txt | parallel "wget {}" #this really doesn't seem to do it in parallel. still quite slow.
    # while read url
    # do 
    # 	wget url &   #really should just do this when I read the symbols. 
    # done < /tmp/tickerurlfile.txt

    echo "The_Following_Code_isnt_Tested" #well not fully tested
    while read LINE
    do
#you can't background this! You need to wait for the files to be downloaded before processing the files >> Solved by using 'wait'
#	wget -nc -nv $LINE &  #background the process to allow multiple downloads at once.  # this often fails as we end up getting : failed: Name or service not known. ; wget: unable to resolve host address ‘ichart.yahoo.com’
	wget -nc -nv $LINE  #

    done < /tmp/tickerurlfile.txt


    }

