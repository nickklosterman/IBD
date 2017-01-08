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
    if (cliArgs.length === 2) {
	extractData2(data,cliArgs[1]);
    } else {
	extractData(data);
    }
}, function(err) {
    console.log(err);
});
