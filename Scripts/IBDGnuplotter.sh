list="IBD50"
ticker="CPRT"
database="IBDdatabase.sqlite.12072014"
date=`date +%Y-%m-%d`
for mylist in "IBD50" "BC20" "Top200Composite" "IBD8585"
do
list=$mylist
case "$list" in
"IBD50")
maxyrange=50
;;
"BC20")
maxyrange=20
;;
"Top200Composite")
maxyrange=200
;;
"IBD8585")
maxyrange=175 #or use `$(sqlite3 "$database" 'select max(rank) from IBD8585')
;;
esac

echo "Max y range: $maxyrange"
done

#these are the limits we will perform our sql query inside; there may be no data returned for these limits. If there is data returned, mindate & maxdate will hold the dates for the first and last datapoint inside the query limits
querymindate=""
querymaxdate=""

mindate=`sqlite3 "$database" 'SELECT min(IBD50_CPRT_Master.Date) FROM IBD50_CPRT_Master  WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >="2013-01-01" and IBD50_CPRT_Master.date < "2014-12-31" )' `

mindate=$(sqlite3 "$database" 'SELECT min('"$list"'_'"$ticker"'_Master.Date) FROM '"$list"'_'"$ticker"'_Master  WHERE '"$list"'_'"$ticker"'_Master.date >= (select min('"$list"'_'"$ticker"'_Master.date) from '"$list"'_'"$ticker"'_Master where '"$list"'_'"$ticker"'_Master.rank > 0 and '"$list"'_'"$ticker"'_Master.date >="2013-01-01" and '"$list"'_'"$ticker"'_Master.date < "2014-12-31" )' )

maxdate=`sqlite3 "$database" 'SELECT max('"$list"'_'"$ticker"'_Master.Date) FROM '"$list"'_'"$ticker"'_Master  WHERE '"$list"'_'"$ticker"'_Master.date >= (select min('"$list"'_'"$ticker"'_Master.date) from '"$list"'_'"$ticker"'_Master where '"$list"'_'"$ticker"'_Master.rank > 0 and '"$list"'_'"$ticker"'_Master.date >="2013-01-01" and '"$list"'_'"$ticker"'_Master.date < "2014-12-31" )' `

echo $mindate
echo $maxdate

# gnuplot <<EOF
# set ylabel "% Change"
# set logscale y
# set yrange [0.9:2]
# set ytics nomirror

# set y2range [1:50]
# set y2tics
# set y2label "-List- Rank"

# set xtics rotate 
# set xlabel "Date"
# # set xdata time 
# # set timefmt "%Y-%m-%d"
# # set format x "%Y-%m-%d"
# # set xtics nomirror
# # set xrange ["2013-01-16":"2014-04-23"]  #would need to replace this with the min and max dates from the query
# # #set the xtics to be one week (604800 seconds) apart for major tics
# # set xtics "2013-01-16",604800,"2014-04-23" #would need to replace this with the min and max dates from the query

# set title "$list $ticker"

# set datafile separator "|"

# #choose the svg terminal
# set terminal svg  size 1200,900 font "Bitstream Vera Sans, 12" linewidth 1
# #pipe the output to a file
# set output "| cat >./plots/$list_$ticker_$date.svg" #replace with filename of format LIST_TICKER_DATE.svg


# # use WITHOUT the set xdata....set xtics 
# plot "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($2/31.8):xtic(1) with linespoints title "CPRT" , \
# "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($9/1472.33):xtic(1) with linespoints title "SP 500", \
# "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($3):xtic(1) axes x1y2 with points  title "CPRT Rank" 

# #use WITH the set xdata....set xtics
# # plot "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($2/31.8):1 with linespoints title "CPRT" , \
# # "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($9/1472.33):1 with linespoints title "SP 500", \
# # "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($3):1 axes x1y2 with points  title "CPRT Rank" 

# #pause -1 "Hit any key to continue."
# EOF
