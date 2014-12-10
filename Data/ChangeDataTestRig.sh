#!/bin/bash
#http://www.linuxjournal.com/content/bash-arrays
filelist=( 'IBD50.txt' 'Top200Composite.txt' 'BC20.txt' '8585.txt' )

function createBackup() {
    for index in 0 1 2 3 
    do
	if [ ! -e "${filelist[index]}.backup" ]
	then
	    cp "${filelist[index]}" "${filelist[index]}.backup"
	else
	    echo "${filelist[index]}.backup exists, not overwriting."
	fi
	
    done
}

function createAndUseShortFiles() {
for i in "${filelist[@]}"
do
    #grab the topmost 2 lines; this should work to get the latest entry when using my extraction and insertion runner; Multiples of 3 lines should work when using the extraction and insertion runner to get X number of days worth of datapoints.
head -n 3 "${i}.backup" > "${i}" 
done
    
    }

function restoreBackup() {
    for i in "${filelist[@]}" #index in 1 2 3 4 
    do
	echo "$i" #"${filelist[i]}"
	if [ -e "${i}.backup" ]
	then
	    cp "${i}.backup" "${i}"
	else
	    echo "No ${i}.backup exists"
	fi
    done
}


function usage() {
    echo "${0} \"UseShortFile\" or \"RestoreBackup\""
}

##Main
NumberOfExpectedArguments=1
#echo "$#"
if [ $# -eq $NumberOfExpectedArguments ]
then
    Mode=${1}
    echo "Mode ${1}"
else
    usage
    exit
fi

#ensure there are backups
createBackup

if [ ${Mode} == "UseShortFile" ]
then
    createAndUseShortFiles
fi

if [ ${Mode} == "RestoreBackup" ]
then
    restoreBackup
fi
