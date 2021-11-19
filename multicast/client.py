#! /usr/bin/python3
"""
Handles client requests for the server
"""

import socket
import logging
import json
import sys
import struct
from typing import List, Union

from conn import (
    DISCONNECT_MESSAGE, CODEC_FORMAT, ADDR, 
    send,
)

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'client.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)


def req(client: socket.socket, expr: str = '') -> str:
    payload = json.dumps({'req': expr})
    logger.info(f'[SEND] {expr}')
    response = send(client, bytes(payload, encoding=CODEC_FORMAT), wait_response=True)
    logger.info(f'[RECIEVE] {response} from {addr}')
    return response


def disconn_req(client: socket.socket) -> None:
    payload = json.dumps({'req': DISCONNECT_MESSAGE})
    send(client, bytes(payload, encoding=CODEC_FORMAT))


def udp_req(client: socket.socket, expr: str) -> str:
    client.sendto(expr.encode(CODEC_FORMAT), ADDR) # encode first
    logger.info(f'[SEND] {expr}')
    response, addr = client.recvfrom(1024)
    response = response.decode(CODEC_FORMAT)
    logger.info(f'[RECIEVE] {response} from {addr}')
    return response


def multicast_receive():
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
    while True:
        logger.info('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        logger.info(f'received {len(data)} bytes from {address}')
        logger.info(str(data))
        logger.info(f'sending acknowledgement to {address}')
        sock.sendto(('ack').encode(), address)