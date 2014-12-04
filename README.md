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

Process for entering new data
=============================
Stick the IBD pdf files in a directory.

Run `Scripts/touchAndOpenIBDTxtFiles.sh`. This will create and open a file named `<pdffilename>.txt`.

Open the pdf and extract the data and place it into the `<pdffilename>.txt`. You must manually copy out the relevant chunks and paste them into the appropriate `<pdffilename>.txt` file. For Top 200, copy out the entire table. For 85-85/Week In Review, copy the side table and not the box data. For IBD50 & BC20 copy the box data. 

Run `ExtractionAndInsertionRunner.sh /path/to/directory test` from the `/Scripts/` directory, pointing to the directory where the `<pdffilename>.txt` files are to test the data before entering.
E.g. `bash ExtractionAndInsertionRunner.sh /tmp/ test`

When you are satisfied that all data has been properly extracted, run `ExtractionAndInsertionRunner.sh /path/to/directory`. This will copy the extracted data into the appropriate files in `/Data/`

Generate SVG Plots of Data
==========================
Run `MasterScript.sh`