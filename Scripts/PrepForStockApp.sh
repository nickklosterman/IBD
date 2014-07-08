#!/bin/bash
if [[ $# -ne 1 ]] && [[ $# -ne 2 ]]
then 
    echo "
Please specify at least an input database to use.
$0 inputDatabase [ backupdatabasename ] 
"
else

    inputdatabase="${1}"
    backupdatabase="${2}"
    bash Scripts/RefreshStockDataForTickersOnList.sh "${inputdatabase}" "${inputdatabase}"
    if [ ! "${backupdatabase}" = "" ]
    then 
	bash Scripts/CreateMasterDateRankStockDataAnalysisDatabases.sh  "${inputdatabase}"  "${backupdatabase}"
	echo "
Completed Database can be found at ${outputdatabase}.
Copy ${outputdabase} to your stock app directory.
"
    else
	bash Scripts/CreateMasterDateRankStockDataAnalysisDatabases.sh  "${inputdatabase}" 
	echo "
Completed Database can be found at ${inputdatabase}.
Copy ${inputdabase} to your stock app directory.
"
    fi

fi
