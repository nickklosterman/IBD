#!/bin/bash

#get list of all stock symbols
#get current quote of all stock symbols
#compare current quote to past quote when on IBD100 List
# loop over mysql output
# grep appropriate line in quote file
# parse out price
# perform math calc using bc
# printout comparison line by line

function QueryForQuote() #OLD METHOD
{
    symbol=$1
    quote=$(curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=${symbol}&f=l1" | sed 's/.$//' ) #the trailing sed command strips a ^M that was at the end of each quote price
    if [ $quote == "0.00" ]
    then
#        echo "uh oh!"
	echo "$symbol" >> BadStockTickers.txt
    fi
    echo ${symbol} ${quote}
    
}
function QueryForAllTickers()
{
    symbol=$1
    quote=$(curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=${symbol}&f=sl1" | sed 's/.$//' ) #the trailing sed command strips a ^M that was at the end of each quote price
#    echo ${symbol} ${quote}
 echo ${quote}   
}


if [ $# -lt 1 ]
then
    echo "scriptname.sh directions;"
else
    if [ -f "BadStockTickers.txt" ]
    then 
	rm BadStockTickers.txt
    fi
    if [ -f "$1" ] #if we specified a file on the command line then read the file and spit it out else parse args as stock tickers
    then
	while read LINE
	do
	    ticker=$(echo "$LINE" | tr '[a-z]' '[A-Z]' )
	    Alltickers="${ticker}+${Alltickers}"
	    QueryForQuote $ticker #OLD METHOD performs the query one ticker at a time which is a bit slow
	done < "$1"
#       echo "$Alltickers"
#	QueryForAllTickers $Alltickers
    else 
	until [ -z "$1" ] #parse args as stock tickers
	do
	    ticker=$(echo "$1" | tr '[a-z]' '[A-Z]' )
	    QueryForQuote $ticker
	    shift
	done 
	echo "Could specify a file full of stock tickers, one per line."
    fi
    if [ -f "BadStockTickers.txt" ] 
    then 
	echo "Bad Stock Tickers:"
	cat BadStockTickers.txt
    fi
fi
#http://www.commandlinefu.com/commands/view/2086/command-line-to-get-the-stock-quote-via-yahoo
#http://www.seangw.com/wordpress/index.php/2010/01/formatting-stock-data-from-yahoo-finance/   for formatting options
<<EOF 
s – Symbol
n – Name
l – Last Trade (with time)
l1 – Last Trade (without time)
d1 – Last Trade Date
t1 – Last Trade Time
k3 – Last Trade Size
c – Change and Percent Change
c1 – Change
p2 – Change in Percent
t7 – Ticker Trend
v – Volume
a2 – Average Daily Volume
i – More Info
t6 – Trade Links
b – Bid
b6 – Bid Size
a – Ask
a5 – Ask Size
p – Previous Close
o – Open
m – Day’s Range
w – 52 Week Range
j5 – Change from 52 Week Low
j6 – Percent Change from 52 Week Low
k4 – Change from 52 Week High
k5 – Percent Change from 52 Week High
e – Earnings/Share
r – P/E Ratio
s7 – Short Ratio
r1 – Dividend Pay Date
q – Ex-Dividend Date
d – Dividend/Share
y – Dividend Yield
f6 – Float Shares
j1 – Market Capitalization
t8 – 1 Year Target Price
e7 – EPS Est. Current Year
e8 – EPS Est. Next Year
e9 – EPS Est. Next Quarter
r6 – Price/EPS Est. Current Year
r7 – Price/EPS Est. Next Year
r5 – PEG Ratio
b4 – Book Value
p6 – Price/Book
p5 – Price/Sales
j4 – EBITDA
m3 – 50 Day Moving Average
m7 – Change from 50 Day Moving Average
m8 – Percent Change from 50 Day Moving Average
m4 – 200 Day Moving Average
m5 – Change from 200 Day Moving Average
m6 – Percent Change from 200 Day Moving Average
s1 – Shares Owned
p1 – Price Paid
c3 – Commission
v1 – Holdings Value
w1 – Day’s Value Change
g1 – Holdings Gain Percent
g4 – Holdings Gain
d2 – Trade Date
g3 – Annualized Gain
l2 – High Limit
l3 – Low Limit
n4 – Notes
k1 – Last Trade (Real-time) with Time
b3 – Bid (Real-time)
b2 – Ask (Real-time)
k2 – Change Percent (Real-time)
c6 – Change (Real-time)
v7 – Holdings Value (Real-time)
w4 – Day’s Value Change (Real-time)
g5 – Holdings Gain Percent (Real-time)
g6 – Holdings Gain (Real-time)
    m2 – Day’s Range (Real-time)
    j3 – Market Cap (Real-time)
    r2 – P/E (Real-time)
    c8 – After Hours Change (Real-time)
    i5 – Order Book (Real-time)
    x – Stock Exchange
    if you do not want to work with a csv file, you can get the same information using the following command which will return an xml.
	http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20%28%22xel.l%22%29 &diagnostics=false&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys
EOF