
var i = 1;

function addRowSearchWithin() {
    var original = document.getElementById('rowSearchWithin' + i);
    var clone = original.cloneNode(true);
    i++;

    clone.id = "rowSearchWithin" + i;
    clone.getElementsByTagName('select')[0].id = "selectSearchWithin" + i;
    clone.getElementsByTagName('input')[0].id = "textSearchWithin" + i;
    clone.getElementsByTagName('input')[1].id = "buttonSearchWithin" + i;

    clone.getElementsByTagName('select')[0].name = "selectSearchWithin" + i;
    clone.getElementsByTagName('input')[1].name = "textSearchWithin" + i;

    original.parentNode.appendChild(clone);

    original.getElementsByTagName('input')[1].value = "-";
    original.getElementsByTagName('input')[1].setAttribute("onclick", "deleteRowSearchWithin(this)");

}

function deleteRowSearchWithin(thisButton) {
    thisButton.parentNode.remove();
}



var j = 1;

function addRowFilters() {
    var original = document.getElementById('rowFilters' + j);
    var clone = original.cloneNode(true);
    j++;

    clone.id = "rowFilters" + j;
    clone.getElementsByTagName('select')[0].id = "select1Filters" + j;
    clone.getElementsByTagName('select')[1].id = "select2Filters" + j;
    clone.getElementsByTagName('input')[0].id = "textFilters" + j;
    clone.getElementsByTagName('input')[1].id = "buttonFilters" + j;

    clone.getElementsByTagName('select')[0].name = "select1Filters" + j;
    clone.getElementsByTagName('select')[1].name = "select2Filters" + j;
    clone.getElementsByTagName('input')[0].name = "textFilters" + j;

    original.parentNode.appendChild(clone);

    original.getElementsByTagName('input')[1].value = "-";
    original.getElementsByTagName('input')[1].setAttribute("onclick", "deleteRowFilters(this)");

}

function deleteRowFilters(thisButton) {
    thisButton.parentNode.remove();
}
