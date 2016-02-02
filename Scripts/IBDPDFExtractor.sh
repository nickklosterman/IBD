#!/bin/bash
function instructions()
{
echo "
This script is to be used to extract the IBD list data from
table data copied directly from the IBD pdfs into a text file.
It is meant to be run in a directory of text files whose names
match that of the IBD PDF file with a .txt extension tacked on.
This allows the script to extract the date.
Output is the determined list the data came from followed by 
the date followed by a list of stocks in appropriate 
order on the following line.
The IBD50 and BC20 lists must be copied from the blocks with 
their charts. The ranks can be muddled as the script will
reorder for proper ingestion by DualPrepForDatabase.py3
The Weekly Review 85 85 list must be copied from the sidebar
and the order should be kept. All stocks are not provided with
block and chart in the main page so we can't use that.
The Top200Composite stocks should be copied with all column 
data.
"
}
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
# #the above is basically cutting off everything after the p/e and accumulation grade. this then gives us a clean set of space delimited fields to use awk on
# sed -n -e 's/^\([^<]*\) [0-9]\{1,3\} [ABCDE] [0-9]\{1,2\} .*/\1/p' ${1} | awk '{ print $(NF) }' | tr '\n' ' '
# I believe the above uses a hold space and what is matched is actually discarded for sed. then we print the last field with awk. The sed is checking for some type of start that is not ?? then it matches the number and grade letter and another est of numbers to find the hold space. 

inputfilename=${1}

#BC20 and IBD50, could be used for 8585 but not all in the 8585 get boxes
extract-from-detail-boxes() {
    #I believe this works as it will always be 'Group' or 'Grp' to key off of, depending which case it is
    grep Group ${1} |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," #| tr '\n' ' '
    grep Grp   ${1} |  sed 's/^\([0-9]*\)/\1,/;s/(/,/;s/)/,/'  | sort -n | cut -f 3 -d"," #| tr '\n' ' '
}

extract-from-top200(){
#print the third from last (NF = number of fields) field; replace all lower case charactesr with spaces; ??replace all leading spaces with nothing???; print the NF field (which at this point should be the only entry; convert newline to space 
#the lowercasing is used to separate out when the company name runs into the ticker symbol. It produces a separate field. we then grab the ticker field with that final `{print $NF}`
    awk '{ print $(NF-3) }' ${1}  | sed 's/[[:lower:]]/ /g;s/^ +*.//g' | awk '{ print $NF }' #| tr '\n' ' '
}

extract-from-8585(){
    #from IBD20141017.pdf.txt : "Keurig Green MountGMCR 35 C 96 98 –8 137.98 –2.18 Profunds Ultra Nas A+ 0.5 –"
    #I need to somehow extract or invite manual intervention when there company name intrudes into the ticker and they are both matched
    sed -n -e 's/^\([^<]*\) [0-9]\{1,3\} [ABCDE] [0-9]\{1,2\} .*/\1/p' ${1} | awk '{ print $(NF) }' | tr '\n' ' ' #fuck I had [1-9][1-9] and this was excluding anything with a zero in the P/E column. And anything w single digit P/E, added additional trailing [0-9]\{1,2\} as `AgreeRealty ADC 16 C 93 87 –19 33.73 –0.26 Mass Mutual Rus 20 A 0.0 +` from 2016-01-08 was failing bc the previous check was capturing to the '.....Mass Mutual Rus 20...' which was then reporting the ticker as Rus instead of ADC.
    #sed -n -e 's/^\([^<]*\) [1-9][0-9][0-9] [ABCDE] .*/\1/p' ${1} | awk '{ print $(NF) }' | tr '\n' ' '
}


#assumes input of IBD20130819*
get-date-from-filename() {
input=${1}
year=${input:3:4}
month=${input:7:2}
day=${input:9:2}
echo "$year-$month-$day"
}


######################
#####   M A I N  #####
######################

#instructions
#echo ${1}
for item in ${1}IBD201*.pdf.txt
do    	
    #echo "Processing '$item'"
    myfile=$(basename ${item} )

    saveIFS=$IFS
    results=$( extract-from-detail-boxes ${item} )  
    IFS=$'\n'
    resultsArr=($results)
    IFS=$saveIFS
    outputType="Unknown"

    #This is super fragile as I don't know how to handle when the results are less than expected
    if [[ ${#resultsArr[@]} -eq 20 ]] #there have been times in the past when there weren't 20 for BC20; 
    then 
	outputType="BC20"
    fi
    if [[ ${#resultsArr[@]} -eq 50 ]]
    then
	outputType="IBD50"
    fi

    if [[ ${#resultsArr[@]} -lt 20 ]] 
    then
        #Wed Jun 24 12:24:48 EDT 2015 tweak calculation bc IBD20150618 was Top200 but being treated as 8585 which was wrong. I believe the probability of the 8585 being 200 records and therefore being mistaken as a top200 is quite low. hmm this might be a Mac(old bash) vs Linux (new bash) I think this is reporting number of characters instead of number of elements in array.
	    results=$( extract-from-top200 ${item} )
	    saveIFS=$IFS
	    IFS=$'\n'
	    resultsArr=($results)
	    IFS=$saveIFS
	    outputType="Top200"
#echo "${#results} ${#results[@]} ${results} $myfile $outputType"
            if [[ ${#resultsArr[@]} -ne 200 ]]
               then 
	    results=$( extract-from-8585 ${item} )
	    saveIFS=$IFS
	    IFS=$'\n'
	    resultsArr=($results)
	    IFS=$saveIFS
	    outputType="8585"
            fi
    fi
    #switch to the output on one line so we can sort easily by type for easier import to the final data files
    echo "${outputType},$( get-date-from-filename ${myfile} ),${resultsArr[@]}"
    shift
done

#for the string to array method http://stackoverflow.com/questions/24628076/bash-convert-n-delimited-strings-into-array?rq=1
