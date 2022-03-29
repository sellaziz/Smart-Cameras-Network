#!/usr/bin/env python3

import socket
from comm_config import read_config

def client_send_message(hostname, port, buffersize, message):
    """
    Send simple message to host.

    Args:
        host: The server's hostname.
        port: The port used by the server.
        buffersize: size of buffer.
        message: string.

    Returns:
        void.
    """

    host = socket.gethostbyname(hostname)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Trying to connect to {hostname} {host}:{port}")
        s.connect((host, port))
        s.sendall(bytes(message, 'utf-8'))
        print("Message sent!")
        #data = s.recv(buffersize)

if __name__=="""__main__""":
    hostname, port, buffersize, client_name, client_orientation = read_config("example.ini")
    client_send_message(hostname, port, buffersize, "Hello World!")