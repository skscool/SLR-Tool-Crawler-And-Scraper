  var i=1;
  function addRow() {
      var original = document.getElementById('row' + i);
      var clone = original.cloneNode(true);
      i++;

      clone.id = "row" + i;
      clone.getElementsByTagName('select')[0].id = "select" + i;
      clone.getElementsByTagName('input')[0].id = "text" + i;
      clone.getElementsByTagName('input')[1].id = "button" + i;

      clone.getElementsByTagName('select')[0].name = "select" + i;
      clone.getElementsByTagName('input')[1].name = "text" + i;
      
      original.parentNode.appendChild(clone);
      
      original.getElementsByTagName('input')[1].value = "-";
      original.getElementsByTagName('input')[1].setAttribute("onclick", "deleteRow(this)");

  }

  function deleteRow(thisButton){
      thisButton.parentNode.remove();
  }