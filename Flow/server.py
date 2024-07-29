# Main Server file
# Return only when server closes

import json
import network
import socket
import rqParse

# Request loop state and initial condition
state = "shutdown"

def start():
    global state
    # pre-start check
    if not network.WLAN(network.STA_IF).isconnected():
        return json.loads("""{"server error": ["not connected"]}""")
    
    # Socket configuration
    pair = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(pair)
    s.listen(5)

    # Start request loop
    state = "running"
    status = run(s)
    # End
    return json.loads("""{"exitstatus": ["%s"]}""" %(status))# Return exit status
    
# Actively accept incomming connection
# and parse the requests for handling
def run(sock):
    global state
    # Main request loop
    while state == "running":
        
        # BLOCKING CALL!
        # Accept connections
        conn, address = sock.accept()
    
        # Decode request
        rqRaw = conn.recv(1024).decode("utf-8")

        # Filter POST requests
        if not rqRaw.find("POST /") == -1:
            
            # Read boundary string
            boundary = rqRaw[rqRaw.find("boundary=")+9:rqRaw.find("User-Agent: ")-2]
            
            # Initialize data and loop condition
            data = ""
            tick = 0
            
            # Stream data from POST request
            while tick < 2:
                
                # Read one line of data
                line = conn.readline().decode("utf-8")
                
                # Check, increment tick & skipe write on boundary string
                if line.find(boundary) != -1:
                    tick += 1
                    continue
                
                # Write data
                if tick == 1 and line != "":
                    data += line
            
            # Find metadata delimiter
            srch = data.find("Content-Type:")
            file = data[(data.find("\n", srch, srch + 50)):]
            
            # Extract filename: MAX 20 charecters
            nid = data.find("filename=") + 10
            name = "/http/%s" %(data[nid:data.find("\"",nid,nid+20)])
            
            # Write file
            with open(name, "w") as f:
                f.write(file)

            # Service final request
            request = rqRaw[rqRaw.find("POST /")+6:rqRaw.find("HTTP/1.1")-1]
        
        # Shutdown command
        elif rqRaw.find("shutdown.html") != -1:
            # Change state to end loop
            state = "shutdown"
            
            # Service final request
            request = rqRaw[rqRaw.find("GET ")+5:rqRaw.find("HTTP/1.1")-1]
        
        # Regular request
        else:
            request = rqRaw[rqRaw.find("GET ")+5:rqRaw.find("HTTP/1.1")-1]
        
        # Parse, respond & close
        try:
            conn.write(rqParse.parse(request))
        except:
            state = "crash 0x0A"
        conn.close()
        
    # End condition
    # Return JSON format as value or array
    return state