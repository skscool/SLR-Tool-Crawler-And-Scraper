
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
    clone.getElementsByTagName('input')[0].name = "textSearchWithin" + i;
    clone.getElementsByTagName('input')[1].name = "textSearchWithin" + i;

    original.parentNode.appendChild(clone);

    original.getElementsByTagName('input')[1].value = "-";
    original.getElementsByTagName('input')[1].setAttribute("onclick", "deleteRowSearchWithin(this)");

}

function deleteRowSearchWithin(thisButton) {
    thisButton.parentNode.remove();
}
