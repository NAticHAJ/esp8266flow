# server.py
# Webserver networking module
# Edit: 06/08/24
# by NAticHAJ

import state
import msg
import socket
import rqp
import trx
import gc

# Request loop state and initial condition
state.erstat = 0

# Starting call for webserver
# Takes no arguments
def start(args):
    if len(args) > 0:
        return msg.err("takes no arguments")
    
    # Check online flag
    if not state.online:
        return msg.err("not connected")
    
    # Socket configuration
    pair = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(pair)
    s.listen(5)

    # Reset error state
    state.erstat = 0
    
    # Respond with webserver exitstatus
    return msg.ecd(run(s))
    
# Actively accept incomming connection
# and parse the requests for handling
def run(sock):
    # Main request loop
    while not state.erstat:
        # BLOCKING CALL!
        # Accept connections
        conn, address = sock.accept()
    
        # Decode request
        rqRaw = conn.recv(1024).decode("utf-8")
        rqType = rqRaw[:rqRaw.find(" ")]
        rqPath = rqRaw[rqRaw.find(" ")+2:rqRaw.find("HTTP/1.1")-1]
        
        # Shutdown command
        if "shutdown.html" in rqPath:
            state.erstat = 1
            del rqRaw
        
        # For uploading files
        elif rqType == "POST":
            tick = 0
            boundary = rqRaw[rqRaw.find("boundary=")+9:rqRaw.find("User-Agent: ")-2]
            del rqRaw
            line = [[]]
            line.pop()
            trig = 0
            loop = 0
            name = ""
            while tick < 2:
                line.append(conn.readline().decode("utf-8"))
                gc.collect()
                if boundary in line[loop]:
                    tick += 1
                    line.pop()
                    loop -= 1
                elif not tick == 1:
                    line.pop()
                    loop -= 1
                elif "filename=" in line[loop] and not name:
                    name = "/http/" + line[loop][line[loop].find("filename=")+10:line[loop].find("\"\r\n")]
                    line.pop()
                    loop -= 1
                elif "Content-Type:" in line[loop]:
                    trig = 1
                    line.pop()
                    loop -= 1
                elif trig != 1:
                    line.pop()
                    loop -= 1
                loop += 1
            del tick, boundary, trig, loop
            
            with open(name, "w") as f:
                for i in line:
                    f.write(i)
                f.close()
            del line, name
        
        else:
            del rqRaw
        
        conn.write(rqp.parse(rqPath))
        del rqType, rqPath
        conn.close()
        del conn, address
        gc.collect()
        
    # End condition
    # Return JSON format as value or array
    return str(state.erstat)