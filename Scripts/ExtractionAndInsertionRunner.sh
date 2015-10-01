#!/bin/bash
if [[ $# -eq 2 ]]
then
    if [[ ${2} == "write" ]]
           then 
    date=`date +%F`
    path=${1}
    bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
    python3 EnterIBDDataFromFile.py3 --inputfile=/tmp/${date}_IBDDataSorted.txt
    else
        echo "The first command will test if the data passes the checks and is clean and ready to be entered."
        echo "Usage: ${0} path/to/files/"
        echo "Usage: ${0} path/to/files/ write"
        fi
    
elif [[ $# -eq 1 ]]
then 
	echo "Testing length of data to be entered."
	echo "To write the results, run the script without the 'write' option."
        echo "E.g. ${0} ${1} write"
	date=`date +%F`
    if [[ ${1} == "write" ]]
    then
	path="$HOME/Downloads/"
	else 
	    path=${1}
	    fi
	bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
	python3 EnterIBDDataFromFile.py3 --inputfile=/tmp/${date}_IBDDataSorted.txt --test
elif [[ $# -eq 0 ]]  #default to checking the $HOME/Downloads directory 
then 
	echo "Testing length of data to be entered."
	echo "To write the results, run the script without the 'write' option."
        echo "E.g. ${0} ${1} write"
	date=`date +%F`
	path="$HOME/Downloads/"
	bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
	python3 EnterIBDDataFromFile.py3 --inputfile=/tmp/${date}_IBDDataSorted.txt --test

else
    
    echo "Usage: ${0} path/to/files/ test #this will test for length correctness but not write out the data"
    echo "Usage: ${0} path/to/files/"
fi
