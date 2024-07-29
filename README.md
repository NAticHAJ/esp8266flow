<h1>esp8266flow</h1>
<p></p>Web server w/ backend</p>
![Flow Filer](https://github.com/user-attachments/assets/62e82e44-5789-45bb-bf61-fb8769428e3e)

<b>NOTE: If main.py is the root dir of the micropython device, the file will run on startup! Only for standalone operation</b>

>Launch main.py form REPL for testing
>
>In main Rx loop, enter any command in this format: {"command": ["arg1","arg2"]}
>
>Once flags permit, the server can be started: {"server": []}
>
>The main Rx loop can be ended with: {"end": []}

---

## [INSTALLING & RUN]

Download all files and directories onto the micropython device **(except main.py unless device is ready for standalone operation)**

Run main.py from REPL capable IDE so that it runs on the micropython device

---

## [MAIN ENTRY]

1. On start, PIN 0 is checked ( default is HIGH )
    - LOW -> UART
    - HIGH -> REPL ( USB )
2. Flags are updated
    - online
    - updown
    - serial
3. Optionally a configuration is loaded ( NOT FUNCTIONAL )
4. Main Rx loop starts and takes commands over REPL ( USB ) or UART


## [COMMANDS]
<details>
<summary><h3>Rx loop commands</h3></summary>
|  Command  | Arguments | description |
|-----------|-----------|-------------|
| flags     |    0,1    | device status |
| interface |    0,1    | interface configuration |
| scan      |     0     | scan for networks |
| connect   |     2     | connect to network |
| disconnect|     0     | disconnect form network |
| server    |     0     | start the webserver |
| end       |     0     | end the Rx loop |
</details>

Enter a command ( and args ) in JSON format. Example:
```
[RxLoop] Type here: {"flags":[]}
```
Device reponds in same format. Example:
```
{"flags": ["1", "0", "1", "1", "1"]}
```
The interface must be up to scan for networks:
```
[RxLoop] Type here: {"flags": ["updown"]}
{"updown": ["1"]}
```


Flags:
{"flags":[]}
    returns all flags
    flags in order and as single flag output by arg:
    ["serial"]
    ["config"]
    ["rxloop"]
    ["updown"]
    ["serial"]
    
Interface:    
{"interface": []}
    returns interface state
    args to change state:
    ["up"]
    ["down"]

Scan:
{"scan":[]}
    returns array of found networks in JSON format. Takes no args
    {"ssid": ["some network", "some other network"]}

Connect:
{"connect":["ssid","presharedkey"]}
    returns connection status as JSON array object. Takes 0 or 2 args
    {"connect": ["5", "192.168.1.105"]}
    args are self explanatory
    return states:
        255: IF Down
        0: Idle
        1: Connecting NOTE: If 1 is returned, it might be hanging. Please retry!
        2: Authentication error
        3: SSID not found
        4: ???
        5: Connected

Disconnect:
{"disconnect": []}
    returns connection status as JSON array object. Takes no args
    
Server:
{"server": []}
    starts webserver returning only when webserver terminates. Take no args
    {"exitstatus": ["condition"]}

End:
{"end": []}
    end the main Rx loop. Takes no arguments


[SERVER]
Once started, the server accepts requests on port 80
HTML and related files are stored and served internally
AJXA commands for external processing is Tx over UART or REPL
Backend is available at /default/FlowControl.html

[FlowFiler]
file manager for the http directory
empty requests return /http/index.html
any file named index.html is retuned
else the 404 error page is returned

upload files, download files and delete files:
same name files are overwritten - NO WARNINGS
deleted files are deleted - NO BACKSIES
downloading files - as usual


