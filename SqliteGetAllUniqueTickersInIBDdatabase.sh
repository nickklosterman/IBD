#!/bin/bash

#pull all over the unique tickers from each table
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from IBD50 ORDER BY stockticker asc;' > /tmp/tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from BC20 ORDER BY stockticker asc;' >> /tmp/tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from IBD8585 ORDER BY stockticker asc;' >> /tmp/tickers.txt
sqlite3 IBDdatabase.sqlite 'SELECT distinct(stockticker) from Top200Composite ORDER BY stockticker asc;' >> /tmp/tickers.txt

#sort the tickers
sort /tmp/tickers.txt -u > uniquetickers.txt

echo "Unique tickers in uniquetickers.txt"
