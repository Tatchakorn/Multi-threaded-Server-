#! /usr/bin/python3

from typing import Callable, Union
from math import sqrt, log, sin, cos
"""
Distributed Systems Assignment #4
1. Design a SciCalculatorServer class to accept calculation 
requests from clients.
2. The server should accept requests such as add, sub, mul, 
div, pow, sqr, log, sin, cos operations. Define remote 
interface if necessary.
3. Design a SciCalculatorClient class to invoke the remote 
operations in a loop until exist

Author: Tatchakorn Saibunjom
"""

import Pyro5.api

number_t = Union[int, float]
def select_op(op: str) -> Union[
    Callable[
        [number_t, number_t], number_t
        ],
    Callable[
        [number_t], number_t
        ], bool
    ]:
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
        return False

@Pyro5.api.expose
class GreetingMaker:
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
            "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)

daemon = Pyro5.api.Daemon()             # make a Pyro daemon
uri = daemon.register(GreetingMaker)    # register the greeting maker as a Pyro object

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()                    # start the event loop of the server to wait for calls