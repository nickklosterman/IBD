#!/bin/bash


function DownloadYahooDataFile() 
{
    symbol=$1
    wget  "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" -O ${symbol}.csv
}


if [ $# -lt 1 ]
then
    echo "scriptname.sh directions;"
else
    if [ -f "$1" ] #if we specified a file on the command line then read the file and spit it out else parse args as stock tickers
    then
	while read LINE
	do
	    ticker=$(echo "$LINE" | tr '[a-z]' '[A-Z]' )
	    DownloadYahooDataFile $ticker
	done < "$1"
    else 
	until [ -z "$1" ] #parse args as stock tickers
	do
	    ticker=$(echo "$1" | tr '[a-z]' '[A-Z]' )
	    DownloadYahooDataFile $ticker
	    shift
	done 

    fi
fi
