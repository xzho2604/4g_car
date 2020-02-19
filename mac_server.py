
import socket
import json

import time


def udpInit(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host,port)
    sock.bind(server_address)
    print("server bind to ", host, port)

    return sock

sock = udpInit("",8888)
while True:
    data,address = sock.recvfrom(4096)
    if(data):
        print("received: " , data, "; from: ", address)

        # send back the data to the sender
        message = "Hey greetings from the server!"
        sock.sendto(message.encode(), address)
        print("greetin sent")


