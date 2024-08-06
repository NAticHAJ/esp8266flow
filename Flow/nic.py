# nic.py
# Network interface module
# Edit: 06/08/24
# by NAticHAJ

import network
import state
from msg import err
from time import sleep

# Initial state update
interface = network.WLAN(network.STA_IF)
state.updown = interface.active()
state.online = interface.isconnected()

# Interface configuration
# Takes no or 1 argument
def iface(args):
    # Check for no arguments
    if len(args) == 0:
        return """{"interface": ["%s"]}""" %("up" if state.updown else "down")
    
    # Check for too many arguments
    elif len(args) > 1:
        return err("too many arguments")
    
    # Up, Down & invalid
    if args[0] == "up":
        interface.active(True)
    elif args[0] == "down":
        interface.active(False)
    else:
        return err("invalid argument")
    
    # Update flag
    state.updown = int(interface.active())
    
    # Respond
    return """{"interface": ["%s"]}""" %("up" if interface.active() else "down")
    
# Scan for access points
# Takes no arguments
def scan(args):
    # Check for no arguments
    if len(args) > 0:
        return err("takes no arguments")
    
    # Check interface flag
    if not state.updown:
        return err("interface down")
    
    # Scan for networks
    nets = interface.scan()
    
    # Assign names
    list = []
    for ssid, bssid, channel, rssi, authmode, hidden in nets:
        list.append(ssid.decode("utf-8"))

    # Assemble JSON
    jstr = """{"ssid": ["""
    for name in list:
        jstr += """"%s", """ %(name)
    jstr = jstr[:-2]
    jstr += "]}"
    
    # Cleanup
    del nets, list, name
    
    # Respond
    return jstr

# Connect to Access Point
# Takes SSID & PSK as arguments
def connect(args):
    # Check for 2 arguments
    if not len(args) == 2:
        return err("takes 2 arguments")
    
    # Check interface flag
    if not state.updown:
        return err("interface down")
    
    # Disconnect from current network
    if interface.isconnected():
        interface.disconnect()
        while interface.isconnected():
            continue
        
    # Attempt to connect
    try:
        interface.connect(args[0], args[1])
    except:
        # Format error
        return err("not string")
    
    # Wait for connection or timeout ( 15s )
    counter = 0
    timeout = 15
    while interface.status() == 1:
        sleep(0.1)
        counter += 1
        if counter >= timeout*10:
            break
    del counter, timeout
    
    
    # Update flag
    state.online = int(interface.isconnected())
    
    # Respond
    return """{"connect": ["%d", "%s"]}""" %(interface.status(),str(interface.ifconfig()[0]))

def disconnect(args):
    if len(args) > 0:
        return err("takes no arguments")
    # Disconnect from current network
    if interface.isconnected():
        interface.disconnect()
        while interface.isconnected():
            continue
    
    # Update flag
    state.online = interface.isconnected()
    
    # Respond
    return """{"disconnect": ["%d", "%s"]}""" %(interface.status(),str(interface.ifconfig()[0]))