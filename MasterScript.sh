#!/bin/bash
python Scripts/DualPrepForDatabase.py3
bash VerifyTickers.sh
bash BadTickerDataLocator.sh BadTickerList.txt
