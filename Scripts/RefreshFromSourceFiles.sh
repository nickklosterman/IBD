#!/bin/bash

#store all the flat data in a fresh
if [ -e ${1} ]
python Scripts/DualPrepForDatabase.py3 -d ${1} #FreshDatabase.sqlite


#I believe the following two steps eliminate the need to call GetHistoricalPrices*.py3 Those are slow single shot grabs of data vs the bulk data download. If I really want to save space, I could just enter in only the data from these flat files that I cared about.
#create uniquetickers.txt
bash SqliteGetAllUniqueTickersInIBDdatabase.sh
#utilize uniquetickers to get all the historical stock data
bash BulkDownloadStockData.sh
#import that 
python ImportCSVStockDataToSQLite.py3 -d ${1}

#perform additional analysis
ListTimelineCreator.py3
python AnalayzeContinuousRunPerformance.py3
DaysOnListAnalyzer.py3
CreateTimeSeriesArrayFromSQLiteDB.py3 #this hasn't been tested in a while Fri Oct 11 21:54:50 EDT 2013
RankMatrix.SQLite.WriteFile.py3
MovementMatrix.py3
PortfolioJSONExporter.py3
