# mgs.py
# Message print or return module 
# Edit: 05/08/24
# by NAticHAJ

# Return error cause
def err(cause):
    return """{"error": ["%s"]}""" %(cause)

# Return end cause
def end(cause):
    return """{"ending": ["%s"]}""" %(cause)

# Return exitcode
def ecd(code):
    return """{"exitcode": ["%s"]}""" %(code)