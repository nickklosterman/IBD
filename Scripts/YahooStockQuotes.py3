#!/usr/bin/env/python
# -*- python -*- 
import sys #for cmd line arguments
import urllib.request, urllib.parse, urllib.error #for getting quotes from net
#




"""


THIS WILL NOT WORK AS A MODULE AS http://docs.python.org/3/tutorial/modules.html#importing-from-a-package 
STATES THAT THE FILE MUST END IN .PY NOT .PY3



"""


# to use:
# from YahooStockQuotes import getHistoricalStockPrices 
def getHistoricalStockPrices(symbol, date):
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
    try:
            days = urllib.request.urlopen(url).readlines()
            data = [day[:-2].split(',') for day in days]
    except urllib.error.HTTPError as err:
        if err.code == 404: #try incrementing date again
            import traceback
            errorLog.append(err)
                #days = urllib.request.urlopen('http://www.djinnius.com').readlines() #get some byte data that will fail and throw an error. This is awful that I'm relying on an outside source to help set an error. I should hand define the error (I tried using buffer() and memoryview() since using str(,encoding) expects a vuffer,bytearray or byte object but no dice. I also could try to move the 
    except urllib.error.URLError as err:
        import traceback
        errorLog.append(err)
    except Exception as err:
        import traceback
        errorLog.append(err)
    else:
        #raise
        import traceback
    return data

#end def get_historical_prices



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
    days = urllib.request.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]

    return data
#end def get_historical_prices_plus_one_day

