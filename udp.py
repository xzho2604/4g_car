import os
import time
import struct
import time

import socket
import json

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("220.245.76.1",5555)

message  = " hello from the raspi!"
sock.sendto(message.encode(),server_address)

print("message sent to my mac: ",server_address)

'''
# receive feedback from the server
data,server_address = sock.recvfrom(4096)
if(data):
    print(data,server_address)
'''


