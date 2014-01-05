#!/usr/bin/python
'''
this script is meant to recover the tickers from a file which contains the raw text copied form the eIBD pdf and placed in a text file. 
it currently uses a hardcoded input file and date for the output json.
json-like output is produced which is appropriate to be used later on for PythonStockTracker
'''
inputFile="top200composite20100114.txt"
fileHandle=open(inputFile,'r')
#fileHandle.write(output)
counter=1
for line in fileHandle:
    elements=line.split(' ')
    #print(elements)
    closingPrice=elements[len(elements)-3]
    #print(elements[len(elements)-4],counter,closingPrice,"2010-01-14") #I am grabbing the fourth element from the back as that is the shortest route to just grabbing the ticker
    print("{ \"ticker\":\"%s\", \"shares\":1, \"totalPurchasePrice\":%s, \"purchaseDate\":\"%s\", \"commissionToBuy\":0, \"commissionToSell\":0}," % (elements[len(elements)-4],closingPrice,"01/14/2010")) 
    counter+=1
fileHandle.close()
