"""
change the pip install pyPS4Controller modeul in:
/usr/local/lib/python3.5/dist-packages/pyPS4Controller

controller interface:
-----------------------
on_R3_right: left to right range: [-32767,32767]
on_L2_press: pressing down range: [-32431 ,32767]
             depend on the releasing speed the lower can be
             -20945 one fast release

controller protocol:
-----------------------

Motor and servo control:
-----------------------
max pulxe lenght of 4096
- servo control
    pwm.set_pwm(1,0,servo_mid)
- Motor control
    pwm.set_pwm(1,0,servo_forward)

"""


import socket
import json

#import RPI.GPIO as GPIO
import time
import Adafruit_PCA9685

from flask import Flask
from flask import jsonify
from flask import request

# ----------------------------------------------
# pwm setup
# define some pwm value
motor_stop = 360
motor_forward = 600
motor_back = 320
servo_mid = 408
servo_left = 526 #460
servo_right = 290 # 350
# --------------------------------------------
# setting up socket connection
def tcpInit(host,port):
    # set up the network connection
    # init the connection
    host = ''        # Symbolic name meaning all available interfaces
    port = 5555     # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print(host , port)

    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    return s

# set up the initial connection with the host using udp
def udpInit(host,port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    print("server bind to: " ,host , port)

    '''
    #----------------------------------------
    # send initial shaske message for client to get the
    # server address for communication
    message="server init handshake!"
    sock.sendto(message.encode(),("203.194.11.102",8888))
    print("sent server init handshake")

    #----------------------------------------
    '''

    return sock


def pwmInit():
    # init the PCA9685 using the default address(0x40)
    pwm = Adafruit_PCA9685.PCA9685()
    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)
    print('Start listening to commnand')

    return pwm

# some help functions for seting pwm
def motorForward(value):
    # modulise the data to mactch the pwm range
    # [360,600] [-32767 ,32767]
    value = (value/32767 + 0.5)*(600-360) + 480
    pwm.set_pwm(0,0,int(value))

def motorControl(value):
    pwm.set_pwm(0,0,value)

def servoTurn(value):
    # [290,408,526] [-32767 ,32767]
    value = (-value/32767)*(118) + 408
    print("Turinig: ",int(value))
    pwm.set_pwm(1, 0, int(value))

def servoControl(value):
    pwm.set_pwm(1, 0, value)

def motorBack(value):
    pwm.set_pwm(0,0,value)

# given the data received from the socket parse the right command
def parseCmd(data):
    if("on_L2_press" in data): # goingforward
       motorForward(data["on_L2_press"])
       #motorControl(motor_forward)
    if("on_L2_release" in data): # motor stop
       #motorControl(data["on_L2_press"])
       motorControl(motor_stop)
    if("on_down_arrow_press" in data): # motor back
       #motorControl(data["on_L2_press"])
       motorControl(motor_back)
       #print("pressed down!!!!")
    if("on_down_arrow_release" in data): # motor back
       #motorControl(data["on_L2_press"])
       motorControl(motor_stop)
       #print("released down!!!!")
    if("on_R3_left" in data): # turn left
       servoTurn(data["on_R3_left"])
       #servoControl(servo_left)
    if("on_R3_right" in data): # turn right
       servoTurn(data["on_R3_right"])
       #servoControl(servo_right)
    if("on_R3_rest" in data): # server center
       #servoControl(servo_stop)
       servoControl(servo_mid)

def tcpListen():
    # start the listening loop for control command
    while True:
        try:
            data = conn.recv(1024)
            data = data.decode("UTF-8");
            # if there is data
            # data will the format of dict{cmd_str:value}
            if(data):
                # {on_R3_left:value} ,{on_R3_right:value},{on_R3_rest:True}
                # {on_L2_press:value}, {on_L2_release:True}

                print(data)
                data = json.loads(data)
                # process the data to see what command is
                #TODO : going backward
                parseCmd(data)

        except socket.error:
            print("Error Occured.")
            break

    conn.close()

# ----------------------------------------------
# init socket connection
pwm = pwmInit()


'''
s = udpInit("",8888)
# ----------------------------------------------
# UDP receive data
while True:
    data, address = s.recvfrom(4096)
    if(data):
        print("client got:",data)
        try:
            data = json.loads(data.decode())
        except:
            continue
        # process the data to see what command is
        #TODO : going backward
        parseCmd(data)


'''
app = Flask(__name__)

# receive http request
@app.route('/', methods = ['POST'])
def receiveCmd():
    cmd = request.get_json()
    print("received :", cmd)
    parseCmd(cmd)

    return "Roger"


if __name__ == "__main__":
    app.run(debug=True)





