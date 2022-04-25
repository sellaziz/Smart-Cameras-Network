from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import pandas as pd
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

port = '9000'
localhost = '10.29.226.123'

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'test', 'count': 'test'})

@socketio.event
def update_prediction(message):
    # print("update_prediction", {'cam_id': message['cam_id'], 'pred_idx': message['pred_idx'],'prediction': message['prediction'], 'accuracy': message['accuracy']})
    # session['receive_count'] = session.get('receive_count', 0) + 1
    df=pd.DataFrame({'cam_id': [0], 'pred_idx': [0],'prediction': ["shirt"], 'accuracy': [80]},
                    columns=['cam_id', 'pred_idx', 'prediction', 'accuracy', 'pred_time'])
    for pred_idx, prediction in message.items():
        cam_id=prediction["cam_id"]
        prediction.setdefault('pred_idx',pred_idx)
        series = pd.Series(prediction)
        # print(series)
        df=df.append(series,ignore_index=True)
    # df.drop(['cam_id'], axis=1)
    # print(df)
    df = df.iloc[1: , :]
    socketio.emit("update_predictions", {'cam_id': cam_id, 'pd_html': df.to_html()})
    # sio.emit("update_predictions", {'cam_id': message['cam_id'], 'pred_idx': message['pred_idx'],'pred_time':message['pred_time'],
                                    # 'prediction': message['prediction'], 'accuracy': message['accuracy']})
    # sio.emit("update_predictions", {'cam_id': message['cam_id'], 'pred_idx': message['pred_idx'],'prediction': message['prediction'], 'accuracy': message['accuracy']})
    # socketio.emit('update_predictions',
    #      {'prediction': message['prediction'], 'id': message['id'], 'accuracy': message['accuracy']})


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app,host=localhost, port=port, debug=True)
