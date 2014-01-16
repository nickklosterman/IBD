#!/bin/bash
function instructions()
{
echo "
This script creates a .txt file for 
each IBDYYYYMMDD.pdf file creating
a IBDYYYYMMDD.pdf.txt file and then
opening all IBD.txt files in emacs"
}
for item in IBD201*.pdf
do 
    touch $item.txt
done
acroread IBD201*.pdf  &
emacs IBD201*.txt
