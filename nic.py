import flags
import network
from time import sleep

# Setup WLAN interface in client mode
# Functions take and retur JSON objects

# Local static variables
interface = network.WLAN(network.STA_IF)

def iface(args):
    if len(args["interface"]) == 0:
        return """{"interface": ["%s"]}""" %("up" if interface.active() else "down")
    elif len(args["interface"]) > 1:
        return """{"interface error": ["too many arguments"]}"""
    
    if "up" in args["interface"]:
        interface.active(True)
    elif "down" in args["interface"]:
        interface.active(False)
    else:
        return """{"interface error": ["up/down"]}"""
    
    flags.updown = int(interface.active())
    return """{"interface": ["%s"]}""" %("up" if interface.active() else "down")
    
# Scan for access points
def scan(args):
    if len(args["scan"]) > 0:
        return """{"scan error": ["takes no arguments"]}"""
    
    if not flags.updown:
        return """{"scan error": ["interface down"]}"""
    
    # Scan for networks
    nets = interface.scan()
    
    list = []
    for ssid, bssid, channel, rssi, authmode, hidden in nets:
        list.append(ssid.decode("utf-8"))
    
    jstr = """{"ssid": ["""
    for name in list:
        jstr += """"%s", """ %(name)
    jstr = jstr[:-2]
    jstr += "]}"
    
    return jstr
    
# Connect to access point
# TODO: Error conditions
def connect(args):
    # Filter correct argument input
    if not len(args["connect"]) == 2:
        return """{"connect error": ["takes 2 arguments"]}"""
    
    # Check interface flag
    if not flags.updown:
        return """{"connect error": ["interface down"]}"""
    
    # Connect to Access Point
    try:
        if interface.isconnected():
            disconnect()
            sleep(1)
        interface.connect(args["connect"][0], args["connect"][1])
    except:
        return """{"connect error": ["could not parse"]}"""
    
    # Wait for connection or timeout
    counter = 0
    timeout = 15
    while not interface.isconnected():
        sleep(0.1)
        counter += 1
        if counter >= timeout*10:
            break
        elif interface.status() == 2:
            break
        elif interface.status() == 3:
            break
    
    flags.online = int(interface.isconnected())
    # Assemble response & return
    return """{"connect": ["%d", "%s"]}""" %(interface.status(),str(interface.ifconfig()[0]))

def disconnect():
    interface.disconnect()
    flags.online = interface.isconnected()
    return """{"connect": ["%d", "%s"]}""" %(interface.status(),str(interface.ifconfig()[0]))
