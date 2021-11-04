#! /usr/bin/python3

import socket
import random
import threading
import time

from client import (
    read_req, 
    write_req, 
    disconn_req, 
    )

from conn import ADDR

z0_to_million = iter(range(0, 1_000_000, 10))
lock = threading.Lock()
available_ops = ('>', '>=', '<', '<=', '=', '%')
current_min_val = 0

def rand_read(client: socket.socket) -> None:
    rand_op = random.choice(available_ops)
    n = current_min_val + random.randint(0, 5)
    cond = f'{rand_op} {n}'
    read_req(client, cond)


def rand_write(client: socket.socket) -> None:
    rand_list = [random.randint(0, 10) for _ in range(10)]
    write_req(client, rand_list)


def not_rand_write(client: socket.socket) -> None:
    global current_min_val
    with lock:
        current_min_val = start_n = next(z0_to_million)
    rand_list = [i for i in range(start_n, start_n + 10)]
    write_req(client, rand_list)


def test_single_client() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(ADDR)
    for _ in range(100):
        rand_op = random.choice(available_ops)
        n = random.randint(0, 10)
        cond = f'{rand_op} {n}'
        rand_list = [random.randint(0, 10) for _ in range(10)]
        rand_read(client, cond)
        rand_write(rand_list)
    disconn_req(client)


def test_multiple_clients(num_client: int = 2, num_req: int = 10):
    clients = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(num_client)]
    for client in clients: client.connect(ADDR)
    
    reqs = [rand_read, rand_write]
    
    def run(client: socket.socket):
        for _ in range(num_req):
            rand_req = random.choice(reqs)
            rand_req(client)
            time.sleep(1)
    
    threads = [threading.Thread(name=f'client_[{i+1}]', target=run, args=(client,)) 
                for i, client in enumerate(clients)]
    
    for t in threads: t.start()
    for t in threads: t.join()
    for client in clients: disconn_req(client)


def test_read_and_write_clients(num_reader: int = 1, 
                                num_writer: int = 1, 
                                num_req: int = 10) -> None:
    writers = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                for _ in range(num_writer)]
    readers = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                for _ in range(num_reader)]
    clients = writers + readers
    for c in clients: c.connect(ADDR) # Connect all clients
    
    def run_writer(client: socket.socket) -> None:
        for _ in range(num_req):
            # rand_write(client)
            not_rand_write(client)
            # time.sleep(random.randint(0, 1))
    

    def run_reader(client: socket.socket) -> None:
        for _ in range(num_req):
            rand_read(client)
            # time.sleep(random.randint(0, 1))
    

    w_threads = [threading.Thread(name=f'writer_[{i+1}]', target=run_writer, args=(w,)) 
                for i, w in enumerate(writers)]
    r_threads = [threading.Thread(name=f'reader_[{i+1}]', target=run_reader, args=(r,)) 
                for i, r in enumerate(readers)]
    
    threads = r_threads + w_threads
    for t in threads: t.start()
    for t in threads: t.join()
    for client in clients: disconn_req(client)


if __name__ == '__main__':
    # test_read_and_write_clients(num_reader=1, num_writer=4, num_req=30)
    test_read_and_write_clients(num_reader=2, num_writer=3)