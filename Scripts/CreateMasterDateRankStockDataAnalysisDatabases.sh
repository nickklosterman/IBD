#!/bin/bash
echo "
This script will create all the temporary tables for a database such that each 
ticker in the database has a table titled CombinedDates${ticker}Details where
the date, rank, and historical stock data are all in one table.
usage:bash $0 database.sqlite3
"
#temporary tables don't persist when created on the command line. they only persist
 
if [[ $# -eq 11 ]]
then 
echo "
This set of queries don't work because of the temporary tables not persisting. 
"

    databasefilename="${1}"
    databaselist=('BC20') # 'IBD50' '8585' 'Top200Composite')
    for database in $databaselist
    do 
	echo "CREATE TEMPORARY TABLE TimesOnList AS SELECT stockticker,count(stockticker) AS count_sticker FROM $database GROUP BY stockticker;"
	sqlite3 $databasefilename "CREATE TEMPORARY TABLE TimesOnList AS SELECT stockticker,count(stockticker) AS count_sticker FROM $database GROUP BY stockticker;"
	echo "CREATE TEMPORARY TABLE DatesList AS SELECT DISTINCT(date) AS distinct_date FROM $database;"
	sqlite3 $databasefilename "CREATE TEMPORARY TABLE DatesList AS SELECT DISTINCT(date) AS distinct_date FROM $database;"

	echo "select distinct(stockticker) from ${database}"
	tickerlist=$(sqlite3 $databasefilename  "select distinct(stockticker) from ${database}")
	for ticker in $tickerlist 
	do 
	    bash "CREATE TEMPORARY TABLE ${ticker}Details AS SELECT rank,date FROM ${database} WHERE stockticker LIKE \"${ticker}\";"
	    sqlite3 $databasefilename "CREATE TEMPORARY TABLE ${ticker}Details AS SELECT rank,date FROM ${database} WHERE stockticker LIKE '${ticker}';"
	    bash "CREATE TEMPORARY TABLE CombinedDates${ticker}Details AS SELECT * FROM DatesList LEFT OUTER JOIN ${ticker}Details ON DatesList.date = ${ticker}Details.date;"
	    sqlite3 $databasefilename "CREATE TEMPORARY TABLE CombinedDates${ticker}Details AS SELECT * FROM DatesList LEFT OUTER JOIN ${ticker}Details ON DatesList.date = ${ticker}Details.date;"
	done
    done
fi

if [[ $# -eq 12 ]]
then 
    databasefilename="${1}"
    databaselist=('BC20') # 'IBD50' '8585' 'Top200Composite')
    for database in $databaselist
    do 
#	echo "CREATE  TABLE TimesOnList AS SELECT stockticker,count(stockticker) AS count_sticker FROM $database GROUP BY stockticker;"

#this query is for 
#	sqlite3 $databasefilename "DROP TABLE IF EXISTS $database.TimesOnList;"
#	sqlite3 $databasefilename "CREATE TABLE IF NOT EXISTS ${database}TimesOnList AS SELECT stockticker,count(stockticker) AS count_sticker FROM $database GROUP BY stockticker;"


#	echo "CREATE  TABLE DatesList AS SELECT DISTINCT(date) AS distinct_date FROM $database;"
	sqlite3 $databasefilename "DROP TABLE IF EXISTS ${database}_DatesList;"
	sqlite3 $databasefilename "CREATE TABLE IF NOT EXISTS ${database}_DatesList AS SELECT DISTINCT(date) FROM $database;"

#	echo "select distinct(stockticker) from ${database}"
	tickerlist=$(sqlite3 $databasefilename  "SELECT distinct(stockticker) FROM ${database}")
	for ticker in $tickerlist 
	do 
#	    echo "DROP TABLE IF EXISTS ${database}_${ticker}Details;"
	    sqlite3 $databasefilename "DROP TABLE IF EXISTS ${database}_${ticker}Details;"
#	    echo "CREATE  TABLE ${ticker}Details AS SELECT rank,date FROM ${database} WHERE stockticker LIKE \"${ticker}\";"

	    sqlite3 $databasefilename "CREATE TABLE ${database}_${ticker}Details AS SELECT rank,date FROM ${database} WHERE stockticker LIKE '${ticker}';"
#	    echo "CREATE  TABLE CombinedDates${ticker}Details AS SELECT * FROM DatesList LEFT OUTER JOIN ${ticker}Details ON DatesList.date = ${ticker}Details.date;"
	    sqlite3 $databasefilename "DROP TABLE IF EXISTS ${database}_CombinedDates${ticker}Details;"
	    sqlite3 $databasefilename "CREATE TABLE ${database}_CombinedDates${ticker}Details AS SELECT * FROM ${database}_DatesList LEFT OUTER JOIN ${database}_${ticker}Details ON ${database}_DatesList.date = ${database}_${ticker}Details.date;"


	    sqlite3 $databasefilename "CREATE TABLE ${database}_${ticker}_Master AS SELECT * FROM ${ticker} INNER JOIN ${database}_CombinedDates${ticker}Details ON ${ticker}.date = ${database}_CombinedDates${ticker}Details.date;  " 
	    echo "
damn it since all the previous tables are superfluous, I realize that a temp table with the end result being a 
permanent table is the true desired result. The other tables are then discarded once we have the final result.
But how do I get the temp tables to persist for as long as I need them to?"
	done
    done
fi

if [[ $# -eq 1 ]]
then 
echo "
this does all the temp work in one query so that only the desired resultant database is left"
    databasefilename="${1}"
#    databaselist=('BC20') # 'IBD50' '8585' 'Top200Composite') #for testing
    databaseArray=('BC20' 'IBD50' '8585' 'Top200Composite') #for production
    for((i=0;i<${#databaseArray[@]};i++))
    do
        database=${databaseArray[${i}]}
    	echo "Working on ${database}"
	sqlite3 $databasefilename "DROP TABLE IF EXISTS ${database}_DatesList;
CREATE TABLE IF NOT EXISTS ${database}_DatesList AS SELECT DISTINCT(date) FROM $database;"
	tickerlist=$(sqlite3 $databasefilename  "SELECT distinct(stockticker) FROM ${database}")
	for ticker in $tickerlist 
	do 

	    sqlite3 $databasefilename "DROP TABLE IF EXISTS ${database}_${ticker}Details;
	    CREATE TEMPORARY TABLE ${database}_${ticker}Details AS SELECT rank,date FROM ${database} WHERE stockticker LIKE '${ticker}';
	    DROP TABLE IF EXISTS ${database}_CombinedDates${ticker}Details;
	    CREATE TEMPORARY  TABLE ${database}_CombinedDates${ticker}Details AS SELECT * FROM ${database}_DatesList LEFT OUTER JOIN ${database}_${ticker}Details ON ${database}_DatesList.date = ${database}_${ticker}Details.date;
            DROP TABLE IF EXISTS ${database}_${ticker}_Master;
	    CREATE TABLE ${database}_${ticker}_Master AS SELECT * FROM ${ticker} INNER JOIN ${database}_CombinedDates${ticker}Details ON ${ticker}.date = ${database}_CombinedDates${ticker}Details.date;  " 
	done
    done
fi


# sqlite> .schema BC20_PCP_Master
# CREATE TABLE BC20_PCP_Master(
#   Date TEXT,
#   Open REAL,
#   High REAL,
#   Low REAL,
#   Close REAL,
#   Volume INT,
#   Adj_Close REAL,
#   "Date:1" TEXT,
#   Rank INT,
#   "Date:2" TEXT
# );

