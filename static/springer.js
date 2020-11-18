//DOM objects
var selectSubcategory1 = document.getElementById("selectSubcategory1");
var searchString = document.getElementById("searchString");
var selectReleaseDate1 = document.getElementById("selectReleaseDate1");
var selectLanguages1 = document.getElementById("selectLanguages1");
var selectLiteratureType1 = document.getElementById("selectLiteratureType1");				//----------------change 1---------------- get dropdown object
var messageBox = document.getElementById("message");

//add error handling if the select dropdown is empty.. i.e fetch filter button is not clicked yet
selectSubcategory1.addEventListener("click", filterNotAvailable);
selectReleaseDate1.addEventListener("click", filterNotAvailable);
selectLanguages1.addEventListener("click", filterNotAvailable);
selectLiteratureType1.addEventListener("click", filterNotAvailable);

 function filterNotAvailable() {
   if ( this.options[0].value == '' ) {
	 this.options[0].text = 'Please Get Filters First!'
   }
 }


function fetchFiltersFromSpringer(url, params) {
	////alert(url + " "+ params);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			////alert("response received!");
			var response = this.responseText;				//response from server has all possible types of filter each type with a differet delimiter

			subcategory = response.split('^');				//list of category-filter values etc...
			dates = subcategory.pop().split('$');
			languages = dates.pop().split('#');
			types = languages.pop().split('!');							//--------------change 2------------------ store the response from server
			
			types.shift();
			types.pop();
			
			//get all the filter fields and paste the filters in them
			var allSelectSubcategories = document.querySelectorAll('[id^=selectSubcategory]');
			var allSelectReleaseDates = document.querySelectorAll('[id^=selectReleaseDate]');
			var allSelectLanguages = document.querySelectorAll('[id^=selectLanguages]');
			
			//sanitize the filters if needed
			for(var i = 0; i < subcategory.length; i++) {
				subcategory[i] = subcategory[i].replace(/^\s*/, "").replace(/\s*$/, "");
			}
			
			for(var i = 0; i < dates.length; i++) {
				dates[i] = dates[i].replace(/^\s*/, "").replace(/\s*$/, "");
			}
			
			for(var i = 0; i < languages.length; i++) {
				languages[i] = languages[i].replace(/^\s*/, "").replace(/\s*$/, "");
			}
			
			
			
			//empty all options of all dropdown of this kind
			for(itr = 0; itr < allSelectSubcategories.length; itr++){
				var length = allSelectSubcategories[itr].options.length;
				for(i = length-1; i >= 0; i--){
					allSelectSubcategories[itr].options[i] = null;
				}
			}
			
			//fill all dropdown of this kind with filter options
			for(itr = 0; itr < allSelectSubcategories.length; itr++){
				allSelectSubcategories[itr].options.add(new Option("---none---"));
				for(var i = 0; i < subcategory.length; i++) {
					allSelectSubcategories[itr].options.add(new Option(subcategory[i]));
				}
			}
			
			
			//empty all options of all dropdown of this kind
			for(itr = 0; itr < allSelectReleaseDates.length; itr++){
				var length = allSelectReleaseDates[itr].options.length;
				for(i = length-1; i >= 0; i--){
					allSelectReleaseDates[itr].options[i] = null;
				}
			}
			
			//fill all dropdown of this kind with filter options
			for(itr = 0; itr < allSelectReleaseDates.length; itr++){
				allSelectReleaseDates[itr].options.add(new Option("---none---"));
				for(var i = 0; i < dates.length; i++) {
					allSelectReleaseDates[itr].options.add(new Option(dates[i]));
				}
			}

			//empty all options of all dropdown of this kind
			for(itr = 0; itr < allSelectLanguages.length; itr++){
				var length = allSelectLanguages[itr].options.length;
				for(i = length-1; i >= 0; i--){
					allSelectLanguages[itr].options[i] = null;
				}
			}
			
			//fill all dropdown of this kind with filter options
			for(itr = 0; itr < allSelectLanguages.length; itr++){
				allSelectLanguages[itr].options.add(new Option("---none---"));
				for(var i = 0; i < languages.length; i++) {
					allSelectLanguages[itr].options.add(new Option(languages[i]));
				}
			}

			
			var length = selectLiteratureType1.options.length;						//--------------change 3------------------ clear dropdown and then populate
			for (i = length-1; i >= 0; i--) {
				selectLiteratureType1.options[i] = null;
			}
			
			
			selectLiteratureType1.options.add(new Option("---none---"));
			for(var i = 0; i < types.length; i++) {
				types[i] = types[i].replace(/^\s*/, "").replace(/\s*$/, "");
				selectLiteratureType1.options.add(new Option(types[i]));
			}
			
			if(response == ''){
				//alert("no filters found for this search string!");
				messageBox.innerHTML = "No filters found for this search string!";
				messageBox.className = 'fail';
			}else{
				//alert("filters found!");
				messageBox.innerHTML = "Filters Available!";
				messageBox.className = 'pass';
			}
			
	   }
	};
	xhttp.open("GET", url+"?"+params, true);		//make a get request to the url with param as search string from input box
	xhttp.send();
}


function getFilters(){
	if(searchString.value == ""){
		searchString.placeholder = "Search String Required!";
		searchString.classList.add('error');
		return;
	}
	
	messageBox.innerHTML = "Fetching Filters...";
	messageBox.className = 'pass';
	
	var url = "/fetchFilters";								
	var string = searchString.value;
	var params = "searchString=" + string;
	fetchFiltersFromSpringer(url, params);
}

function validateMyForm(event){
	event.preventDefault();
	var springerForm = document.getElementById('springerForm');
	if(searchString.value == ""){
		searchString.placeholder = "Search String Required!";
		searchString.classList.add('error');
		return false;
	}
	
	var url = "/isSearchValid";				
	const formx = document.querySelector('form');
	const data = Object.fromEntries(new FormData(formx).entries()); 	//get data from the form
	var stateOfResult = false;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = this.responseText;				//response from server whether search was valid or not
			if(response == 'valid'){
				messageBox.innerHTML = "Result found! Fetching BibTex...";
				messageBox.className = 'pass';
				stateOfResult = true;
				springerForm.submit();
				return;
			}else if(response == 'invalid'){
				messageBox.innerHTML = "No result found for search!";
				messageBox.className = 'fail';
				stateOfResult = false;
				return;
			}
			stateOfResult = false;
	   }
	};
	xhttp.open("POST", url, true);	//make a post request to the url with payload as form data
	xhttp.send(JSON.stringify(data));

		messageBox.innerHTML = "Searching in Springer...";
		messageBox.className = 'pass';

}
