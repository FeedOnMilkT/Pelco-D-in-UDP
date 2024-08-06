import socket
import time


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
}
  

class UDPCommunication:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.ip, self.port)
        self.frame = Frame()

    
    def send(self, message):
        print(f"Sending: {message}")
        sent = self.sock.sendto(message, self.server_address)

    def move_in_direction(self, direction, pan_speed = 0x00, tilt_speed = 0x00):
        command = self.frame.command_construct(direction, pan_speed, tilt_speed)
        self.send(command)

    def move_to_position(self, direction , angle = 0x00):
        angle = angle * 100
        pan_position = (angle >> 8) & 0xFF
        tilt_position = angle & 0xFF
        command = self.frame.command_construct(direction, pan_position, tilt_position)
        self.send(command)
    
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


if __name__ == "__main__":
    ip = "192.168.1.100"
    port = 6666
    udp = UDPCommunication(ip, port)
    #udp.move_in_direction("right", 0x09, 0x00)
    udp.move_to_position("vertical", 30)
    time.sleep(1)
    udp.move_to_position("horizontal", 100)
    time.sleep(5)
    # udp.stop()

