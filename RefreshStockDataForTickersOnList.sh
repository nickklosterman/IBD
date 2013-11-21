#!/bin/bash

database="${1}"

#pull all over the unique tickers from each table
sqlite3 "${database}" 'SELECT distinct(stockticker) from IBD50 ORDER BY stockticker asc;' > /tmp/tickers.txt
sqlite3 "${database}" 'SELECT distinct(stockticker) from BC20 ORDER BY stockticker asc;' >> /tmp/tickers.txt
sqlite3 "${database}" 'SELECT distinct(stockticker) from IBD8585 ORDER BY stockticker asc;' >> /tmp/tickers.txt
sqlite3 "${database}" 'SELECT distinct(stockticker) from Top200Composite ORDER BY stockticker asc;' >> /tmp/tickers.txt

#sort the tickers
sort /tmp/tickers.txt -u > /tmp/uniquetickers.txt

echo "Unique tickers in uniquetickers.txt"

rm /tmp/tickerurlfile.txt
while read symbol
do
#echo "\"http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv\" -O ${symbol}.csv" >> /tmp/tickerurlfile.txt
echo "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" >> /tmp/tickerurlfile.txt
done < /tmp/uniquetickers.txt

cat /tmp/tickerurlfile.txt | parallel "wget {}"

# Remove files of length/size 0
find . -type f -size 0 -print0 | xargs -0 rm 


python Scripts/ImportCSVStockDataToSQLite.py3  umm I think I want the one with bulk transactions....


#to determine how risky an investment would've been, do a query to find the min and max of each ticker and get the dates. see how close the dates are as well.


