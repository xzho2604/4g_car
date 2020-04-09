import cv2
import io
import socket
import struct
import time
import pickle
import zlib

import numpy as np

bridgeSever = '3.104.231.53'
port = 8485

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = ("tcp://0.tcp.au.ngrok.io",15472)
server_address = (bridgeSever,port)

cam = cv2.VideoCapture(0)
cam.set(3, 320);
cam.set(4, 240);

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
img_counter = 0

while True:
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result, frame = cv2.imencode('.jpg', frame, encode_param)

    data = pickle.dumps(frame, 0)
    size = len(data)

    print("{}: {}".format(img_counter, size))
    client_socket.sendto(struct.pack(">L", size) + data,server_address)

    img_counter += 1

cam.release()
