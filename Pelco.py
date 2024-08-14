import socket
import time
import binascii
import threading
from concurrent.futures import ThreadPoolExecutor 

"""
def message_send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    
    print(f"Sending: {message}")
    sent = sock.sendto(message.encode(), server_address)
"""  
frame = {
    "sync_byte": 0xff,
    "address": 0x01,
    "command1": 0x00,
    "command2": 0x00,
    "data1": 0x00,
    "data2": 0x00,
    "checksum": 0x00
}

funnction_code = {
    "up": 0x08,
    "down": 0x10,
    "left": 0x04,
    "right": 0x02,
    "stop": 0x00,
    "horizontal": 0x4b,
    "vertical": 0x4d,
    "getVerDgr":0x53
}
  

class UDPCommunication:
    def __init__(self, ip, port, localIP = ""):   
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.ip, self.port)
        self.localIP = localIP
        self.sock.bind((self.localIP, self.port))
        self.frame = Frame()

    
    def send(self, message):
        print(f"Sending: {message}")
        sent = self.sock.sendto(message, self.server_address)

    def receiveOnce(self, localIP, localPort):
        print("Receiving")
        
        # s.bind((localIP, localPort))
        data, addr = self.sock.recvfrom(4096)
        data = binascii.hexlify(data)
        print(f"Received: {data}")

        if self.isDegreeResponse(data):
            return data
        else:
            return self.receiveOnce(localIP, localPort)



    def move_in_direction(self, direction, pan_speed = 0x00, tilt_speed = 0x00):
        command = self.frame.command_construct(direction, pan_speed, tilt_speed)
        self.send(command)
        #self.close()

    def move_to_position(self, direction , angle = 0x00):
        angle = angle * 100
        pan_position = (angle >> 8) & 0xFF
        tilt_position = angle & 0xFF
        command = self.frame.command_construct(direction, pan_position, tilt_position)
        self.send(command)
        #self.close()

    def getVerticalDgr(self, pan_speed = 0x00, tilt_speed = 0x00):
        command = self.frame.command_construct("getVerDgr", pan_speed, tilt_speed)
        self.send(command)
        #self.close()

    def isDegreeResponse(self, message):
        str_message = message.decode("utf-8")
        return str_message[6:8] == "59" or str_message[6:8] == "5b"
        
    def stop(self):
        self.move_in_direction("stop")
    
    def close(self):
        print("Closing socket")
        self.sock.close()


class Frame:
    def __init__(self) -> None:
        pass

    def command_construct(self, command2, data1, data2):

        #Command 2:

        if command2 not in funnction_code:
            print("Invalid command")
            return None    
        else:
            frame["command2"] = funnction_code[command2]

        frame["data1"] = data1
        frame["data2"] = data2
        frame["checksum"] = self.calculate_checksum()

        command = [frame["sync_byte"], frame["address"], frame["command1"], frame["command2"], frame["data1"], frame["data2"], frame["checksum"]]
        print(command)

        return bytes(command)
        

    def calculate_checksum(self):
        sum = (frame["address"] + frame["command1"] + frame["command2"] + frame["data1"] + frame["data2"])%256
        return sum

"""
    def get_command_code(self, command):
        command_code = {
            "UP": 0x08,
            "DOWN": 0x10,
            "LEFT": 0x04,
            "RIGHT": 0x02,
        }

        return command_code[command]
"""

def move(ip, port, vertical_degree, horizontal_degree):
    udp = UDPCommunication(ip, port)
    udp.move_to_position("horizontal", horizontal_degree)
    udp.move_to_position("vertical", vertical_degree)
    #udp.close()

def back_zero(ip, port):
    udp = UDPCommunication(ip, port)
    udp.move_to_position("horizontal", 0)
    udp.move_to_position("vertical", 0)
    #udp.close()

def sendVerticalDegreeCommand(ip, port):
    udp = UDPCommunication(ip, port)
    udp.getVerticalDgr()

def calculateDegree(message):
    str_message = message.decode("utf-8")
    HTimesAngle = int(str_message[8:12], 16)
    if HTimesAngle > 32767:
        HTimesAngle = HTimesAngle - 65536
    angle = HTimesAngle/100
    return angle 


def getVerticalDegree(ip, port, localIP, localPort):
    udp = UDPCommunication(ip, port)
    with ThreadPoolExecutor(max_workers=1) as executor:  
        future = executor.submit(udp.receiveOnce, localIP, localPort)  
  
        time.sleep(1)  
        udp.getVerticalDgr()  
  
        result = future.result()  
  
    # print("Threads finished")  
    # print("Received data:", result)  
    return calculateDegree(result)

    
    

if __name__ == "__main__":
    ip = "192.168.1.100"
    port = 6666
    degree = 45

    localIP = "192.168.1.243"
    localPort = 8080

    # move(ip, port, -17, 13)    
    # back_zero(localIP, port)
    # sendVerticalDegreeCommand(ip, port)
    print(getVerticalDegree(ip, port, localIP, port))


    """
    udp = UDPCommunication(ip, port)

    receiveThread = threading.Thread(target=udp.receiveOnce, args=(localIP, localPort))

    receiveThread.start()
    time.sleep(1)
    udp.getVerticalDgr()
    

    receiveThread.join()

    print("Threads finished")

"""