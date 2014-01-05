#!/bin/bash
echo "Begin SqliteGetAllUniqueTickersInIBDdatabase.sh Execution"
echo "
This script outputs a list of the unique sorted stock tickers 
from IBD50,BC20,IBD8585 and Top200Composite"

#pull all over the unique tickers from each table
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from IBD50 ORDER BY stockticker asc;' > /tmp/Tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from BC20 ORDER BY stockticker asc;' >> /tmp/Tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from IBD8585 ORDER BY stockticker asc;' >> /tmp/Tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from Top200Composite ORDER BY stockticker asc;' >> /tmp/Tickers.txt

#sort the tickers
sort /tmp/Tickers.txt -u > /tmp/uniquetickers.txt

echo "Unique tickers in /tmp/uniquetickers.txt"

if [ -e /tmp/tickerurlfile.txt ]
then
    rm /tmp/tickerurlfile.txt
fi

while read symbol
do
    #echo "\"http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv\" -O ${symbol}.csv" >> /tmp/tickerurlfile.txt
    echo "http://ichart.yahoo.com/table.csv?s=${symbol}&ignore=.csv" >> /tmp/tickerurlfile.txt
done < /tmp/uniquetickers.txt

# cat /tmp/tickerurlfile.txt | parallel "wget {}"

# # Remove files of length/size 0
# find . -type f -size 0 -print0 | xargs -0 rm 

#to determine how risky an investment would've been, do a query to find the min and max of each ticker and get the dates. see how close the dates are as well.

#TFLN can be parallelized as well
echo "End SqliteGetAllUniqueTickersInIBDdatabase.sh Execution"
