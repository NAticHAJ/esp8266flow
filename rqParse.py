import flags
import json
from machine import UART
from time import sleep
from os import remove, listdir

# UART port setup
port = UART(0, 115200)

def fourofour():
    with open("default/404.html", "r") as file:
        return file.read()

# Parse request from browser
def parse(term):
    # Initialize return variable
    response = None
    
    # DEBUG INFORMATION
    print(term)
    
    # Request term filtering
    # Dynamic AJAX action handler
    if term.find("?") != -1:
        if term.find("value=") != -1:
            # Call AJAX handler
            return ajax(term)
        else:
            # Return 404
            return fourofour()
            
    # Default query
    elif term == "":
        term = "http/index.html"
    
    # Default directory
    elif term.find("default/") == -1 and term.find("http/") == -1 and term != "favicon.ico":
        term = "http/" + term

    # Internal file resolver
    # Find and read
    try:
        # Try text resolving
        try:
            # Open, read an d close file
            with open(term, "r") as file:
                response = file.read()
                
        # Fallback to binary resolving
        except:
            # Open, read and close file
            with open(term, "rb") as file:
                response = file.read()
    
    # Respond 404 Error page
    except:
        response = fourofour()

    # Return data
    return response

# Parse and handle AJAX requests for dynamic responses
def ajax(request):
    # Extraxt key/value pair
    key = request[:request.find("?")]
    value = request[request.find("=")+1:]
    
    # Internal queries
    # Flow Filer viewport
    if key == "refresh":
        if value == "viewport":
            id = 0
            html = ""
            for item in listdir("http"):
                itemName = str(item)
                html += """<input id="item%d" type="radio" name="file" value="%s"><label for="item%d">%s</label><br>""" %(id,itemName,id,itemName)
                id += 1
            if not id:
                html = """<label class="cursive">Empty</label><br>"""
            return html
        else:
            return fourofour()
    
    # Downloading files from /http/
    elif key == "getfile":
        with open("/http/%s" %(value), "r") as f:
            return f.read()
    
    # Removing files from /http/ 
    elif key == "delete":
        remove("/http/%s" %(value))
        return "<!DOCTYPE html><html></html>"        
                
    # Assemble JSON string & Tx over UART
    if not flags.serial:
        port.write("""{"%s": "%s"}""" %(key,value))
    else:
        print("""{"%s": "%s"}""" %(key,value))
    
    # Unstable
    
    # Await response
    if not flags.serial:
        while (port.any() < 1):
            continue
        jstr = json.loads(port.read())
    else:
        try:
            jstr = json.loads(input("[SERVER] Type here: "))
        except:
            return """{"pa error": ["not JSON"]}"""
    
    # Filter input
    try:
        if len(jstr["ajax"]) == 0:
            return """Failed at value test"""
    except:
        return """Failed at key test"""
        
    
    # Assign AJAX response
    # Response format: {"led": ["color": "red"]}
    # Fetch file: /led/color/red.txt
    for i in jstr:
        # Assemble file path
        path = "/%s/%s/%s.txt" %(i, jstr[i][0], jstr[i][1])

    # Read file
    with open(path) as file:
        response = file.read()
    
    # Return AJAX response
    return response
