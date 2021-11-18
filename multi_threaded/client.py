#! /usr/bin/python3
"""
Handles client requests for multi-threaded server
"""

import socket
import logging
import json
import sys
from typing import List

from conn import (
    DISCONNECT_MESSAGE, CODEC_FORMAT,
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


def read_req(client: socket.socket, cond: str = '') -> List[int]:
    payload = json.dumps({'req_type': 'read', 'data': cond})
    response = send(client, bytes(payload, encoding=CODEC_FORMAT), wait_response=True)
    logging.info(f'[READ] {response}')


def write_req(client: socket.socket, data: List[int]) -> None:
    payload = json.dumps({'req_type': 'write', 'data': data})
    response = send(client, bytes(payload, encoding=CODEC_FORMAT), wait_response=True)
    logging.info(f'[WRITE] {response}')


def disconn_req(client: socket.socket) -> None:
    payload = json.dumps({'req_type': DISCONNECT_MESSAGE})
    send(client, bytes(payload, encoding=CODEC_FORMAT))
