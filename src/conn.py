#! /usr/bin/python3

"""
Handles connection between server and client
"""

import socket
from typing import Union

PORT = 5050
HOST_NAME = socket.gethostname()
SERVER_ADDR = socket.gethostbyname(HOST_NAME)
ADDR = (SERVER_ADDR, PORT)

HEADER_SIZE = 64 # 64-byte header -- specifying message length
CODEC_FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'disconnect'
REC_SIZE = 2048


def receive(conn: socket.socket) -> str:
    msg_len = conn.recv(HEADER_SIZE).decode(CODEC_FORMAT)
    if msg_len:
        msg_len = int(msg_len)
        msg = conn.recv(msg_len).decode(CODEC_FORMAT)
        return msg


def send(conn: socket.socket, msg: bytes, wait_response: bool = False) -> Union[None, str]:
    header = str(len(msg)).encode(CODEC_FORMAT)
    header += b' ' * (HEADER_SIZE - len(header)) # 64-byte padding
    conn.sendall(header)
    conn.sendall(msg)
    if wait_response:
        return receive(conn)