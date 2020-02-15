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

# ----------------------------------------------
# pwm setup
# define some pwm value
motor_stop = 360
motor_forward = 600
motor_back = 335
servo_mid = 400
servo_left = 510 #460
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

def udpInit(host,port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    message = 'This is the message.  It will be repeated.'

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    print("server bind to: " ,host , port)

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
    # [290,400,510] [-32767 ,32767]
    value = (value/32767)*(100) + 400
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
    if("on_down_arrow_release" in data): # motor back
       #motorControl(data["on_L2_press"])
       motorControl(motor_stop)
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
s = udpInit("localhost",5555)
pwm = pwmInit()


# ----------------------------------------------
# UDP receive data
while True:
    data, address = s.recvfrom(4096)
    if(data):
        print(data)
        data = json.loads(data.decode())
        # process the data to see what command is
        #TODO : going backward
        parseCmd(data)








