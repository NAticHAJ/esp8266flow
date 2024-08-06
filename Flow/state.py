# state.py
# 03/08/24
# by NAticHAJ

from machine import Pin
from msg import err

from os import statvfs
from gc import mem_free
from gc import mem_alloc

# State variables
serial = Pin(4, Pin.IN, Pin.PULL_UP).value()
online = 0
updown = 0
rxloop = 0

erstat = 0

def flags(args):
    if len(args) == 0:
        return """{"flags": ["%d", "%d", "%d", "%d"]}""" %(serial,rxloop,updown,online)
    else:
        return err("too many arguments")
    
def usage():
    memFree = mem_free()
    memUsed = mem_alloc()
    memTot = memFree + memUsed
    mempct = int((memUsed / memTot)*100)

    dsk = statvfs("/")
    dskTot = round((dsk[1] * dsk[2])/1024,2)
    dskFree = (dsk[0] * dsk[3])/1024
    dskUsed = round(dskTot - dskFree,2)
    dskpct = int((dskUsed / dskTot)*100)
    
    # RSSI ?
    
    # 
    
    return """{"memtot": "%s", "memuse": "%s", "mempct": "%d%%", "dsktot": "%s", "dskuse": "%s", "dskpct": "%d%%"}""" %(str(memTot), str(memUsed),mempct, str(dskTot), str(dskUsed),dskpct)