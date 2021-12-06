import logging
import sys
from typing import Callable, List, Union
from math import sqrt, log, sin, cos

import Pyro5.api


LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'client.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)
number_t = Union[int, float]


@Pyro5.api.expose
class SciCalculatorServer:
    
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
    

    def calc(self, op: str, operands: List[int]) -> Union[number_t, None]:
        
        exec = self.select_op(op)
        op_len = len(operands)
        if exec is None or not 0 < op_len < 3:
            logger.error(f'Invalid request!')
            return None
        try:
            if op_len == 1:     # -- Unary
                return exec(operands[0])
            elif op_len == 2:   # -- Binary
                return exec(operands[0], operands[1])
        except Exception as e:
            logger.error(f'Err: {e}')
            return None


if __name__ == '__main__':
    Pyro5.api.start_ns()
    daemon = Pyro5.server.Daemon()              # make a Pyro daemon
    ns = Pyro5.api.locate_ns()                  # find the name server
    uri = daemon.register(SciCalculatorServer)  # register the greeting maker as a Pyro object
    ns.register('SciCalculator', uri)           # register the object with a name in the name server
    logger.info('[REMOTE OBJECT READY]')
    daemon.requestLoop()                        # start the event loop of the server to wait for calls