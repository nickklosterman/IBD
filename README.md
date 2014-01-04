This is a set of data and accompanying bash scripts to organize various stock lists into sqlite3 databases for analysis by programs.

---Data/----------
Data/: Main IBD lists that I follow
Data/8585.txt - Friday 85/85 listing:  All stocks above $10, within 15% of 12-month high, Earnings Per Share (EPS) Rating and Relative Price Strength (RS) Rating of 85 or more and average daily volume of 10,000 or more are shown in order of Industry Group Relative Strength Rating.
Data/BC20.txt
Data/IBD50.txt
Data/IBDListDefinitions.txt Definitions of the lists from the investors.com website
Data/OpenAllIBDListFiles.sh - Script to open my main lists all at once in emacs
Data/TODO
Data/Top200Composite.txt

Data/ExchangeCompanyListings: - Ticker Lists, mainly used for determining ticker changes
AMEXcompanylist.csv
ChangeTickerList.txt  
NASDAQcompanylist.csv
NASDAQ_NYSE_Sources.txt - States where I downloaded the company lists for each exchange
NASDAQ.txt
NYSEcompanylist.csv
NYSE.txt
StockTickerChangeList.txt
StockTickerSourceInstructions.txt

Data/SecondaryLists: - Other lists which I don't update as frequently and some misc data
IBDSubgroups.txt
NewAmerica.txt
Top15World.txt
TopUSDiversifiedETFs.txt

---Scripts/--------
