#!/bin/bash
python Scripts/DualPrepForDatabase.py
bash VerifyTickers.sh
bash BadTickerLocator.sh BadTickerList.txt
