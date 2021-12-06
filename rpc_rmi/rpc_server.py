#! /usr/bin/python3
'''
Distributed Systems Assignment #4

1. Design a SciCalculator function and call it with RPC.
2. Design a SciCalculatorServer class to accept calculation 
requests from clients.
3. The both the function and server above should accept 
requests such as add, sub, mul, div, pow, sqr, log, sin, 
cos operations. Define remote interface if necessary.
4. Design a SciCalculatorClient class to invoke the remote 
operations in a loop until exist.

Author: Tatchakorn Saibunjom
'''

import sys
import logging
from typing import Callable, List, Union
from math import sqrt, log, sin, cos

import rpyc
from rpyc.utils.server import ThreadedServer

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'server.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)
number_t = Union[int, float]


class SciCalculatorServer(rpyc.Service):


    @staticmethod
    def select_op(op: str) -> Union[Callable[
        [number_t, number_t], number_t], 
        Callable[ [number_t], number_t], None]:
        if op == 'add':       
            return lambda a, b: a + b
        elif op == 'sub':    
            return lambda a, b: a - b
        elif op == 'mul':     
            return lambda a, b: a * b
        elif op == 'div':    
            return lambda a, b: a / b
        elif op == 'pow':
            return lambda n, pow: n ** pow
        elif op == 'sqrt':
            return lambda n: sqrt(n)
        elif op == 'log':
            return lambda n, base: log(n, base)
        elif op == 'sin':
            return lambda n: sin(n)
        elif op == 'cos':
            return lambda n: cos(n)
        else: 
            return None
    

    def exposed_SciCalculator(self, op: str, operands: List[int]) -> Union[number_t, None]:
        
        exec = self.select_op(op)
        op_len = len(operands)
        if exec is None or not 0 < op_len < 3:
            logger.error(f'Invalid request!')
            return None
        try:
            if op_len == 1: # -- Unary
                return exec(operands[0])
            elif op_len == 2: # -- Binary
                return exec(operands[0], operands[1])
        except Exception as e:
            logger.error(f'Err: {e}')
            return None



if __name__ == '__main__':
    t = ThreadedServer(SciCalculatorServer, port=18861)
    t.start()