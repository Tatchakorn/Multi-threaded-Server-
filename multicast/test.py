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

import random
import socket
import threading
from typing import Union, Callable
from conn import ADDR
from client import (
    req, udp_req,disconn_req,
)

AVAILABLE_OPS = ('+', '-', '/', '*')


def rand_req() -> str:
    op = random.choice(AVAILABLE_OPS)
    a, b = (random.randint(0, 100), random.randint(0, 100))
    return f'{op} {a} {b}'



def test_tcp_req(num_client: int = 3):
    clients = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                for _ in range(num_client)]
    for client in clients: client.connect(ADDR)
    

    def run(client: socket.socket) -> None:
        for _ in range(5):
            req(client, rand_req())
    

    threads = [threading.Thread(name=f'client_[{i+1}]', target=run, args=(client,)) 
                for i, client in enumerate(clients)]
    for t in threads: t.start()
    for t in threads: t.join()
    for client in clients: disconn_req(client)


def test_udp_req(num_client: int = 3):
    clients = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
                for _ in range(num_client)]
    
    def run(client: socket.socket) -> None:
        for _ in range(5):
            udp_req(client, rand_req())

    threads = [threading.Thread(name=f'client_[{i+1}]', target=run, args=(client,)) 
                for i, client in enumerate(clients)]
    for t in threads: t.start()
    for t in threads: t.join()

if __name__ == '__main__':
    try:
        test_udp_req(5)
    except Exception as e:
        print(e)
    finally:
        input('Press [ENTER]...')