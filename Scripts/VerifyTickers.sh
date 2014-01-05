#!/bin/bash

function instructions() {
echo "This program verifies stock tickers in bulk.
It first obtains a list of all unique tickers 
in our database. It then attempts to get the
most recent stock data from Yahoo for that
ticker. If N/A is returned then that ticker
is marked as a dead ticker.
I believe that if this script is run on a day
when the market is closed all tickers will 
show as invalid.

"
}
echo "Begin VerifyTickers.sh Execution"
echo "This assumes $0 is being called from one directory below the Scripts/ 
directory, otherwise the following call to Scripts/SqliteGetAllUniqueTickersInIBDdatabase.sh won't work."
bash Scripts/SqliteGetAllUniqueTickersInIBDdatabase.sh

# if [ 1 -eq 0 ]
# then

#     bash ~/Git/BashScripts/Financial/StockScripts/GetCompanyNameFromTicker.sh /tmp/TickerList.txt #this is slow bc it pings fo reach separate ticker symbol

#     number=$( wc -l /tmp/TickerList.txt )
#     echo "There are $number stock tickers to query"
#     counter=0
#     tickerlist=""
#     #while [ $counter -lt $number ] 
#     while read LINE
#     do
# 	tickerlist="${tickerlist}"$LINE","
# 	let counter 
#     done < /tmp/TickerList.txt
#     url="http://download.finance.yahoo.com/d/quotes.csv?s=${tickerlist}&f=sl1d1t1c1ohgv&e=.csv"
#     echo $url
#     wget $url -O /tmp/output.txt

#     less /tmp/output.txt
# fi

if [ -e /tmp/Tickers.txt ]
then
    echo "Removing the existing /tmp/Tickers.txt file"
    rm /tmp/Tickers.txt
fi

# #filecontent=$( ` cat "/tmp/TickerList.txt"` | sort | uniq ) #this will cut down repeats a bit across the three (or more) indexes we follow
# filecontent=$(  cat "/tmp/TickerList.txt" | sort | uniq ) #this will cut down repeats a bit across the three (or more) indexes we follow

# #NOTE: the statement above and the following two statements are very different. The first one places each line into a separate array element. The second one puts all the elements into a single variable. Arrays are declared with parens () around them so they are needed outside the command expansion for the cat command.
# #filecontent=( $(  cat "/tmp/TickerList.txt" )) filecontent=$(  cat "/tmp/TickerList.txt" )

# #http://www.thegeekstuff.com/2010/06/bash-array-tutorial/
# filecontent=( $(  cat "/tmp/TickerList.txt" | sort | uniq )) #place tickers in array


#/tmp/uniuqetickers.txt should be produced by SqliteGetAllUniqueTickersInIBDdatabase.sh
filecontent=( $(  cat "/tmp/uniquetickers.txt" )) #place tickers in array

#Yahoo limits quotes to 200 per request
limit=200
#counter=0
# if [ 1 -eq 0 ]
# then
#     for item in "${filecontent[@]}"
#     do
# 	echo -n ${item}","
#     done
# fi

#build list of 199 stock tickers, when we reach 199 tickers then get data
for item in $(seq 0 $((${#filecontent[@]} - 1 )))
do
    #echo -n ${filecontent[$item]}","
    templist=$templist+${filecontent[$item]}","
    #echo $item
    # when we hit the count limit, we perform our wget call. This hits the Yahoo api, bad tickers have N/A results
    let "flag = ( $item + 1 ) % $limit"
    if [[ $flag -eq 0 ]]
    then 
	url="http://download.finance.yahoo.com/d/quotes.csv?s=${templist}&f=sl1d1t1c1ohgv&e=.csv"
	wget -q $url -O - >> "/tmp/Tickers.txt"   
	templist=""
    fi
done

#do it one more time for the ones in the buffer still
url="http://download.finance.yahoo.com/d/quotes.csv?s=${templist}&f=sl1d1t1c1ohgv&e=.csv"
#echo $url "HERRO"
wget -q $url -O - >> "/tmp/Tickers.txt"

#Bad tickers have N/A as the result
echo "These are the tickers with N/A results:"
grep "N/A" /tmp/Tickers.txt | sed 's/",.*//;s/"//' #awk '{ print $1 }'

#touch BadTickerList.txt #this is needed if file not all ready created? NO
#add the current date and append the badtickers into BadTickerList.txt
date +%F >> BadTickerList.txt
grep "N/A" /tmp/Tickers.txt | sed 's/",.*//;s/"//' >> BadTickerList.txt

#NOTE: if you try to run this (without restricting the fields you look at) when the market isn't open then all tickers will have an N/A field

# DUPLICATE Method
# #touch BadTickerList.txt #this is needed if file not all ready created? NO
# date +%F >> BadTickerList.txt
# cut -d , -f 1-3 /tmp/Tickers.txt |grep "N/A"  | sed 's/",.*//;s/"//' >> BadTickerList.txt

echo "End VerifyTickers.sh Execution"
