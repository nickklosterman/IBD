#!/bin/bash
for item in "BC20" "IBD50" "IBD8585" "Top200Composite"
do
    echo "$item"
    bash makeSVGpage.sh ${item}
done
