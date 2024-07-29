function populate() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("files").innerHTML = this.responseText;
    }
    xhttp.open("GET", "/refresh?value=viewport", true);
    xhttp.send();
}

function getfile() {
    const radioButtons = document.querySelectorAll('input[name="file"]');
    let filename;
    let button;
    for (const item of radioButtons) {
        if(item.checked) {
            button = item;
            filename = item.value;
            break;
        }
    }
    if(!filename) {
        alert("No file selected");
    }
    else {
        query = "/getfile?value=";
        query += filename;
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            const element = document.createElement("a");
            element.setAttribute('href','data:text/plain;charset=utf-8, ' + encodeURIComponent(this.responseText));
            element.setAttribute('download', filename);
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            button.checked = false;
        }
        xhttp.open("GET", query, true);
        xhttp.send();
    }
    event.preventDefault();
}

function givefile() {
    if(!document.getElementById("upload").value) {
        alert("No file selected");
        event.preventDefault();
    }
}

function rem() {
    const radioButtons = document.querySelectorAll('input[name="file"]');
    var confirmed = document.getElementById("confirm");
    let file
    for (const item of radioButtons) {
        if(item.checked) {
            file = item.value;
            break;
        }
    }
    if(!file) {
        alert("No file selected");
    }
    else {
        if (!confirmed.checked) {
            alert("Confirm!");
        }
        else {
            query = "/delete?value=";
            query += file;
            const xhttp = new XMLHttpRequest();
            xhttp.onload = function() {
                location.reload();
            }
            xhttp.open("GET", query, true);
            xhttp.send();
        }
    }
    event.preventDefault();
}