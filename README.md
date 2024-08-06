# Pelco-D-in-UDP
It is a simple Python 3 script for encoding and sending pelco-d command use UDP. 

# Introduction:
Pelco-D is a communication protocol for PTZ camera control. This project is a simple Python3 script for you to control PTZ or similar equipment. This script implements some simple countrol method such as "UP", "Down", or rotate in specific degree. You can also add new command in `function_code` dictionay to meet your requirment.

The communication protocol is UDP, which uses RJ45 internet port to transmit information. You can also change it into Modbus protocol.

You have to be familiar with the Pelco-D protocol message format, because this script unable to determine which byte should be 0x00 and which should be a specific value. All improvement to yhis script are welcome.
