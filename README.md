<h1>esp8266flow</h1>
<p></p>Web server w/ backend</p>

<b>NOTE: If main.py file is in the root directory of the micropython device, it will run on startup! Intended for UART operation</b>

>Launch main.py form REPL for testing
>
>In main Rx loop, enter any command in this format: {"command": ["arg1","arg2"]}
>
>Once flags permit, the server can be started: {"server": []}
>
>The main Rx loop can be ended with: {"end": []}

---

## [INSTALLING & RUN]

Download all files and directories in [Flow](/Flow/) onto the micropython device **~~(except main.py unless device is ready UART operation)~~** BUG: KEEP Pin 0 NC!

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

---

## [SERVER]
Once started, the server accepts requests on port 80

HTML and related files are stored and served internally

AJXA commands for external processing is Tx over UART or REPL

Backend is available at /default/FlowControl.html

---

## [FlowFiler]

Backend file manager for the http directory

![Flow Filer](/assets/FlowFiler.png)

Empty requests are served index.html from the http directory

If no file named index.html is found, a 404 page is served.

Use the file manager to get started!

<br>

### upload files, download files and delete files:

same name files are overwritten - NO WARNINGS

deleted files are deleted - NO BACKSIES

downloading files - as usual

---

## [COMMANDS]
<details>
    
<summary><h3>Rx loop commands</h3></summary>

|  Command  | Arguments | description |
|-----------|-----------|-------------|
| flags     |    0,1    | Device status |
| interface |    0,1    | Interface configuration |
| scan      |     0     | Scan for networks |
| connect   |     2     | Connect to network |
| disconnect|     0     | Disconnect form network |
| server    |     0     | Start the webserver |
| end       |     0     | End the Rx loop |

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
---

## [ARGUMENTS]

<details>
    
<summary><h3>Flags</h3></summary>

| Argument | Description |
|----------|----------------------------------------------|
|   NONE   |Returns all flags in this order:|
|  serial  |REPL / UART flag|
|  config  |Configuration file present|
|  rxloop  |Rx loop state|
|  updown  |STA interface state|
|  online  |Connection state|

</details>

<details>
    
<summary><h3>Interface</h3></summary>

|  Argument  | Description |
|------------|---------------|
|    NONE    |Interface state|
|     up     |Enable interface|
|    down    |Disable interface|

</details>

<details>
    
<summary><h3>Scan</h3></summary>

|  Argument  | Returns |
|------------|------------------|
|    NONE    |Available networks|

</details>

<details>
    
<summary><h3>Connect</h3></summary>

| Argument 1 | Argument 2 | Returns
|------------|------------|----------------|
|    SSID    |  PASSWORD  |Connection state|


Connection status:

        255: IF down
        0: Idle
        1: Connecting
            If 1 is returned, it might be hanging. Please retry!
        2: Authentication error
        3: SSID not found
        4: ???
        5: Connected


</details>

<details>
    
<summary><h3>Disconnect</h3></summary>

|  Argument  | Returns |
|------------|------------------|
|    NONE    |Connection state|

</details>

<details>
    
<summary><h3>Server</h3></summary>

|  Argument  | Description |
|------------|------------------|
|    NONE    |Start webserver|

**NOTE: Returning only when webserver terminates!**

</details>

<details>
    
<summary><h3>End</h3></summary>

|  Argument  | Description |
|------------|------------------|
|    NONE    |End main Rx loop|

</details>
