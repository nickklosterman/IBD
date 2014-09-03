#!/bin/bash
if [[ $# -eq 1 ]]
then 
date=`date +%F`
path=${1}
bash IBDPDFExtractor.sh ${path} | sort > /tmp/${date}_IBDDataSorted.txt #turning on any add'l echo statements will most likely break the EnterIBDDataFromFile script as the format will change
python3 EnterIBDDataFromFile.py3 /tmp/${date}_IBDDataSorted.txt
else
    
echo "Usage: ${0} path/to/files/"
fi
