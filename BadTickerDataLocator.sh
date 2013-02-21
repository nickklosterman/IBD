#!/bin/bash

echo "create an ignore or solved table, and query that first and if it doesn't return anything then continue\ni.e. look for it in the solved table first and if it isnt solved then attempt to 'solve' it"
echo "also create a script that runs dualprep and then verifytickers and this so we don't have"

filename=$1
#for tickernotfound in "fx" "eew" "eqqm"
while read LINE
do
    tickernotfound=$LINE
    echo "----" $tickernotfound "-----"
    for table in "ibd8585" "ibd50" "bc20" "top200composite"
    do
	echo $table
	results=$(sqlite3 IBDdatabase.sqlite "select date from $table where stockticker like '$tickernotfound' order by date desc;")
	if [[ $results == "" ]]
	then
	    echo "empty"
	else
	    echo $results
	fi
    done
done < $filename

#sqlite3 IBDdatabase.sqlite "select date from ibd8585 where stockticker like 'fx' order by date desc;"
