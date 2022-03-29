import socketio
import socket
import sys

sio = socketio.Client()

def send_multiple_predictions():
    val=0
    while True:
        if val<3 :
            val=val+1
        else:
            val=0
        # print("update_prediction", {'prediction': val, 'id':0})
        # sio.emit("update_prediction", {'prediction': val, 'id':0})
        send_prediction(0, val, 80)
        sio.sleep(5)

def send_prediction(id, pred, accuracy=10):
    example_labels=["shirt", "coat", "dress"]
    if pred>=3:
        pred=0
    sio.emit("update_prediction", {'prediction': example_labels[pred], 'id': id, 'accuracy': accuracy})

@sio.event
def connect():
    print('connection established')
    sio.start_background_task(send_multiple_predictions)


@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://'+'localhost'+':' + str(5000))
# send_prediction()