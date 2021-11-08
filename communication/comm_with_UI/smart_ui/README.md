# Usage
## Install Environment
```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Setup the environment
Find your IP address with the following command
```bash
hostname -I | awk '{print $1}'
```
Then edit the script app.py and socket_msg.py to use this address
app.py:
```python
socketio.run(app,host="YOUR_IP", port="A_PORT", debug=True)
```
socket_msg.py:
```python
sio.connect('http://'+'YOUR_IP'+':' + str(A_PORT))
```

## Run the script
```bash
python app.py
```


# Acknowledgment
[Tutorial](https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent)