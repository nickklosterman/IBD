#!/bin/bash

# #These are extractors for pdf IBD
# #you need to copy the relevant list out of the pdf and stick it in a file. 
# #for IBD50 and BC20 you need to copy the large blocks with the graph as the ticker isn't included in the small sidebar list
# #for top200 just grab the whole table
# #for 8585 grab the small sidebar table and not the large blocks w the graph as the last page always has more in the sidebar than the large blocks

# #IBD50/BC20
# better to grep off Grp to prevent false positives
# grep Grp ibd5020131209.txt |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," | tr '\n' ' '
# grep Group ibd5020131209.txt |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," | tr '\n' ' '
# ####grep \( ibd5020131209.txt |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," | tr '\n' ' '

# #Top 200 Composite
# #i couldn't figure out how to do this with sed.
# #this still produces some extraneous output. I still need to clean it up 
# awk '{ print $(NF-3) }' ibd5020131129_top200.txt
# awk '{ print $(NF-3) }' ibd5020131129_top200.txt  | sed 's/[[:lower:]]/ /g;s/^ *.//g' #not fully working to get rid of extra upper and lower case chars. 
# #this one works. although I feel like there is a more elegant solution out there.
# awk '{ print $(NF-3) }' ibd5020131129_top200.txt  | sed 's/[[:lower:]]/ /g;s/^ +*.//g' | awk '{ print $NF }' | tr '\n' ' '

# #for 8585
# sed -n -e 's/^\([^<]*\) [1-9][1-9] [ABCDE] .*/\1/p' ibd5020131206.8585.txt | awk '{ print $(NF) }' | tr '\n' ' '
# #the above is basically cutting off everything after the p/e and accumulation grade. this then gives us a clean est of space delimited fields to use awk on



inputfilename=${1}

#BC20 and IBD50, could be used for 8585 but not all in the 8585 get boxes
extract-from-detail-boxes() {
    grep Group ${1} |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," | tr '\n' ' '
    grep Grp ${1} |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," | tr '\n' ' '
}

extract-from-top200(){
    awk '{ print $(NF-3) }' ${1}  | sed 's/[[:lower:]]/ /g;s/^ +*.//g' | awk '{ print $NF }' | tr '\n' ' '
}

extract-from-8585(){
    sed -n -e 's/^\([^<]*\) [1-9][1-9] [ABCDE] .*/\1/p' ${1} | awk '{ print $(NF) }' | tr '\n' ' '
}


#assumes input of IBD20130819*
get-date-from-filename() {
input=${1}
year=${input:3:4}
month=${input:7:2}
day=${input:9:2}
echo "$year-$month-$day"
}

#test
#get-date-from-filename "IBD20131523"

for item in IBD201*.pdf.txt
#until [ -z "$1" ]
do    	
    echo "Processing '$item'"
    myfile=$(basename ${item} )
    
    results=$( extract-from-detail-boxes ${item} )  # there has got to be a better way to do this calling an array of function if no results found
    #guessing on the length of the result as to which list this came from
    if [[ ${#results} -lt 100 ]]
    then 
	outputType="BC20"
    else
	outputType="IBD50"
    fi
    
    if [[ ${#results} -lt 20 ]]
    then 
	results=$( extract-from-8585 ${item} )
	outputType="8585"
	if [[ ${#results} -lt 300 ]]
	then 
	    results=$( extract-from-top200 ${item} )
    outputType="Top200"
	fi
    fi
    echo "${outputType}"
    get-date-from-filename ${myfile}
    echo "${results}"
    shift
done
echo "based on the output type we could insert the desired data into the appropriate file instead of simply printing it out. That would save a cut/past step. We could easily just have a test run flag and then a insert flag."
