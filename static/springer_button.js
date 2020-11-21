  var i=1;
  function addRowLiteratureType() {
      var original = document.getElementById('rowLiteratureType' + i);
      var clone = original.cloneNode(true);
      i++;

      clone.id = "rowLiteratureType" + i;
      clone.getElementsByTagName('select')[0].id = "selectLiteratureType" + i;
      clone.getElementsByTagName('input')[0].id = "buttonLiteratureType" + i;

      clone.getElementsByTagName('select')[0].name = "selectLiteratureType" + i;
      
      original.parentNode.appendChild(clone);
      
      original.getElementsByTagName('input')[0].value = "-";
      original.getElementsByTagName('input')[0].setAttribute("onclick", "deleteRowLiteratureType(this)");

  }

  function deleteRowLiteratureType(thisButton){
      thisButton.parentNode.remove();
  }



  var j=1;
  function addRowSubcategory() {
      var original = document.getElementById('rowSubcategory' + j);
      var clone = original.cloneNode(true);
      j++;

      clone.id = "rowSubcategory" + j;
      clone.getElementsByTagName('select')[0].id = "selectSubcategory" + j;
      clone.getElementsByTagName('input')[0].id = "buttonSubcategory" + j;

      clone.getElementsByTagName('select')[0].name = "selectSubcategory" + j;
      
      original.parentNode.appendChild(clone);
      
      original.getElementsByTagName('input')[0].value = "-";
      original.getElementsByTagName('input')[0].setAttribute("onclick", "deleteRowSubcategory(this)");

  }

  function deleteRowSubcategory(thisButton){
      thisButton.parentNode.remove();
  }
  
  
  var k=1;
  function addRowReleaseDate() {
      var original = document.getElementById('rowReleaseDate' + k);
      var clone = original.cloneNode(true);
      k++;

      clone.id = "rowReleaseDate" + k;
      clone.getElementsByTagName('select')[0].id = "selectReleaseDate" + k;
      clone.getElementsByTagName('input')[0].id = "buttonReleaseDate" + k;

      clone.getElementsByTagName('select')[0].name = "selectReleaseDate" + k;
      
      original.parentNode.appendChild(clone);
      
      original.getElementsByTagName('input')[0].value = "-";
      original.getElementsByTagName('input')[0].setAttribute("onclick", "deleteRowReleaseDate(this)");

  }

  function deleteRowReleaseDate(thisButton){
      thisButton.parentNode.remove();
  }
  
  
  var l=1;
  function addRowLanguages() {
      var original = document.getElementById('rowLanguages' + l);
      var clone = original.cloneNode(true);
      l++;

      clone.id = "rowLanguages" + l;
      clone.getElementsByTagName('select')[0].id = "selectLanguages" + l;
      clone.getElementsByTagName('input')[0].id = "buttonLanguages" + l;

      clone.getElementsByTagName('select')[0].name = "selectLanguages" + l;
      
      original.parentNode.appendChild(clone);
      
      original.getElementsByTagName('input')[0].value = "-";
      original.getElementsByTagName('input')[0].setAttribute("onclick", "deleteRowLanguages(this)");

  }

  function deleteRowLanguages(thisButton){
      thisButton.parentNode.remove();
  }
