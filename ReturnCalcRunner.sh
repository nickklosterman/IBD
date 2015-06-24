#!/bin/bash

# usage : bash script IBDdatabase.sqlite 2015-01-01 2015-06-01

# This script is meant to loop over the given database file and compute the return from the first time the stock appeared on the list to the current day

database=$1 #"IBDdatabase.sqlite.12072014"
date=`date +%Y-%m-%d`

#these are the limits we will perform our sql query inside; there may be no data returned for these limits. If there is data returned, mindate & maxdate will hold the dates for the first and last datapoint inside the query limits
querymindate=$2  #2015-01-01
querymaxdate=$3 #2015-05-31


for table in Top200Composite #"BC20" #"IBD50" "BC20" "Top200Composite" "IBD8585"
#for table in "IBD50" "BC20" "Top200Composite" "IBD8585"
do

    tickerlist=$(sqlite3 $database "SELECT distinct(stockticker) FROM ${table}") # compute datapoint for all tickers
#    tickerlist=$(sqlite3 $database "SELECT stockticker FROM ${table} where date in ( select max(date) from ${table})") #this will only create datapoints for the tickers present on the most recent list; instead of `in` I could've used `like` or `=` 
    for ticker in $tickerlist
    do 
	mindate=$(sqlite3 "$database" 'SELECT min('"$table"'_'"$ticker"'_Master.Date) FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" )' )
	mindatelength=${#mindate}

	if [[ $mindatelength -eq 10 ]]
	then 
	    maxdate=`sqlite3 "$database" 'SELECT max('"$table"'_'"$ticker"'_Master.Date) FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" )' `
            if [[ 1 -eq 10 ]]
               then
	    tickerStartOpen=$(sqlite3 "$database" 'SELECT '"$table"'_'"$ticker"'_Master.Open FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.date ASC LIMIT 1' )
            tickerFinishOpen=$(sqlite3 "$database" 'SELECT '"$table"'_'"$ticker"'_Master.Open FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.date DESC LIMIT 1' )
            tickerReturn=$( echo  "scale=3;($tickerFinishOpen-$tickerStartOpen)/$tickerStartOpen" | bc )
	        sp500StartOpen=$(sqlite3 "$database" 'SELECT  _GSPC.Open as SP500Open  FROM '"$table"'_'"$ticker"'_Master INNER JOIN _GSPC ON '"$table"'_'"$ticker"'_Master.Date =  _GSPC.Date WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.Date ASC LIMIT 1' )
	        sp500FinishOpen=$(sqlite3 "$database" 'SELECT  _GSPC.Open as SP500Open  FROM '"$table"'_'"$ticker"'_Master INNER JOIN _GSPC ON '"$table"'_'"$ticker"'_Master.Date =  _GSPC.Date WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.Date DESC LIMIT 1' )
                spReturn=$( echo "scale=3;($sp500FinishOpen-$sp500StartOpen)/$sp500StartOpen" | bc )
                echo "$ticker,$mindate,$maxdate,$tickerStartOpen,$tickerFinishOpen,$tickerReturn,$sp500StartOpen,$sp500FinishOpen,$spReturn"
            else
          tickerStartAdj_Close=$(sqlite3 "$database" 'SELECT '"$table"'_'"$ticker"'_Master.Adj_Close FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.date ASC LIMIT 1' )
            tickerFinishAdj_Close=$(sqlite3 "$database" 'SELECT '"$table"'_'"$ticker"'_Master.Adj_Close FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.date DESC LIMIT 1' )
            tickerReturn=$( echo  "scale=3;($tickerFinishAdj_Close-$tickerStartAdj_Close)/$tickerStartAdj_Close" | bc )
	        sp500StartAdj_Close=$(sqlite3 "$database" 'SELECT  _GSPC.Adj_Close as SP500Adj_Close  FROM '"$table"'_'"$ticker"'_Master INNER JOIN _GSPC ON '"$table"'_'"$ticker"'_Master.Date =  _GSPC.Date WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.Date ASC LIMIT 1' )
	        sp500FinishAdj_Close=$(sqlite3 "$database" 'SELECT  _GSPC.Adj_Close as SP500Adj_Close  FROM '"$table"'_'"$ticker"'_Master INNER JOIN _GSPC ON '"$table"'_'"$ticker"'_Master.Date =  _GSPC.Date WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.Date DESC LIMIT 1' )
                spReturn=$( echo "scale=3;($sp500FinishAdj_Close-$sp500StartAdj_Close)/$sp500StartAdj_Close" | bc )
                echo "$ticker,$mindate,$maxdate,$tickerStartAdj_Close,$tickerFinishAdj_Close,$tickerReturn,$sp500StartAdj_Close,$sp500FinishAdj_Close,$spReturn"
                
            fi
            
	else
	    echo "phail $ticker" 1>&2 #print to stderr
	fi 
    done
done

echo "You really want to use the adjusted close as this takes into account any stock splits.Might have to do goofy math where you take the adjusted close of the day before you bought. Fuck it doesn't matter since it is pretend. Buffett doesn't care about one day difference. "
echo "NOTE: if any stock doesn't span until your end date, it is bc the stock was delisted / bought"




