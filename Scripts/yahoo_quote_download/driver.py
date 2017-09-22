# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:58:59 2017

@author: c0redumb
"""

from yqd import load_yahoo_quote

import sys

def load_quote(ticker):
    #print('===', ticker, '===')
    load_yahoo_quote(ticker, '20150515', '20170517') #don't need the print since we are printing in load_yahoo_quote
    #print(load_yahoo_quote(ticker, '20170515', '20170517', 'dividend'))
    #print(load_yahoo_quote(ticker, '20170515', '20170517', 'split'))
    
def test(ticker):
    # Download quote for stocks
    load_quote(ticker)
    #load_quote('V')
    
    # Download quote for index
    #load_quote('^DJI')

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        print(sys.argv[1])
    test(sys.argv[1])
        
