var fs = require('fs');

function readFile(filename) {
    return new Promise(function(resolve,reject) {
	fs.readFile(filename,'utf8',function(err,data){
	    if (err) {
		reject(err);
	    } else {
		resolve(data);
	    }
	});
    });
}

//outputs 'Rank Symbol' or 'Symbol'
function extractData(data) {
    var jsonData = JSON.parse(data);
    jsonData.forEach(function(ele,idx,arr){
	if (ele.Rank) {
	    console.log(ele.Rank+" "+ele.Symbol);
	} else {
	    console.log(ele.Symbol);
	}
    });
}

//outputs '[Key] Symbol' or 'Symbol'
function extractData2(data,key) {
    var jsonData = JSON.parse(data);
    jsonData.forEach(function(ele,idx,arr){
	if (ele[key]) {
	    console.log(ele[key]+" "+ele.Symbol);
	} else {
	    console.log(ele.Symbol);
	}
    });
}

//outputs space delimited list of Symbols
function extractData3(data,key) {
    var jsonData = JSON.parse(data),
	output="",
	len =jsonData.length;
    //have to use for loop instead of forEach otherwise would need a callback...
    for (var i=0; i<len; i++) {
	output+=jsonData[i].Symbol+" ";
    }
    console.log(output);
}

function getDateFromFilename(filename) {
    var re=/^.*_/,
	front;
    filename=filename.substring(0,filename.length-4);
    front=filename.match(re);
    filenameSplit=(filename.substring(front[0].length,filename.length)).split("-");
//this should be unnecessary now that i've modified app.js to output the date in YYYY-MM-DD format
    if (filenameSplit[1].length===1){
	filenameSplit[1]="0"+filenameSplit[1];
    }
    if (filenameSplit[2].length===1){
	filenameSplit[2]="0"+filenameSplit[2];
    }
    
    //console.log(filenameSplit);

    return filenameSplit[0]+'-'+filenameSplit[1]+'-'+filenameSplit[2];
}
if (process.argv.length <= 2) {
    console.log("Usage: " + __filename + " Big Cap 20_2017_1_3.txt {json key: PerOffHigh CompanyName}");
    console.log("node app.js filename");
    process.exit(-1);
}

var cliArgs = process.argv.slice(2);

/*console.log(cliArgs);
console.log(process.argv);
console.log(cliArgs[1]);
/**/
readFile(cliArgs[0]).then(function(data) {
    console.log(getDateFromFilename(cliArgs[0]));
    if (cliArgs.length === 2) {
	extractData2(data,cliArgs[1]);
    } else {
	//extractData(data);
	extractData3(data,cliArgs[1]);
    }
}, function(err) {
    console.log(err);
});
