#!/bin/bash
python Scripts/DualPrepForDatabase.py
bash VerifyTickers.sh
bash BadTickerDataLocator.sh BadTickerList.txt
