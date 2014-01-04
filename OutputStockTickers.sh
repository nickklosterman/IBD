#!/bin/bash
if [ -e /tmp/TickerList.txt ]
then 
echo "Overwriting /tmp/Tickerlist.txt"
fi

sqlite3 IBDdatabase.sqlite "select distinct stockticker from IBD8585" > /tmp/TickerList.txt
sqlite3 IBDdatabase.sqlite "select distinct stockticker from IBD50" >> /tmp/TickerList.txt
sqlite3 IBDdatabase.sqlite "select distinct stockticker from BC20" >> /tmp/TickerList.txt
sqlite3 IBDdatabase.sqlite "select distinct stockticker from Top200Composite" >> /tmp/TickerList.txt

#S----------------> superseded by SqliteGetAllUniqueTickersInIBDdatabase.sh
