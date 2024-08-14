# Pelco-D Communication Protocol in Python 3

## Introduction:

This is a script form Pelco D command construction and  communication between PTZ and computer. The UDP protocol is used for communicatiion, you can change it into RS485 by yourself. The main functions of this script are Pelco-D command construction, command sending, and command receiving. It is able to control the PTZ to rotate to specific direction. You can also choose to control it to rotate a specific degree in specific degree. And it is able to get PTZ's information by sending commands, I write a vertical degree (elevation abgle) getter as an example.

## Functions

#### `frame` and `function_code`:

They are two dictionaries that contain the command information. I don't encourage you to change the content of  `frame` dictionary, it is the command format of the Pelco-D protocol message. The `function_code` dictionary is for storing the command code, which each of these code corresponds to a kind of command, such as "rotate up", "turn 30 degree ro right. If you have requirement that the dictionary not involved, you can add the command code here.

#### `class UDPCommunication`

This is a class for communication. I use UDP protocol in this script, and if your need use other protocol, you can try to rewrite this class to meet your requirement. 

This class implement the command sending and receiving function. Some specific control operations are also implemented in this class, such as `move_to_position`, which is for controling PTZ to rotate a spection degree in specific direction.

#### `class Frame`

It is for command construction. I have to note that this command construction method unable to determine on its own whether a byte in an instruction should be 0x00 or not. So you have to fimilar with the Pelco-D's message format.

#### `getVerticalDegree`

This method is able to receive the response after sending the command in same script through mutiple thread. 
