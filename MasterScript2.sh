#!/bin/bash
echo "Begin MasterScript.sh Execution"
#date +%F gives date in YYYY-MM-DD
#grab data from the raw /Data/IBD50.txt,8585.txt etc files and
#properly insert them into a database
today=`date +%F`

python Scripts/DualPrepForDatabase.py3
bash Scripts/VerifyTickers.sh

#I have to put the begin/end echo statements here since I'm piping to a file.
echo "-Begin BadTickerDataLocator.sh Execution"
#this script below is giving me weird errors....Err it wasn't giving errors, I was piping the data to the file so only the errors were being shown!
bash Scripts/BadTickerDataLocator.sh BadTickerList.txt > BadTickerListDataLocatorOutput.txt #>-- these files will be local to the calling script so we don't need ../
echo "output written to BadTickerListDataLocatorOutput.txt"
echo "-End BadTickerDataLocator.sh Execution"
dateName=$( date +%Y-%m-%d )
bash Scripts/PrepForStockApp.sh IBDdatabase.sqlite.${dateName}
bash Scripts/IBDGnuplotter.sh IBDdatabase.sqlite.${dateName} 2013-07-15 ${today}
path="svgs/${today}/" 
mkdir $path

filePrefix=('Big Cap 20' 'CANSLIM Select' 'Global Leaders' 'IBD50' 'IPO Leaders' 'New High' 'Relative Strength At New High' 'Rising Profit Estimates' 'Sector Leaders' 'Stock Spotlight' 'Stocks That Funds Are Buying' 'Weekly Review')
for ((i = 0; i < ${#filePrefix[@]}; i++))
do
    mv ${fileprefix[$i]}*${date}.svg svgs/${today}
    python makeSVGPage.py ${fileprefix[$i]} ${path}
done


echo "End MasterScript.sh Execution"
