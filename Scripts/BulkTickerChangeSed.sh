#!/bin/bash

#this program is meant to take as input a file which holds pairs of sed entries to be executed on the tickers in the IBD/Data directory
#a line of the input file should read as such :
# AAPLE/AAPL

while read LINE
do 
    Line=${LINE%?}
    seddelimiter="/"
    seddelimiterflag=0
    case $Line in 
	*"$seddelimiter"*) seddelimiterflag=1;;
    esac
    if [ $seddelimiterflag == 1 ]
    then 

    echo "find . -type f -print | xargs sed -i 's/${Line}/g'"
    exec find . -type f -print | xargs sed -i "s/${Line}/g"
    else
	echo "skipping execution of this line: find . -type f -print | xargs sed -i 's/${Line}/g'  as it doesn't have the sed delimiter in it"
    fi
    
done < $1