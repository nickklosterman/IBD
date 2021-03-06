#!/usr/bin/env/pythong
# -*- pythong -*- 
'''
contains helper functions
getHistoricalStockData - gets historical stock data for a given symbol,date pair from Yahoo
'''


'''
[DONE] TODO : a driver script 
python:
from YahooStockQuotes import getHistoricalStockData 
getHistoricalStockData("BWLD","2013-12-05")
this should return: 
[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], ['2013-12-05', '146.10', '149.63', '146.10', '148.00', '283500', '148.0']]

'''
import sys #for cmd line arguments
#from urllib import *
import urllib #for getting quotes from net
import urllib.error 
import urllib.request

import urllib.request, urllib.parse, urllib.error #for getting quotes from net

"""
you'll get the following error if you don't import urrllib.error 
 File "/home/puffjay/Repo/Github/IBD/Scripts/YahooStockQuotes.py", line 33, in getHistoricalStockPrices
    except urllib.error.HTTPError as err:

NOTE 
THIS WILL NOT WORK AS A MODULE AS http://docs.python.org/3/tutorial/modules.html#importing-from-a-package STATES THAT THE FILE MUST END IN .PY NOT .PY3
"""


def getHistoricalStockData(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
#the date goes month(jan=0) day year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date[5:7]) - 1) + \
          'e=%s&' % str(int(date[8:10])) + \
          'f=%s&' % str(int(date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(date[5:7]) - 1) + \
          'b=%s&' % str(int(date[8:10])) + \
          'c=%s&' % str(int(date[0:4])) + \
          'ignore=.csv'
    data="None"
    #print(url)
    try:
        days = urllib.request.urlopen(url).readlines()
        #print(days)
        # Sun Oct  6 12:04:04 EDT 2013: I think something changed as this was working before without the decoding (the data is a byte string now and not a string) 
        days[0]=days[0].decode('ascii')
        days[1]=days[1].decode('ascii')
        data = [day[:-2].split(',') for day in days]
    except urllib.error.HTTPError as err:
        #print(err)
        import traceback
        #errorLog.append(err)
    except urllib.error.URLError as err:
        #print(err)
        import traceback
        #errorLog.append(err)
    except Exception as err:
        #print(err)
        import traceback
        #errorLog.append(err)
    else:
        #raise
        import traceback
    return data

'''
I believe this is effectively the same as the above getHistoricalStockData,
but getHistoricalStockData handles errors better.
'''
def get_historical_prices(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
#the date goes month(jan=0) day year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date[5:7]) - 1) + \
          'e=%s&' % str(int(date[8:10])) + \
          'f=%s&' % str(int(date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(date[5:7]) - 1) + \
          'b=%s&' % str(int(date[8:10])) + \
          'c=%s&' % str(int(date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data
#end def get_historical_prices

'''
I believe this function shouldnt' be used as I came to the 
realization that the lists came out the day before the list date
(due to the pdf beign available the night before) such that we don't have to 
add another day to match the IBD performance.
'''
def get_historical_prices_plus_one_day(symbol, date):
    """
    Get historical prices for the given ticker symbol.
    Returns a nested list.
    """
#the date goes month(jan=0) day year
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(date[5:7]) - 1) + \
          'e=%s&' % str(int(date[8:10]) + 1) + \
          'f=%s&' % str(int(date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(date[5:7]) - 1) + \
          'b=%s&' % str(int(date[8:10]) + 1) + \
          'c=%s&' % str(int(date[0:4])) + \
          'ignore=.csv'
#    print url
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data
#end def get_historical_prices_plus_one_day

