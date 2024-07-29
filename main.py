from machine import Pin
from machine import UART
import flags
import network
import nic
import server
import json
import gc

# Pin setup for output mode selection
trigger = Pin(0, Pin.IN, Pin.PULL_UP)

# Update online flag
flags.online = int(network.WLAN(network.STA_IF).isconnected())

# Update updown flag
flags.updown = int(network.WLAN(network.STA_IF).active())

# Select UART or USB mode via PIN 0 High/Low
flags.serial = trigger.value()
if not flags.serial:
    # Disable REPL
    os.dupterm(None, 1)
    
    # Initialize UART PORT
    port = UART(0, 115200)

# Retun parsing fault to uartParse
def returnFault(cause):
    return """{"parse error": ["%s"]}""" %(cause)

# Parsing commands (& arguments)
def uartParse(query):
    
    # Extract command
    for i in query:
        switch = str(i)
        # Ignore subsequent commands
        break 

    # Command switch #
    # {"flags": []}
    if switch == "flags":
        return json.loads(flags.get(query))
    
    # {"interface": ["up"]}
    elif switch == "interface":
        return json.loads(nic.iface(query))
    
    # {"scan": []}
    elif switch == "scan":
        return json.loads(nic.scan(query))
    
    # {"connect": ["mySSID", "myPassword"]}
    elif switch == "connect":
        return json.loads(nic.connect(query))
    
    # {"disconnect": []}
    elif switch == "disconnect":
        return json.loads(nic.disconnect())
    
    # {"server": []}
    elif switch == "server":
        return server.start()
    
    # {"end": []}
    elif switch == "end":
        return endLoop(query)
    
    # No match response
    return json.loads(returnFault("not a command"))

# print JSON faults from main Rx loop
def printFault(cause):
    if flags.serial:
        print("""{"json error": ["%s"]}""" %(cause))
    else:
        port.write("""{"json error": ["%s"]}""" %(cause))
        
# End main Rx loop
def endLoop(args):
    if len(args["end"]) > 0:
        return json.loads("""{"end error": ["takes no arguments"]}""")
    flags.rxloop = 0
    return json.loads("""{"rx loop": ["ending"]}""")
        

##############################
# TODO: Configuration loader 
# Check for config file
# load configuration
# else continue to main Rx
###############################

# Set loop condition
flags.rxloop = 1

# Main Rx loop
while flags.rxloop:
    # UART ONLY - Wait for input
    if not flags.serial:
        # Wait for input
        while (port.any() < 1):
            continue
        
        # Take input as JSON format
        command = json.loads(port.read())
        port.write(json.dumps(uartParse(command)))
    
    # REPL ONLY - Take REPL input
    else:
        try:
            # Filter input via JSON conversion
            command = json.loads(input("[RxLoop] Type here: "))
        
            # Deny empty input
            if not len(command) > 0:
                printFault("empty or malformed")
                continue
            else:
                # Parse finally approved command and print reponse
                print(json.dumps(uartParse(command)))
    
        # Invalid input
        except:
            printFault("malformed")
            continue
    
    # Clean up
    gc.collect()