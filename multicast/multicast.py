#! /usr/bin/python3

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