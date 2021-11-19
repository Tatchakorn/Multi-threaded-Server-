#! /usr/bin/python3

"""
Handles connection between server and client
"""

import socket
import struct
from typing import Union, Tuple


def get_ip() -> Tuple[str, int]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


# PORT = 5050
PORT = 5052
HOST_NAME = socket.gethostname()
# SERVER_ADDR = socket.gethostbyname(HOST_NAME)
SERVER_ADDR = get_ip()

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

# Multicast group addresses are in the reserved 
# range (224.0.0.0~230.255.255.255).

def multicast_send():
    message = 'very important data'
    multicast_group = ('224.3.29.71', 10000)
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block indefinitely when
    # trying to receive data.
    sock.settimeout(0.2)
    # Set the time-to-live for messages to 1 so they do not go 
    # past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 
    ttl)
    try:
        # Send data to the multicast group
        print('sending "%s"' % message)
        sent = sock.sendto(message.encode(), multicast_group)
        
        # Look for responses from all recipients
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received "%s" from %s' % (data, server))
    finally:
        print('closing socket')
        sock.close()

def example_multicast_receive():
    multicast_group = '224.3.29.71'
    server_address = ('', 10000)
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to the server address
    sock.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sl', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    # Receive/respond loop
    # while True:
        # logger.info('\nwaiting to receive message')
        # data, address = sock.recvfrom(1024)
        # logger.info(f'received {len(data)} bytes from {address}')
        # logger.info(str(data))
        # logger.info(f'sending acknowledgement to {address}')
        # sock.sendto(('ack').encode(), address)