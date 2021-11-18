#! /usr/bin/python3
"""
Distributed Systems Assignment #3

Assignment 3: Python TCP, 
UDP and Multicasting
1. Try out the Python TCP/UDP client-server and 
multithreaded server examples. Correct any problem.
2. Try out the Python multicast example. Correct any 
problem.
3. Write simple TCP/UDP calculate servers that accept 
simple arithmetic computing requests in prefix form such 
as “+ 4 5” and send back the result. Write 
corresponding clients to test them.
4. Using Python multicast, write a client that sends out 10 
messages to a multicast group and another client that 
receives the messages. Give a few tests to see if all 
messages were correctly received.

"""
import socket
import struct
import random
import sys
from typing import Union, Callable

available_ops = ('+', '-', '/', '*')
test_req = '+ 4 5'


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


def rand_req() -> str:
    op = random.choice(available_ops)
    a, b = (random.randint(0, 100), random.randint(0, 100))
    return f'{op} {a} {b}'


def test() -> None:
    for _ in range(100_000):
        req = rand_req()
        op, a, b = req.split()
        print(f'req: {op} {a} {b}')
        
        func = select_op(op)
        try:
            res = func(int(a), int(b))
        except ZeroDivisionError as e:
            print(e)
            break
        print(res)


if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print(e)
    finally:
        input('Press [ENTER]...')