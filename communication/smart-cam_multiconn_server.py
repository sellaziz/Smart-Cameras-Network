import eventlet
import socketio
import socket
from comm_config import read_config

hostname, port, buffersize, client_name, client_orientation = read_config("example.ini")
sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('Received data from {} {}'.format(sid, data))

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
