#!/bin/bash

echo 
"This program is meant to take as input a file 
which holds pairs of sed entries to be executed 
on the tickers in the IBD/Data directory
a line of the input file should read as such :
AAPLE/AAPL
"
if [ $# -lt 1 ]
then 
    echo 
    "Please enter a filename for execution.
The contents should be of the form
oldticker/newticker
"
else 
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
fi
