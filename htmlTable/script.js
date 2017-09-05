window.onload = function() {
    init();
}

function init() {
    document.body.addEventListener('mouseover',handleBodyEvent);
    populateTable();
}

handleBodyEvent = function(e) {
    var t = e.target;

    if (t.nodeName ==='TD') {
	hoverByClass(t.className,'red','white');
    }
}

function hoverByClass(classname,colorOver,colorOut) {
    var elms = document.getElementsByClassName(classname),
	i, k;
    for (i = 0; i < elms.length; i++) {
	elms[i].onmouseover = function() {
	    for (k = 0; k < elms.length; k++) {
		elms[k].style.backgroundColor=colorOver
	    }
	};
	elms[i].onmouseout = function() {
	    for (k = 0; k < elms.length; k++) {
		elms[k].style.backgroundColor=colorOut
	    }
	};
    }
}


populateTable = function() {
    var dataLength = data.length,
	tickerLength,
	i,j,
	tableRow,
	output = "",
	node,
	table = document.getElementById("dataTable");

    
    for (i = 0; i < dataLength; i++) {
	tableRow = "<tr> <td>"+data[i].date+"</td>";
	tickerLength = data[i].ticker.length;
	for (j = 0; j < tickerLength; j++) {
	    node = "<td class='" + data[i].ticker[j] + "'>" + data[i].ticker[j] + "</td>";
	    tableRow += node;
	    console.log(node);
	}
	tableRow += "</tr>";
	output += tableRow;
//	console.log(template);
    }
    table.innerHTML = output;
};
