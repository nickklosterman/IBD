#!/bin/bash
item=$1
echo "<html><body>" > ${item}.html
ls ${item}*.svg | sed 's/^/<img src="/;s/$/">/' >> ${item}.html
echo "</body></html>" >> ${item}.html
