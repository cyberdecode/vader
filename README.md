# vader.py
Tkinter Front-End for the Empire RESTful API

Current release built on Kali GNU/Linux Rolling 2018.1 with Python 2.7.14+.

Support for Empire RESTful API for Empire version 2.5.

NOTE: Requires xterm for the embedded shell.

1. Start the Empire RESTful API instance:
* This will start the API service, and start an Empire shell

/opt/Empire: # ./empire --rest --username empire --password empire

2. Start the GUI:

/opt/empireGUI: # python vader.py
