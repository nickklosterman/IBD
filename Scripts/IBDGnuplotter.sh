#table="IBD50"
#ticker="CPRT"
database="IBDdatabase.sqlite.12072014"
date=`date +%Y-%m-%d`

#these are the limits we will perform our sql query inside; there may be no data returned for these limits. If there is data returned, mindate & maxdate will hold the dates for the first and last datapoint inside the query limits
querymindate="2013-07-13"
querymaxdate="2014-12-31"


#for mytable in "BC20" #"IBD50" "BC20" "Top200Composite" "IBD8585"
for mytable in "IBD50" "BC20" "Top200Composite" "IBD8585"
do
    table=$mytable
    case "$table" in
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

 #   echo "Max y range: $maxyrange"

    tickerlist=$(sqlite3 $database  "SELECT distinct(stockticker) FROM ${table}")
    for ticker in $tickerlist
    do 

	mindate=$(sqlite3 "$database" 'SELECT min('"$table"'_'"$ticker"'_Master.Date) FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" )' )
mindatelength=${#mindate}

if [[ $mindatelength -eq 10 ]]
then 
	maxdate=`sqlite3 "$database" 'SELECT max('"$table"'_'"$ticker"'_Master.Date) FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" )' `

	echo -e $ticker
#	echo $mindate
#	echo $maxdate
	tickerOpen=$(sqlite3 "$database" 'SELECT '"$table"'_'"$ticker"'_Master.Open FROM '"$table"'_'"$ticker"'_Master  WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.date ASC LIMIT 1' )
#	echo $tickerOpen
	sp500Open=$(sqlite3 "$database" 'SELECT  _GSPC.Open as SP500Open  FROM '"$table"'_'"$ticker"'_Master INNER JOIN _GSPC ON '"$table"'_'"$ticker"'_Master.Date =  _GSPC.Date WHERE '"$table"'_'"$ticker"'_Master.date >= (select min('"$table"'_'"$ticker"'_Master.date) from '"$table"'_'"$ticker"'_Master where '"$table"'_'"$ticker"'_Master.rank > 0 and '"$table"'_'"$ticker"'_Master.date >="'"$querymindate"'" and '"$table"'_'"$ticker"'_Master.date < "'"$querymaxdate"'" ) ORDER BY '"$table"'_'"$ticker"'_Master.Date ASC LIMIT 1' )
#	echo $sp500Open

	gnuplot <<EOF
set ylabel "% Change"
set logscale y
set yrange [0.8:2.6]
set ytics nomirror

set y2range [1:$maxyrange]
set y2tics
set y2label "$table Rank"

set xtics rotate 
set xlabel "Date"
set xdata time 
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set xtics nomirror
set xrange ["$mindate":"$maxdate"] 
#set the xtics to be one week (604800 seconds) apart for major tics
set xtics "$mindate",604800,"$maxdate"

set title "$table $ticker"

set datafile separator "|"

#choose the svg terminal
set terminal svg size 1200,900 font "Bitstream Vera Sans, 12" linewidth 1
#pipe the output to a file
set output "${table}_${ticker}_$date.svg" #replace with filename of format TABLE_TICKER_DATE.svg


#use WITH the set xdata....set xtics
plot "< sqlite3 $database 'SELECT ${table}_${ticker}_Master.Date, ${table}_${ticker}_Master.Open, ${table}_${ticker}_Master.Rank, ${table}_${ticker}_Master.High, ${table}_${ticker}_Master.Low, ${table}_${ticker}_Master.Close, ${table}_${ticker}_Master.Volume, ${table}_${ticker}_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM ${table}_${ticker}_Master INNER JOIN _GSPC ON ${table}_${ticker}_Master.Date =  _GSPC.Date WHERE ${table}_${ticker}_Master.date >= (select min(${table}_${ticker}_Master.date) from ${table}_${ticker}_Master where ${table}_${ticker}_Master.rank > 0 and ${table}_${ticker}_Master.date >=\"${querymindate}\" and ${table}_${ticker}_Master.date < \"${querymaxdate}\" ) ORDER BY ${table}_${ticker}_Master.Date ASC ' " using 1:(\$2/${tickerOpen}):1 with linespoints title "${ticker}" , \
"" using 1:(\$9/$sp500Open):1 with linespoints title "SP 500", \
"" using 1:(\$3):1 axes x1y2 with points  title "${ticker} Rank" 

EOF

fi 
    done



done


# # use WITHOUT the set xdata....set xtics 
# plot "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($2/31.8):xtic(1) with linespoints title "CPRT" , \
# "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($9/1472.33):xtic(1) with linespoints title "SP 500", \
# "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($3):xtic(1) axes x1y2 with points  title "CPRT Rank" 

# #use WITH the set xdata....set xtics
# # plot "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($2/31.8):1 with linespoints title "CPRT" , \
# # "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($9/1472.33):1 with linespoints title "SP 500", \
# # "< sqlite3 IBDdatabase.sqlite.12072014 'SELECT IBD50_CPRT_Master.Date, IBD50_CPRT_Master.Open, IBD50_CPRT_Master.Rank, IBD50_CPRT_Master.High, IBD50_CPRT_Master.Low, IBD50_CPRT_Master.Close, IBD50_CPRT_Master.Volume, IBD50_CPRT_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM IBD50_CPRT_Master INNER JOIN _GSPC ON IBD50_CPRT_Master.Date =  _GSPC.Date WHERE IBD50_CPRT_Master.date >= (select min(IBD50_CPRT_Master.date) from IBD50_CPRT_Master where IBD50_CPRT_Master.rank > 0 and IBD50_CPRT_Master.date >=\"2013-01-01\" and IBD50_CPRT_Master.date < \"2014-12-31\" ) ORDER BY IBD50_CPRT_Master.Date ASC '" using ($3):1 axes x1y2 with points  title "CPRT Rank" 



# # use WITHOUT the set xdata....set xtics 
# plot "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($2/31.8):xtic(1) with linespoints title "\$ticker" , \
# "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($9/1472.33):xtic(1) with linespoints title "SP 500", \
# "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($3):xtic(1) axes x1y2 with points  title "\$ticker Rank" 

# #use WITH the set xdata....set xtics
# # plot "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($2/31.8):1 with linespoints title "\$ticker" , \
# # "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($9/1472.33):1 with linespoints title "SP 500", \
# # "< sqlite3 \$database 'SELECT \$table_\$ticker_Master.Date, \$table_\$ticker_Master.Open, \$table_\$ticker_Master.Rank, \$table_\$ticker_Master.High, \$table_\$ticker_Master.Low, \$table_\$ticker_Master.Close, \$table_\$ticker_Master.Volume, \$table_\$ticker_Master.Adj_Close, _GSPC.Open as SP500Open, _GSPC.High as SP500High , _GSPC.Low as SP500Low , _GSPC.Close as SP500Close , _GSPC.Volume as SP500Volume , _GSPC.Adj_Close as SP500Adj_Close  FROM \$table_\$ticker_Master INNER JOIN _GSPC ON \$table_\$ticker_Master.Date =  _GSPC.Date WHERE \$table_\$ticker_Master.date >= (select min(\$table_\$ticker_Master.date) from \$table_\$ticker_Master where \$table_\$ticker_Master.rank > 0 and \$table_\$ticker_Master.date >=\$querymindate and \$table_\$ticker_Master.date < \$querymaxdate ) ORDER BY \$table_\$ticker_Master.Date ASC '" using ($3):1 axes x1y2 with points  title "\$ticker Rank" 




