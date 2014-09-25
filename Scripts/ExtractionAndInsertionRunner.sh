#!/bin/bash
if [[ $# -eq 1 ]]
then 
    date=`date +%F`
    path=${1}
    bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
    python3 EnterIBDDataFromFile.py3 --inputfile=/tmp/${date}_IBDDataSorted.txt
elif [[ $# -eq 2 ]]
then 
    if [[ ${2} == "test" ]] 
    then 
	echo "Testing length of data to be entered."
	echo "To write the results, run the script without the 'test' option."
	date=`date +%F`
	path=${1}
	bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
	python3 EnterIBDDataFromFile.py3 --inputfile=/tmp/${date}_IBDDataSorted.txt --test
    else
	echo "Usage: ${0} path/to/files/ test #this will test for length correctness but not write out the data"
    fi
else
    
    echo "Usage: ${0} path/to/files/ test #this will test for length correctness but not write out the data"
    echo "Usage: ${0} path/to/files/"
fi
