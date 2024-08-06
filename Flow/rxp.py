# rxp.py
# RX loop parse module
# Edit: 06/08/24
# by NAticHAJ

import state
import msg
import server
import nic

# Parsing commands (& arguments)
def parse(query):
    
    # Extract command
    for i in query:
        switch = str(i)
        break 

    # Command switch #
    # {"flags": []}
    if switch == "flags":
        return state.flags(query[switch])
    
    # {"interface": ["up"]}
    elif switch == "interface":
        return nic.iface(query[switch])
    
    # {"scan": []}
    elif switch == "scan":
        return nic.scan(query[switch])
    
    # {"connect": ["mySSID", "myPassword"]}
    # {"connect": ["intetnet", "Brugsanvisning"]}
    elif switch == "connect":
        return nic.connect(query[switch])
    
    # {"disconnect": []}
    elif switch == "disconnect":
        return nic.disconnect(query[switch])
    
    # {"server": []}
    elif switch == "server":
        return server.start(query[switch])
    
    # {"end": []}
    elif switch == "end":
        if len(query[switch]) == 0:
            state.rxloop = 0
            return msg.end("command")
        else:
            return msg.err("takes no arguments")
    
    # No match response
    return msg.err("not a command")
