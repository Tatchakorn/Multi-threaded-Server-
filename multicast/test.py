import random
import socket
import threading
from typing import Union, Callable
from client import req, disconn_req
from conn import ADDR

AVAILABLE_OPS = ('+', '-', '/', '*')


def rand_req() -> str:
    op = random.choice(AVAILABLE_OPS)
    a, b = (random.randint(0, 100), random.randint(0, 100))
    return f'{op} {a} {b}'



def test_reqs(num_client: int = 3):
    clients = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(num_client)]
    for client in clients: client.connect(ADDR)
    
    
    def run(client: socket.socket) -> None:
        req(client, rand_req())
        
    threads = [threading.Thread(name=f'client_[{i+1}]', target=run, args=(client,)) 
                for i, client in enumerate(clients)]
    for t in threads: t.start()
    for t in threads: t.join()
    for client in clients: disconn_req(client)


if __name__ == '__main__':
    try:
        test_reqs(1)
    except Exception as e:
        print(e)
    finally:
        input('Press [ENTER]...')