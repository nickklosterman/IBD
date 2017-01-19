#/bin/bash

filePrefix=('Big Cap 20' 'CANSLIM Select' 'Global Leaders' 'IBD50' 'IPO Leaders' 'New High' 'Relative Strength At New High' 'Rising Profit Estimates' 'Sector Leaders' 'Stock Spotlight' 'Stocks That Funds Are Buying' 'Weekly Review')
IFS=$'\n'
for ((i = 0; i < ${#filePrefix[@]}; i++))
do
    echo "${filePrefix[$i]}---------------------------- ${item}"
    for file in `ls -r "${filePrefix[$i]}"_*`  # argg I was trying to get the sort order reversed for input into my data file. solution was adding in the IFS.. above to get this ls to work with filenames with spaces
		#for file in `ls -r "${filePrefix[$i]}"*`  #"${item}"*
    do
	node fileReader.js "${file}" >> "${filePrefix[$i]}.txt"
	#echo "${file}"
    done
done
