#!/bin/bash
python Scripts/DualPrepForDatabase.py3
bash VerifyTickers.sh
echo "output written to /tmp/TickerListDataLocatorOutput.txt"
bash BadTickerDataLocator.sh BadTickerList.txt > BadTickerListDataLocatorOutput.txt
