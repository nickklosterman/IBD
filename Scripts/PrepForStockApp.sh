#!/bin/bash
inputdatabase="${1}"
backupdatabase="${2}"
bash Scripts/RefreshStockDataForTickersOnList.sh "${inputdatabase}" "${inputdatabase}"
if [ ! "${backupdatabase}" = "" ]
then 
    bash Scripts/CreateMasterDateRankStockDataAnalysisDatabases.sh  "${inputdatabase}"  "${backupdatabase}"
else
    bash Scripts/CreateMasterDateRankStockDataAnalysisDatabases.sh  "${inputdatabase}" 
fi
echo "
Completed Database can be found at ${inputdatabase}.
Copy ${inputdabase} to your stock app directory.
"

