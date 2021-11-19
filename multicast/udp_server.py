#! /usr/bin/python3

import socket
import sys
import logging
from typing import Callable, Union
from pprint import pformat
from conn import (
    ADDR, CODEC_FORMAT,
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
    op, a, b = req.split()
    func = select_op(op)
    try:
        return func(int(a), int(b))
    except ZeroDivisionError as e:
        print(e)
        return False


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(ADDR)
    while True:
        
        logger.info('Wating...')
        data, addr = s.recvfrom(1024)
        logger.info(f'[REQUEST] from {addr} : {data}')
        result = str(exec(data.decode(CODEC_FORMAT)))
        s.sendto(bytes(result, encoding=CODEC_FORMAT), addr)
        if addr not in visited_addr:
            visited_addr[addr] = 1
        else:
            visited_addr[addr] += 1
        
        logger.info(pformat(visited_addr))
        


if __name__ == '__main__':
    try:
        logger.info('[SERVER STARTED]')
        start_server()
    except Exception as e:
        logger.error(e)
    finally:
        input('Press [ENTER]...')