# trx.py
# Transmit and receive module
# Edit: 05/08/24
# by NAticHAJ

import state
from machine import UART
import json

# Setup UART
if not state.serial:
    os.dupterm(None, 1)
    port = UART(0, 115200)
    port.init(115200, bits=8, parity=None, stop=1)
    
# Receive data
def rx():
    # USB / REPL
    if state.serial:
        while True:
            try:
                return json.loads(input("Type here: "))
            except:
                print("""{"json": ["malformed"]}""")
                continue
    # UART
    else:
        while port.any() < 1:
            continue
        return json.loads(port.read())

# Transmit data
def tx(data):
    if state.serial:
        print(data)
    else:
        port.write(data)

# Convert to JSON
def enc(jstr):
    return json.loads(jstr)

# Reset serial port
def reset():
    if not state.serial:
        os.dupterm(port, 1)