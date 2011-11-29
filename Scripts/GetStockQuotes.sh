#!/bin/bash

#get list of all stock symbols
#get current quote of all stock symbols
#compare current quote to past quote when on IBD100 List
# loop over mysql output
# grep appropriate line in quote file
# parse out price
# perform math calc using bc
# printout comparison line by line

function QueryForQuote()
{
    symbol=$1
    quote=$(curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=${symbol}&f=l1" | sed 's/.$//' ) #the trailing sed command strips a ^M that was at the end of each quote price
    if [ $quote == "0.00" ]
    then
        echo "uh oh!"
    fi
    echo ${symbol} ${quote}
    
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
	    QueryForQuote $ticker
	done < "$1"
    else 
	until [ -z "$1" ] #parse args as stock tickers
	do
	    ticker=$(echo "$1" | tr '[a-z]' '[A-Z]' )
	    QueryForQuote $ticker
#	    symbol=$1
#	url="'http://download.finance.yahoo.com/d/quotes.csv?s=${symbol}&f=l1'"
#echo $url
#	    quote=$(curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=${symbol}&f=l1" | sed 's/.$//' ) #the trailing sed command strips a ^M that was at the end of each quote price
#	    if [ $quote == "0.00" ]
#	    then 
#		echo "uh oh!"
#	    fi
#	    echo ${symbol} ${quote}
	    shift
	done 
	
	echo "could check if the cli arg is a file and attempt to open otherwise treat as a stock symbol and do a query"
    fi
fi
#http://www.commandlinefu.com/commands/view/2086/command-line-to-get-the-stock-quote-via-yahoo