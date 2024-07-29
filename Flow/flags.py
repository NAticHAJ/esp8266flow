#### FLAGS ####
serial = 0
config = 0
rxloop = 0
updown = 0
online = 0
###############

def get(args):
    if len(args["flags"]) == 0:
        return """{"flags": ["%d", "%d", "%d", "%d", "%d"]}""" %(serial,config,rxloop,updown,online)
    elif len(args["flags"]) > 1:
        return """{"flags error": ["too many arguments"]}"""
    
    switch = args["flags"][0]
    if switch == "serial":
        return """{"serial": ["%d"]}""" %(serial)
    elif switch == "config":
        return """{"config": ["%d"]}""" %(config)
    elif switch == "rxloop":
        return """{"rxloop": ["%d"]}""" %(rxloop)
    elif switch == "updown":
        return """{"updown": ["%d"]}""" %(updown)
    elif switch == "online":
        return """{"online": ["%d"]}""" %(online)
    elif switch == "help":
        return """{"flags": ["serial", "config", "rxloop", "updown", "online"]}"""
    else:
        return """{"flags error": ["not a key"]}"""