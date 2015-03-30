// based on BashScripts/MuddleParser.js

var readline=require('readline')
var fs=require('fs')

var filename='/home/puffjay/Muddle.txt'
if (typeof process.argv[2] !== 'undefined') {
    filename=process.argv[2]
}

//console.log("Using "+filename);

var rl = readline.createInterface({
    input : fs.createReadStream(filename),
    output: process.stdout,
    terminal: false
})

var myObj = {};
var bigArray = [];
//readline code

//Read the file a line at a time
//ignore comment lines (#)
//if line starts with a date, populate the date property of the object with that value
//if the line doesn't start with a date and the date property is already populated, parse the line into the list array property
rl.on('line',function(line){
    var trimLine = line.trim();

    var dateRE = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/;
    
    var dateMatch = trimLine.match(dateRE); //alternately if line doesn't start with # and not of zero length after trim whitespace
  //console.log("dateMatch:",dateMatch);

    if ( trimLine[0] !== "#") { //ignore comment lines
	//console.log("tl:"+trimLine+" tlIo:"+trimLine.indexOf("201") );
//	if ( trimLine.indexOf("201") !== -1 ) { //
 	if (dateMatch !== null) {
	    //print out data before overwriting
	    if (typeof myObj.date !== 'undefined' ){
//		console.log("obj:",myObj);
		bigArray.push(myObj);
		myObj = {}; //clear out the obj
	    }
	    //	    console.log("data set");
	    myObj.date=trimLine;
	} else { 
	    //if we've populated the date property and the line has length
	    if ( typeof myObj.date !== 'undefined' && trimLine.length > 0 ) { 
		var temp = returnArray(trimLine);
		if ( temp.length > 0 ) {
		    myObj.list=temp;//returnArray(trimLine);
		}
	    } else {
		//console.log(trimLine);
	    }
	}
    }
});

//When we are at the end of the file, output any last line
//perform any processing on our object/array now that we are done populating it.
rl.on('close',function() {
    //use this as a trigger to perform any postProc

    //need to printout the last obj here    ......???really won't this be a duplicate?...hmm appears not
    if (typeof myObj.date !== 'undefined' && myObj.list.length > 0 ){
//	console.log("obj:",myObj);
	bigArray.push(myObj);
    };
    bigArray.sort(function(a,b) { 
	if (a.date > b.date) {
	    return -1;
	}
	if (a.date < b.date) {
	    return 1;
	}
	// a must be equal to b....and this should never happen
	return 0;
    });
    appendStats(bigArray);
    //key off streakCount = 1 to highlight new entries
    console.log(JSON.stringify(bigArray));
    //    console.log(bigArray);
    //    console.log("rl close");

})

//end readline code

function returnArray(line) { 
    if (false === true){
	//this will return a simple array of the tickers
	return line.split(' '); 
    } else {
	//this will return an array of objects that hold the ticker, index, and whatever else I want to tack on
	var tickerArray = line.toUpperCase().split(' ');
	var returnArray = [];
	tickerArray.forEach(function(ele,ind,fullArray){
	    returnArray.push({"ticker":ele,"index":ind});
	});
	return returnArray
    }


}
/*
  Here we will loop backwards over our sorted array (loooping from oldest entry to most recent entry) and compute the streak of each ticker. Items with a streakCount === 1 are new to the list and can easily be marked. 
We also find the list of tickers that exit the list.
We also collect / accumulate the rank to perform stats on
*/
function appendStats(inputArray){
    var currentStats = {previousMemberArray:[],memberExitsArray:[]}; 
    var inputArrayLength = inputArray.length;

    for (var index=inputArrayLength-1; index>=0; index--){
	//Psuedocode:loop over array from the highest index (oldest) and move forward.
	//perform a diff of the current array in inputArray to currentStatsArray; if item in inputArray[i] in currentStatsArray, then increment streakCount in currentStatsArray. If item in inputArray[i] is not in currentStatsArray, then pop/slice element from currentStatsArray and push to old array obj. it's streakCount will be preserved....err that is wrong. if it is in inputArray[i], but not currentStatsArray then we need to tag it as new. 
	//each loop through need to clear out new and old array;  these will be populated based on actions on the current array. 

	Array.prototype.diff = function(a) {
	    return this.filter(function(i) {return a.indexOf(i.ticker) < 0;});
	};
	var currentInputArray = inputArray[index].list;
	//Ugg the above diff function works on simple value based arrays but fails when they are objects
	//	var diffArray = currentInputArray.diff(currentStats.previousMemberArray);
	//	currentStats.memberExitsArray=currentStats.previousMemberArray.diff(currentInputArray);
	//	inputArray[index].memberExitsArray=currentStats.memberExitsArray

//get the tickers that left the list
	//this seems stupidly inefficient (O(n^2) for each array element)
	currentStats.previousMemberArray.forEach(function(ele,index,fA) {
	    var flag = false;
	    for (var idx=0; idx<currentInputArray.length; idx++){
		//if we have a match, break...
		if(flag === true || ele.ticker === currentInputArray[idx].ticker) {
		    flag = true;
		    break;
		}
		//..otherwise push the element onto the array as it wasn't found
		//		currentStats.memberExitsArray.push(ele);
	    }
	    /*	    currentInputArray.forEach(function(ele_,index_,fA_){

		    });*/
	    if (!flag) {
		currentStats.memberExitsArray.push(ele);
	    }
	});
	inputArray[index].memberExitsArray=currentStats.memberExitsArray;
	currentStats.memberExitsArray=[];

//compute our streakCount
	//	console.log("cIa:b:",currentInputArray);
//		console.log("cS.pMA:",currentStats.previousMemberArray);
	currentInputArray.forEach(function(ele,ind,fA) {
	    var filterEle = currentStats.previousMemberArray.filter(function(ele_,ind_,fA_) { return ele.ticker === ele_.ticker; } );
	    //	    console.log(ele.ticker+' '+filterEle.length+' '+filterEle[0].streakCount); 
	    if ( filterEle.length > 0 ) {
		/*if ( ele.streakCount ) {*/ 
		//	    console.log(ele.ticker+' '+filterEle.length+filterEle[0].streakCount); 
		ele.streakCount=filterEle[0].streakCount+1;
//		console.log("fE0.i:"+filterEle[0].index+" ei:"+ele.index+" fE0.rA:"+filterEle[0].rankAccumulator); 
		ele.rankAccumulator=ele.index+filterEle[0].rankAccumulator;
		//	    console.log(ele.ticker+' '+filterEle.length+' '+filterEle[0].streakCount+' '+ele.streakCount); 
	    } else { ele.streakCount=1; ele.rankAccumulator=ele.index; }
	    //}
	    
	});
	//	console.log("cIa:a:",currentInputArray);
 	currentStats.previousMemberArray=currentInputArray;
    }
}
