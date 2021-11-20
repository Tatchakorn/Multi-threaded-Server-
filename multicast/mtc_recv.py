#! /usr/bin/python3

import threading
import socket
from test import create_upd_clients
from client import multicast_receive

def test_multicast_receive():
    clients = create_upd_clients(3)

    def run(client: socket.socket) -> None:
        multicast_receive(client)
    
    threads = [threading.Thread(name=f'client_[{i+1}]', target=run, args=(client,)) 
                for i, client in enumerate(clients)]
    for t in threads: t.start()
    for t in threads: t.join()


if __name__ == '__main__':
    try:
        test_multicast_receive()
    except Exception as e:
        print(e)
    finally:
        input('Press [ENTER]...')