for item in IBD*.pdf
do 
    touch $item.txt
done
emacs IBD*.txt
