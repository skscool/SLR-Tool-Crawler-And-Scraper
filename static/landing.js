function downloading() {
    var messageBox = document.getElementById("message");
    messageBox.innerHTML = "Fetching results ...";
    messageBox.className = 'pass';
    document.getElementById("topHeading").innerHTML = "Fetching results ...";
    console.log("from downloading");
}
function updateYear(){
	curr_year = new Date().getFullYear();
	var ys = document.getElementById("yearStart");
	ys.setAttribute("max",curr_year);

	var ye = document.getElementById("yearEnd");
	ye.setAttribute("max",curr_year);
	ye.setAttribute("value",curr_year);
}

function invalid_years(){
    var messageBox = document.getElementById("message");
    messageBox.innerHTML = "Starting year should not be greater than Ending year";
    messageBox.className = 'fail';
}

function validate(){
	// console.log("dsfads",document.main_form.basic.value);
	if(document.main_form.basic.value == ""){
	    var messageBox = document.getElementById("message");
	    messageBox.innerHTML = "Search string empty";
	    messageBox.className = 'fail';
	    return false
	}
	if (parseInt(document.main_form.yearStart.value) > parseInt(document.main_form.yearEnd.value)){
		console.log("Hi");
		invalid_years()
		return false;
	}
	else{
		downloading();
		return true;
	}
}
