#!/bin/bash
python GetStockDataForAllDates.py3 -i BC20 -o StockData -d IBDdatabase.sqlite
python GetStockDataForAllDates.py3 -i IBD50 -o StockData -d IBDdatabase.sqlite
python GetStockDataForAllDates.py3 -i IBD8585 -o StockData -d IBDdatabase.sqlite
python GetStockDataForAllDates.py3 -i Top200Composite -o StockData -d IBDdatabase.sqlite
