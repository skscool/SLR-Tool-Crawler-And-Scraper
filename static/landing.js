function updateYear() {
    curr_year = new Date().getFullYear();
    var ys = document.getElementById("yearStart");
    ys.setAttribute("max", curr_year);

    var ye = document.getElementById("yearEnd");
    ye.setAttribute("max", curr_year);
    ye.setAttribute("value", curr_year);
}

function fail_msg(s) {
    var messageBox = document.getElementById("message");
    messageBox.innerHTML = s;
    messageBox.className = 'fail';
}

function validate() {
    // console.log("dsfads",document.main_form.basic.value);
    var messageBox = document.getElementById("message");
    messageBox.innerHTML = '';
    var curr_year = new Date().getFullYear();
    if (document.main_form.basic.value == "") {
        fail_msg("Search string empty");
        return false
    }
    if (parseInt(document.main_form.yearStart.value) < 1872) {
        fail_msg("Starting year must be greater than 1872")
        return false;
    }
    if (parseInt(document.main_form.yearStart.value) > curr_year) {
        fail_msg("Starting year must be less than " + curr_year)
        return false;
    }
    if (parseInt(document.main_form.yearEnd.value) < 1872) {
        fail_msg("Ending year must be greater than 1872")
        return false;
    }
    if (parseInt(document.main_form.yearEnd.value) > curr_year) {
        fail_msg("Ending year must be less than " + curr_year)
        return false;
    }

    if (parseInt(document.main_form.yearStart.value) > parseInt(document.main_form.yearEnd.value)) {
        console.log("Hi");
        fail_msg("Starting year should not be greater than Ending year")
        return false;
    }
    downloading();
    return true;
}