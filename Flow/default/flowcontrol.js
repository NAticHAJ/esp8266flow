// flowcontrol.js
// Script file for Flow Control
// Edit: 06/08/24
// by NAticHAJ

function flowcontrol() {

    // Load Flow Filer viewport
    flowfiler();
    
    // Load Flow State data
    flowstate();
    
    // Refresh Flow State
    setInterval(flowfiler,5000);
    setInterval(flowstate,5000);
}




// THESE ARE FUNCTIONS RELATED TO FLOW FILER !!!

function flowfiler() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.getElementById("viewport").innerHTML = this.responseText;
    }
    xhttp.open("GET", "/refresh?value=flowfiler", true);
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
    const fi = document.getElementById("upload");
    if(fi.files.length < 1) {
        alert("No file selected");
        event.preventDefault();
    }
    else if (fi.files.item(0).size > 6656){ 
        alert("File too large. MAX: 6.5 KB");
        event.preventDefault();
    }
}

function rem() {
    const radioButtons = document.querySelectorAll('input[name="file"]');
    var confirmed = document.getElementById("confirm");
    let file;
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
                event.preventDefault();
                confirmed.checked = false;
            }
            xhttp.open("GET", query, true);
            xhttp.send();
        }
    }
    event.preventDefault();
}



// THESE ARE FUNCTIONS RELATED TO FLOW STATE !!!

function flowstate() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        state = JSON.parse(this.responseText);
        document.getElementById("ramInfo").innerHTML = state.memuse + " / " + state.memtot + " Bytes";
        ram = document.getElementById("ram");
        ram.style.width = state.mempct;
        if (ram.style.width > "80%") {
            ram.style.background = "red";
        } else if (ram.style.width < "50%") {
            ram.style.background = "green";
        } else {
            ram.style.background = "orange";
        }
        document.getElementById("flashInfo").innerHTML = state.dskuse + " / " + state.dsktot + " KBytes";
        document.getElementById("flash").style.width = state.dskpct;
    }
    xhttp.open("GET", "/refresh?value=flowstate", true);
    xhttp.send();
}

