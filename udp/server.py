import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib


def udpInit(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host,port)
    sock.bind(server_address)
    print("server bind to ", host, port)

    return sock


HOST=''
PORT=8485

s = udpInit(HOST,PORT)
print('Socket created')

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += s.recvfrom(40960)[0]

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += s.recvfrom(40960)[0]
        print("data len:",len(data))
    frame_data = data[:msg_size]
    print("final farm len: ",len(frame_data))
    data = data[msg_size:]
    frame= pickle.loads(frame_data)
    #print(frame)

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
