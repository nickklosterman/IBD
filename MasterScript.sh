#!/bin/bash
echo "Begin MasterScript.sh Execution"
#grab data from the raw /Data/IBD50.txt,8585.txt etc files and properly insert them into a database 
python Scripts/DualPrepForDatabase.py3
bash Scripts/VerifyTickers.sh

#I have to put the begin/end echo statements here since I'm piping to a file.
echo "-Begin BadTickerDataLocator.sh Execution"
#this script below is giving me weird errors....Err it wasn't giving errors, I was piping the data to the file so only the errors were being shown!
bash Scripts/BadTickerDataLocator.sh BadTickerList.txt > BadTickerListDataLocatorOutput.txt #>-- these files will be local to the calling script so we don't need ../
echo "output written to BadTickerListDataLocatorOutput.txt"
echo "-End BadTickerDataLocator.sh Execution"

echo "End MasterScript.sh Execution"
