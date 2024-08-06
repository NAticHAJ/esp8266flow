# rqp.py
# Webserver request module
# Edit: 05/08/24
# by NAticHAJ

import state
from machine import UART
from time import sleep
from os import remove, listdir

# UART port setup
port = UART(0, 115200)

# 404 - File not found landing page
def fourofour():
    with open("default/404.html", "r") as file:
        return file.read()

# Parse request string from web browser
# Input is determined by browser call
def parse(term):
    # Initialize return variable
    response = None
    
    # DEBUG INFORMATION
    print(term)
    
    # Check for AJAX querie
    if term.find("?value=") != -1:
        return ajax(term)
            
    # Default query
    elif term == "":
        term = "http/index.html"
    
    # Default directory
    elif term.find("default/") == -1 and term.find("http/") == -1 and term != "favicon.ico":
        term = "http/" + term

    # Internal file resolver
    try:
        # Text resolving
        try:
            # Open, read an d close file
            with open(term, "r") as file:
                response = file.read()
                
        # Binary resolving
        except:
            # Open, read and close file
            with open(term, "rb") as file:
                response = file.read()
    
    # Respond 404 Error page
    except:
        response = fourofour()

    # Return data
    return response

# AJAX query handler
# Unknown requests are Tx for external processing
# TODO: Implement config filter
def ajax(request):
    # Extraxt key/value pair
    key = request[:request.find("?")]
    value = request[request.find("=")+1:]
    
    # Internal queries
    if key == "refresh":
        # Initialize response
        id = 0
        html = ""
        
        # Flow filer HTML builder
        # RETURN FROM HERE!
        if value == "flowfiler":
            # TODO: Move listdir to stateMachine.py
            for item in listdir("http"):
                itemName = str(item)
                html += """<input id="item%d" type="radio" name="file" value="%s"><label for="item%d"><a href="/%s">%s</a></label><br>""" %(id,itemName,id,itemName,itemName)
                id += 1
            if not id:
                html = """<label class="cursive">Empty</label><br>"""
            return html
        
        # Flow state HTML builder
        elif value == "flowstate":
            return state.usage()
        
        # 404 - Not found
        else:
            return fourofour()
    
    # Downloading files from /http/
    elif key == "getfile":
        with open("/http/%s" %(value), "r") as f:
            return f.read()
    
    # Removing files from /http/ 
    elif key == "delete":
        remove("/http/%s" %(value))
        print("Good")
        return "<!DOCTYPE html><html></html>"        
                
    #v v v v v v v v v v v v v v v v v v v v v v v v#
    ############ External query handling ############
    #v v v v v v v v v v v v v v v v v v v v v v v v#
    
    #################################################
    ### Config filters for external uart requests ###
    #################################################
    
    #v v v v v v v v v v v v v v v v v v v v v v v v#
    ### Sensitive area for now! Avoid unknown rq! ###
    #v v v v v v v v v v v v v v v v v v v v v v v v#
    
    # Assemble JSON string & Tx over REPL or UART
    trx.tx("""{"%s": "%s"}""" %(key,value))

    # Await response
    jstr = trx.rx()

    # Filter input
    try:
        if True:
            return """Failed at value test OR INTENTIONAL TERMINATION ON PARSING"""
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
