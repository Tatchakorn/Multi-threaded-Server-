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
    DISCONNECT_MESSAGE, CODEC_FORMAT, 
    ADDR, SEND_RECV_SIZE, MULTICAST_GROUP, 
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
    logger.info(f'[RECIEVE] {response}')
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


def multicast_receive(client: socket.socket):
    server_addr = ('', 10000)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(server_addr)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(MULTICAST_GROUP[0])
    mreq = struct.pack('4sl', group, socket.INADDR_ANY)
    client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    # Receive/respond loop
    while True:
        logger.info('[WAITING] to receive message')
        data, address = client.recvfrom(SEND_RECV_SIZE)
        logger.info(f'[RECEIVE] {len(data)} bytes from {address}')
        logger.info(str(data))
        logger.info(f'[ACK] to {address}')
        client.sendto(('ack').encode(CODEC_FORMAT), address)