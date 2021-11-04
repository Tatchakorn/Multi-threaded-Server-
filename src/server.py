#! /usr/bin/python3

"""
Distributed Systems Assignment #2 
Multi-threaded Server
Author: Tatchakorn Saibunjom
"""

import threading
import socket
import sys
import logging
import json
from queue import Queue
from typing import Callable, List, Tuple, Union

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

# -----** Critical Data **-----||
global_data = [0] * 10
# ||-----** Critical Data **-----

writer_q = Queue()
lock = threading.Lock()
DO_NOTHING = 2_000_000

try:
    server = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        )
    server.bind(ADDR)

except socket.error as e:
    logger.error(f'Fail to create a socket: {e}')
    sys.exit()


def select_query(op: str, n: int) -> Union[Callable[[str], bool], bool]:
    if op == '>':       
        return lambda x: x > n
    elif op == '>=':    
        return lambda x: x >= n
    elif op == '<':     
        return lambda x: x < n
    elif op == '<=':    
        return lambda x: x <= n
    elif op == '=':     
        return lambda x: x == n
    elif op == '%':
        return lambda x: x % n == 0
    else: 
        return False 


def read(cond: str = '') -> List[int]:
    if cond == '': # just read -- for testing purpose
        return global_data
    op, n = cond.split()
    # Perform a busy loop incrementing a local variable from 0 to 2,000,000
    local_var = 0
    for _ in range(DO_NOTHING): local_var += 1
    
    select_cond = select_query(op, int(n))
    if select_cond is False:
        return 'Invalid request!'
    try:
        data = list(filter(select_cond, global_data))
    except ZeroDivisionError:
        return 'Division by zero!'
    logger.info(f'[READ] "{cond}" : {data}')
    return data


def write(values: List[int]) -> None:
    global global_data 
    # Perform a busy loop incrementing a local variable from 0 to 2,000,000
    local_var = 0
    for _ in range(DO_NOTHING): local_var += 1
    # THESE DO NOT WORK !!
    # global_data = values
    global_data = [0] * 10
    # for i in values: 
    #     global_data.append(i)
    for i, val in enumerate(values): 
        global_data[i] = val
    logger.info(f'[WRITE] {global_data}')


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    logger.info(f'[NEW CONNECTION] {addr} connected.')

    while True:
        msg = receive(conn)
        logger.info(f'[REQUEST] from {addr}: {msg}')
        msg = json.loads(msg)
        req_type = msg.get('req_type')
        
        if req_type == DISCONNECT_MESSAGE:
            break

        if req_type == 'write':
            writer_q.put(1)
            # -----** Critical Section **----- ||
            with lock:
                write(msg.get('data'))
            # || -----** Critical Section **-----
            writer_q.get()
            writer_q.task_done()
            payload = json.dumps({'req_': 'write', 'res_': global_data})
            send(conn, bytes(payload, encoding=CODEC_FORMAT))
        
        if req_type == 'read':
            writer_q.join()
            req_cond = msg.get('data')
            data = read(req_cond)
            payload = json.dumps({'req_': req_cond, 'res_': data})
            send(conn, bytes(payload, encoding=CODEC_FORMAT))        
    conn.close()


def start_server() -> None:
    server.listen(1)
    logger.info(f'[LISTENING] on {SERVER_ADDR}')
    i = 0
    try:
        while True:
            conn, addr = server.accept()
            i += 1
            t = threading.Thread(name=f'handler_[{i}]', target=handle_client, args=(conn, addr))
            t.start()
            logger.info(f'[ACTIVE CONNECTION] {threading.active_count() - 1}') # exclude main thread
    finally:
        conn.close()

if __name__ == '__main__':
    logger.info('[SERVER STARTED]')
    start_server()