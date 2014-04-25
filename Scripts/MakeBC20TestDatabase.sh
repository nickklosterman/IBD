#!/bin/bash
echo "
This program strips all but the BC20 database from a given database.
Good for creating a minimal test database.
"

function dropTable(){ 
        inputDatabase="${1}"
table="${2}"
    echo "Removing ${table} from ${inputDatabase}"
    sqlite3 "${inputDatabase}" "DROP TABLE IF EXISTS ${table};" 
}


if [ $# -ne 2 ]
then 
    echo "Please supply a database to use."
    echo "$0 DatabaseWithTickerLists.sqlite OutputHistoricalStockDatabase.sqlite"
else
    inputDatabase="${1}"
    backupDatabase="${2}"
    if [ ! "${outputDatabase}" = "" ]
    then
	echo "Making a copy of the original database (${inputDatabase}) name ${backupDatabase}."
	cp "${inputDatabase}" "${backupDatabase}"
    fi


    #    tableArray=(BC20StockData  BC20ErrorStockData  IBD50StockData  IBD50StockDataError  Top200CompositeStockData  Top200CompositeStockDataError  BC20StockDataError  IBD8585StockData  IBD8585StockDataError  IBD50ContinuousRun  BC20ContinuousRun  IBD8585ContinuousRun  Top200CompositeContinuousRun  StockData  StockDataError  IBD50  IBD50Error  BC20  BC20Error  IBD8585  IBD8585Error  Top200Composite  Top200CompositeError )
    tableArray=(BC20StockData  BC20ErrorStockData  IBD50StockData  IBD50StockDataError  Top200CompositeStockData  Top200CompositeStockDataError  BC20StockDataError  IBD8585StockData  IBD8585StockDataError  IBD50ContinuousRun  BC20ContinuousRun  IBD8585ContinuousRun  Top200CompositeContinuousRun  StockData  StockDataError  IBD50  IBD50Error    BC20Error  IBD8585  IBD8585Error  Top200Composite  Top200CompositeError ) #Leave the BC20 database

    for((i=0;i<${#tableArray[@]};i++))
    do
        dropTable ${inputDatabase} ${tableArray[${i}]} 
    done
fi
