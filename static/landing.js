function downloading() {
    var messageBox = document.getElementById("message");
    messageBox.innerHTML = "Fetching results ...";
    messageBox.className = 'pass';
    document.getElementById("topHeading").innerHTML = "Fetching results ...";
    console.log("from downloading");
}