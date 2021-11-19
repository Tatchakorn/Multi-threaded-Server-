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
    response = send(client, bytes(payload, encoding=CODEC_FORMAT), wait_response=True)
    logging.info(f'[req: {expr}] {response}')
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