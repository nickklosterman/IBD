#!/bin/bash
date=`date +%F`
tar czvf IBD_${date}_Data.tgz Big\ Cap\ 20*.txt CANSLIM\ Select*.txt Global\ Leaders*.txt  IBD50*.txt IPO\ Leaders*.txt New\ High*.txt Relative\ Strength\ At\ New\ High*.txt Rising\ Profit\ Estimates*.txt Sector\ Leaders*.txt Stock\ Spotlight*.txt Stocks\ That\ Funds\ Are\ Buying*.txt Weekly\ Review*.txt
