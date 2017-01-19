var http = require('http'),
    //cheerio = require('cheerio'),
    fs = require('fs'),
    //request = require('request'),
    cookie='',
    postIDUrl="http://www.investors.com/ajax/static/postID:";

function makeRequest(urlPiece){
    var options = {
	host: 'research.investors.com',
	path: '/Services/SiteAjaxService.asmx/'+urlPiece,
	headers: {
	    'content-type': 'application/json; charset=utf-8',
	    cookie:cookie
	}
    };

    callback = function(response) {
	var str = '';

	//another chunk of data has been received, so append it to `str`
	response.on('data', function (chunk) {
	    str += chunk;
	});

	//the whole response has been received, so we just print it out here
	response.on('end', function () {
	    //	console.log(str);
	    var resp = JSON.parse(str);
	    resp.d.ETablesDataList.forEach(function(ele, indx,arr) {
		console.log(ele.Rank+" "+ele.Symbol);
	    });
	});
    }

    http.request(options, callback).end();
}
function makeRequest2(obj){
    var options = {
	host: 'research.investors.com',
	path: '/Services/SiteAjaxService.asmx/'+obj.urlPiece,
	headers: {
	    'content-type': 'application/json; charset=utf-8',
	    cookie:cookie
	}
    };

    callback = function(response) {
	var str = '';

	//another chunk of data has been received, so append it to `str`
	response.on('data', function (chunk) {
	    str += chunk;
	});

	//the whole response has been received, so we just print it out here
	response.on('end', function () {
	    console.log(obj.site);
	    var resp = JSON.parse(str);
	    writeDataToFile(obj.site+'_'+dateForInsertion+'.txt',JSON.stringify(resp.d.ETablesDataList));
/*	    resp.d.ETablesDataList.forEach(function(ele, indx,arr) {
		console.log(ele.Rank+" "+ele.Symbol);
	    }); */
	    //console.log(JSON.stringify(resp.d.ETablesDataList));  //<-- this is the data that you'd write to the sql database
	});
    }

    http.request(options, callback).end();
}

function writeDataToFile(filename,data) {
    fs.writeFile(filename,data, (err) => {
  if (err) throw err;
  console.log('It\'s saved!:'+filename);
});

}

var sitesArr = [ 
    'GetIBD50?sortcolumn1="ibd100rank"&sortOrder1="asc"&sortcolumn2=""&sortOrder2="ASC"', //d.ETablesDataList
    'GetSectorLeaders?sortcolumn1="sectorrank"&sortOrder1="asc"&sortcolumn2="symbol"&sortOrder2="ASC"', //d.ETablesDataList
    'GetBigCap20?sortcolumn1="ibd100rank"&sortOrder1="asc"&sortcolumn2=""&sortOrder2="ASC"', //d.ETablesDataList
    'GetNewHigh?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="Symbol"&sortOrder2="ASC"', //d.ETablesDataList
    'GetIPOLeaders?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="Symbol"&sortOrder2="ASC"',//d.ETablesDataList
    'GetGlobalLeaders?sortcolumn1="rank"&sortOrder1="asc"&sortcolumn2="CompRating"&sortOrder2="ASC"',//d.ETablesDataList
    'GetWeeklyReview?sortcolumn1="indgrprank"&sortOrder1="asc"&sortcolumn2="symbol"&sortOrder2="ASC"'//d.ETablesDataList
],
    
    ibdDataTablesUrl={ url:"http://www.investors.com/ibd-data-tables/", host:"www.investors.com", path:"/ibd-data-tables"};


