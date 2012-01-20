#!/bin/bash

filename=$1
filename="/home/arch-nicky/IBD50.txt"
counter=0
while read Line
do 
    Date="Nothing"
    StocksArray=" 1 2 3 "
    let "countermod = $counter % 3"
    case  "$countermod" in
	"0" ) Date="$Line";;
	"1" ) TempLine="$Line"
	    StocksArray=$( echo "$TempLine" | tr ',' ' ' )
	    read -a StocksArray2 <<<$StocksArray #this turns the space separated variable into an array of the variables
	    echo $Date ${StocksArray2[0]} #0 indexed array
	    echo ${#StocksArray2[*]} # ${StocksArray[@]}
	    ;;
	"2" ) echo "Blank Line" ;;

    esac
#echo $Line
#echo $counter $countermod
    let "counter += 1"
done < $filename

#to split the variable into an array I used this: http://stackoverflow.com/questions/1617771/splitting-string-into-array