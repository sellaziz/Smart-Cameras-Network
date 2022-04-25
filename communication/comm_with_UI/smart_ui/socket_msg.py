import socketio
import socket
import sys
from datetime import datetime

port = '9000'
localhost = '10.29.226.123'

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
        example_labels=["shirt", "coat", "dress"]
        pred=val
        if pred>=3:
            pred=0
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        cam_id=0
        # predictions={"0":{'cam_id': cam_id, 'pred_idx': pred_idx,'pred_time':dt_string, 'prediction': example_labels[pred], 'accuracy': accuracy+val},
        accuracy=80
        predictions={0:{'cam_id': cam_id, 'pred_time':dt_string, 'prediction': example_labels[pred], 'accuracy': accuracy+val},
                     1:{'cam_id': cam_id, 'pred_time':dt_string, 'prediction': example_labels[pred], 'accuracy': accuracy+val+1}}
        send_prediction(predictions)
        sio.sleep(5)

def send_prediction(predictions):
    # sio.emit("update_prediction", {'prediction': example_labels[pred], 'id': id, 'accuracy': accuracy})
    sio.emit("update_prediction", predictions)

@sio.event
def connect():
    print('connection established')
    sio.start_background_task(send_multiple_predictions)


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://'+localhost+':' + str(port))
# send_prediction()
