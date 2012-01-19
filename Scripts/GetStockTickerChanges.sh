#!/bin/bash
echo "This script grabs the stock ticker change list from nasdaq.com."
#grab the initial page
wget http://www.nasdaq.com/markets/stocks/symbol-change-history.aspx -O /tmp/NASDAQ
numberofpages=$(grep pager /tmp/NASDAQ | grep http | sed 's/.*next//;s/.*http/http/;s/.*page=//;s/".*//')
echo $numberofpages
counter=1
#grab all the pages of the list of changed tickers
while [ $counter -le $numberofpages ]
do
echo $counter
wget http://www.nasdaq.com/markets/stocks/symbol-change-history.aspx?page=$counter -O /tmp/NASDAQ$counter
let 'counter+=1'
done

#concatenate the results into one file
#rm ChangeTickerList.txt
#grep "<td class=\"body2\">" /tmp/NASDAQ
grep body2 /tmp/NASDAQ* --no-filename | sed 's/<[^>]*>//g;s/^[ \t]*//;s/[ \t]*$//' >> ../Data/ChangeTickerList.txt





