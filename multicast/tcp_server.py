#! /usr/bin/python3

import threading
import socket
import sys
import logging
import json
from pprint import pformat
from typing import Callable, Tuple, Union

from conn import (
    ADDR, DISCONNECT_MESSAGE, SERVER_ADDR, CODEC_FORMAT,
    send, receive,
)

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'server.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)

# ||--- Global

visited_addr = {}

# ---||
lock = threading.Lock()


def select_op(op: str) -> Union[Callable[[int, int], Union[int, float]], bool]:
    if op == '+':       
        return lambda a, b: a + b
    elif op == '-':    
        return lambda a, b: a - b
    elif op == '*':     
        return lambda a, b: a * b
    elif op == '/':    
        return lambda a, b: a / b
    elif op == '%':
        return lambda a, b: a % b
    else: 
        return False


def exec(req: str) -> Union[int, float, bool]: 
    try:
        op, a, b = req.split()
        func = select_op(op)
        return func(int(a), int(b))
    except ZeroDivisionError as e:
        print(e)
        return False


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    logger.info(f'[NEW CONNECTION] {addr} connected.')

    while True:
        msg = receive(conn)
        logger.info(f'[REQUEST] from {addr}: {msg}')
        msg = json.loads(msg)
        req = msg.get('req')
        
        if req == DISCONNECT_MESSAGE:
            break
        
        with lock:
            if addr not in visited_addr:
                visited_addr[addr] = 1
            else:
                visited_addr[addr] += 1

        # logger.info(pformat(visited_addr))
        res = exec(req)
        if res is not False:
            payload = json.dumps({'res_': res})
            send(conn, bytes(payload, encoding=CODEC_FORMAT))
        else:
            payload = json.dumps({'res_': 'Failed!'})
            send(conn, bytes(payload, encoding=CODEC_FORMAT))
    conn.close()


def start_server() -> None:
    server.listen(1)
    logger.info(f'[LISTENING] on {SERVER_ADDR}')
    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
            logger.info(f'[ACTIVE CONNECTION] {threading.active_count() - 1}') # exclude main thread
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        server = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            )
        server.bind(ADDR)
    except socket.error as e:
        logger.error(f'Fail to create a socket: {e}')
        sys.exit()
    
    try:
        logger.info('[SERVER STARTED]')
        start_server()
    finally:
        input('Press [ENTER]...')