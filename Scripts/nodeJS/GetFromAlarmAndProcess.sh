#!/bin/bash

scp alarm@192.168.1.102:/home/alarm/*20[12][7890]*-*-*.txt .
bash DumpContentsForListDataFiles.sh

filePrefix=('Big Cap 20' 'CANSLIM Select' 'Global Leaders' 'IBD50' 'IPO Leaders' 'New High' 'Relative Strength At New High' 'Rising Profit Estimates' 'Sector Leaders' 'Stock Spotlight' 'Stocks That Funds Are Buying' 'Weekly Review')
IFS=$'\n'
for ((i = 0; i < ${#filePrefix[@]}; i++))
do
    echo "${filePrefix[$i]}----------------"
    #    cat  ${filePrefix[$i]} ../../Data/${filePrefix[$i]} > /tmp/${filePrefix[$i]}
    #cat  ${filePrefix[$i]}.txt ../../Data/"${filePrefix[$i]}".txt >> tmp${filePrefix[$i]}
    
    #    mv /tmp//${filePrefix[$i]} ../../Data/${filePrefix[$i]}
done

#bash ../../MasterScript2.sh