sitesArr = [ 
    {site:"IBD50",urlPiece:    'GetIBD50?sortcolumn1="ibd100rank"&sortOrder1="asc"&sortcolumn2=""&sortOrder2="ASC"'}, 
    {site:"Sector Leaders",urlPiece:    'GetSectorLeaders?sortcolumn1="sectorrank"&sortOrder1="asc"&sortcolumn2="symbol"&sortOrder2="ASC"'},
    {site:"Stock Spotlight",urlPiece:    'GetStockSpotlight?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="symbol"&sortOrder2="ASC"'},


    {site:"Big Cap 20",urlPiece:    'GetBigCap20?sortcolumn1="ibd100rank"&sortOrder1="asc"&sortcolumn2=""&sortOrder2="ASC"'}, 
    {site:"New High",urlPiece:    'GetNewHigh?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="Symbol"&sortOrder2="ASC"'},
    {site:"Relative Strength At New High",urlPiece:    'GetBoltingRSLines?sortcolumn1="rsrating"&sortOrder1="desc"&sortcolumn2="symbol"&sortOrder2="ASC"'},
    {site:"Stocks That Funds Are Buying",urlPiece:    'GetAccelMFOwnership?sortcolumn1="nofunds"&sortOrder1="desc"&sortcolumn2="symbol"&sortOrder2="ASC"'}, 


    {site:"Global Leaders",urlPiece:    'GetGlobalLeaders?sortcolumn1="rank"&sortOrder1="asc"&sortcolumn2="CompRating"&sortOrder2="ASC"'},   
    {site:"IPO Leaders",urlPiece:    'GetIPOLeaders?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="Symbol"&sortOrder2="ASC"'},
    {site:"Rising Profit Estimates",urlPiece:    'GetLeadersRisingEstimates?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="symbol"&sortOrder2="ASC"'},
    //teach leaders is just a list of articles

    //same with stocks near a buy zone
    {site:"Weekly Review",urlPiece:'GetWeeklyReview?sortcolumn1="indgrprank"&sortOrder1="asc"&sortcolumn2="symbol"&sortOrder2="ASC"'},
    {site:"CANSLIM Select",urlPiece:'GetCanslimSelect?sortcolumn1="comprating"&sortOrder1="desc"&sortcolumn2="symbol"&sortOrder2="ASC"'}

];


/*
function getIBDDataTableUrls() {
    request(ibdDataTablesUrl.url,function(error,response,html) {
	if (!error && response.statusCode == 200) {
	    var $ = cheerio.load(html);
	    $('.box-link').each(function(i,e){
		//	    console.log(e.attribs.href);
		getPostID(e.attribs.href);
	    });
	}
    });
}


function getPostID(url) {
    request(url,function(error,response,html) {
	if (!error && response.statusCode == 200) {
	    var $ = cheerio.load(html);
	    console.log(url +" -=- "+ ($("link[rel='shortlink']")[0]).attribs.href.split("p=")[1] );
	    //	    getPost($("link[rel='shortlink']")[0]).attribs.href.split("p=")[1] ); //need to pass in some stuff to set the offset for the correct data to be grabbed from the lists
	}
    });
}

function getPost(id) {
    request(postIDUrl+id,function(error,response,html) {
	if (!error && response.statusCode == 200) {
	    var $ = cheerio.load(html);
	    $('TABLE TR TD').each(function(index,element){
		//		if (index > 17 && (index-7) % 10 === 0 ) { //algo for top-200-composite
		//		if (index > 5 && (index -8 ) %5 ===0 ) { //algo for smallmid-cap-leaders ; largemid-cap-leadres
		if (index > 6 && (index -6 ) %5 ===0 ) { //algo for utilities, reit-leaders
		    console.log(index+": "+element.children[0].data);
		}
	    });
	} else { console.log(error);}
    });
}
*/

