# rxloop.py
# Receive command loop
# Edit: 06/08/24
# by NAticHAJ

import state
import trx
import rxp
import gc

# Variables
command = None
state.rxloop = 0

def run():
    state.rxloop = 1
    while state.rxloop:
        command = trx.rx()
        trx.tx(rxp.parse(command))
        gc.collect()
    trx.reset()