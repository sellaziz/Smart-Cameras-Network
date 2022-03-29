import socketio
import socket
import sys
from comm_config import read_config

hostname, port, buffersize, client_name, client_orientation = read_config("example.ini")
host = socket.gethostbyname(hostname)
message_arg=sys.argv[1]
sio = socketio.Client()

def send_sensor_readings():
    while True:
        sio.emit("my_message", {'mess': message_arg})
        sio.sleep(5)

@sio.event
def connect():
    print('connection established')
    sio.start_background_task(send_sensor_readings)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://'+host+':' + str(port))
sio.wait()