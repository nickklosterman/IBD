#!/bin/bash

echo "Begin BadTickerDataLocator.sh Execution"

function instructions() {
echo "
This script takes a list of bad tickers as a file,
it then loops over each ticker and queries the IBDdatabase.sqlite
file locating the records location in the database.
The list of bad tickers is obtained by running the 
VerifyTickers.sh script.
"
}

echo "create an ignore or solved table, and query that 
first and if it doesn't return anything then 
continue i.e. look for it in the solved table 
first and if it isnt solved then attempt to 'solve' 
it also create a script that runs dualprep and then 
verifytickers and this so we don't have"

if [[ $# -lt 2 ]]
then 
    echo "usage: $0 badtickerlist.txt"
    instructions
else 
    filename=$1
    #for tickernotfound in "fx" "eew" "eqqm"
    while read LINE
    do
	tickernotfound=$LINE
	echo "----" $tickernotfound "-----"
	for table in "IBD8585" "IBD50" "BC20" "TOP200Composite"
	do
	    echo $table
	    results=$(sqlite3 IBDdatabase.sqlite "select date from $table where stockticker like '$tickernotfound' order by date desc;")
	    if [[ $results == "" ]]
	    then
		echo "empty" #this shouldn't happen as the tiker came from the database originally, so it MUST be found in it.
	    else
		echo $table - $results
	    fi
	done
    done < $filename
fi
#sqlite3 IBDdatabase.sqlite "select date from ibd8585 where stockticker like 'fx' order by date desc;"

echo "End BadTickerDataLocator.sh Execution"
