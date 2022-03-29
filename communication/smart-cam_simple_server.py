#!/usr/bin/env python3

import socket
from comm_config import read_config

def client_send_message(hostname, port, buffersize):
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
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(buffersize)
                if not data:
                    break
                print("Received", repr(data))

if __name__=="""__main__""":
    hostname, port, buffersize, client_name, client_orientation = read_config("example.ini")
    client_send_message(hostname, port, buffersize)