function main(cookie) {
    sitesArr.forEach(function(ele,idx,arr) {
	//	makeRequest(ele);
		makeRequest2(ele);	
    });

    //      getIBDDataTableUrls();
    
    //still working on this bit of getting the post
    //    getPost(294373); //top-200-composite
    //    getPost(294350);
    
    /*
      http://www.investors.com/data-tables/company-earnings-reports-august-9-2016/ -=- 294462
      http://www.investors.com/data-tables/ipos-august-10-2016/ -=- 295498
      http://www.investors.com/data-tables/psychological-indicators-volume-august-9-2016/ -=- 294486
      http://www.investors.com/data-tables/expanded-52-week-highs-and-lows-august-10-2016/ -=- 295606
      http://www.investors.com/data-tables/ibd-smart-nyse-nasdaq-tables-august-10-2016/ -=- 295611
      http://www.investors.com/data-tables/dividends-august-10-2016/ -=- 295502
      http://www.investors.com/data-tables/expanded-mutual-fund-tables-august-9-2016/ -=- 294890
      http://www.investors.com/data-tables/mutual-fund-charts-august-9-2016/ -=- 294521
      http://www.investors.com/data-tables/top-sector-etfs-august-10-2016/ -=- 295540
      http://www.investors.com/data-tables/ibd-smallmid-cap-leaders-index-august-10-2016/ -=- 295677
      http://www.investors.com/data-tables/top-200-composite-stocks-august-10-2016/ -=- 295623
      http://www.investors.com/data-tables/industry-sub-group-rankings-august-9-2016/ -=- 294451
      http://www.investors.com/data-tables/bottom-200-composite-stocks-august-10-2016/ -=- 295585
      http://www.investors.com/data-tables/ibd-tech-leaders-august-10-2016/ -=- 295682
      http://www.investors.com/data-tables/reit-leaders-august-10-2016/ -=- 295515
      http://www.investors.com/data-tables/dividend-leaders-august-10-2016/ -=- 295508
      http://www.investors.com/data-tables/sector-rotation-etfs-august-9-2016/ -=- 294447
      http://www.investors.com/data-tables/futures-tables-august-10-2016/ -=- 295663
      http://www.investors.com/data-tables/timesaver-table-august-10-2016/ -=- 295619
      http://www.investors.com/data-tables/options-august-9-2016/ -=- 294516
      http://www.investors.com/data-tables/top-fidelity-sector-funds-august-9-2016/ -=- 294499
      http://www.investors.com/data-tables/etf-tables-august-10-2016/ -=- 295524
      http://www.investors.com/data-tables/stocks-out-of-bases-august-10-2016/ -=- 295555
      http://www.investors.com/data-tables/futures-charts-august-9-2016/ -=- 294481
      http://www.investors.com/data-tables/etf-winners-august-10-2016/ -=- 295536
      http://www.investors.com/data-tables/groups-with-highest-of-stocks-at-new-high-august-10-2016/ -=- 295544
      http://www.investors.com/data-tables/reits-august-10-2016/ -=- 295615
      http://www.investors.com/data-tables/spot-prices-august-10-2016/ -=- 295550
      http://www.investors.com/data-tables/etf-losers-august-10-2016/ -=- 295531
      http://www.investors.com/data-tables/interest-rates-august-9-2016/ -=- 294474
      http://www.investors.com/data-tables/find-your-groups-sector/ -=- 220397
      http://www.investors.com/data-tables/new-high-list-august-10-2016/ -=- 295601
      http://www.investors.com/data-tables/utility-leaders-august-10-2016/ -=- 295519
      http://www.investors.com/data-tables/top-ranked-low-priced-stocks-august-10-2016/ -=- 295627
      http://www.investors.com/data-tables/nyse-nasdaq-most-active-and-most-up-august-10-2016/ -=- 295593
      http://www.investors.com/data-tables/ibd-largemid-cap-leaders-index-august-10-2016/ -=- 295669
      http://www.investors.com/data-tables/preferred-stocks-august-9-2016/ -=- 294490
    */
}

if (process.argv[2]) {
    cookie = process.argv[2];
} else {
    console.log("no cookie provided");
}

main(cookie)
var now=new Date();
console.log(now);
var dateForInsertion = now.getUTCFullYear()+"-"+(now.getUTCMonth()+1)+"-"+now.getUTCDate();
dateForInsertion = now.getFullYear()+"-"+(getDateTwoDigitFormat(now.getMonth()+1))+"-"+getDateTwoDigitFormat(now.getDate());
console.log(dateForInsertion);

function getDateTwoDigitFormat(m) {
    return m<10?"0"+m:m;
}

/*TODO:
  know which list to write the data to,
  disallow writing if there is no cookie as this won't write a full list.
*/
