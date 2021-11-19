#! /usr/bin/python3

import sys
import subprocess
import time
import os
from glob import glob
from pathlib import Path
from typing import Union

multithread_test_path = Path('./multi_threaded/test.py')
multithread_server_path = Path('./multi_threaded/server.py')
multicast_multicast_path = Path('./multicast/multicast.py')
multicast_test_path = Path('./multicast/test.py')
multicast_tcp_server_path = Path('./multicast/tcp_server.py')
multicast_udp_server_path = Path('./multicast/udp_server.py')

LINUX_TERMINAL_CMD = 'gnome-terminal -- python3'

GREETINGS = '''Greetings!
Options:
    "mt": Multi-threaded Server
        "t": test only
        "s": server only
    "mc": Multicast Server
        "t": test only
        "s": server only
    "r": RPC and RMI
    "del": delete *.log files
    "help": Greetings! again!
    "exit": exit
'''

INPUT_ERR_MSG = 'Invalid Input! more info -- type "help" or "h"'

def exec_win32_(command: str) -> Union[None, bool]:
    command = command.split()
    if command[0] == 'mt':
        if len(command) == 1:
            subprocess.Popen(['start', 'python', multithread_server_path], shell=True)
            time.sleep(2)
            subprocess.Popen(['start', 'python', multithread_test_path], shell=True)
        elif len(command) == 2:
            if command[1] == 't':
                subprocess.Popen(['start', 'python', multithread_test_path], shell=True)
            elif command[1] == 's':
                subprocess.Popen(['start', 'python', multithread_server_path], shell=True)
            else:
                return False
        else:
            return False
    elif command[0] == 'mc':
        subprocess.Popen(['start', 'python', multicast_test_path], shell=True)
    elif command[0] == 'del':
        subprocess.Popen(['del', '*.log'], shell=True)
    else:
        return False


def exec_linux_(command: str) -> Union[None, bool]:
    command = command.split()
    if command[0] == 'mt':
        if len(command) == 1:
            cmd = f'{LINUX_TERMINAL_CMD} {multithread_server_path}'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            time.sleep(2)
            cmd = f'{LINUX_TERMINAL_CMD} {multithread_test_path}'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        elif len(command) == 2:
            if command[1] == 't':
                cmd = f'{LINUX_TERMINAL_CMD} {multithread_test_path}'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            elif command[1] == 's':
                cmd = f'{LINUX_TERMINAL_CMD} {multithread_server_path}'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            else:
                return False
        else:
            return False
    elif command[0] == 'mc':
        if len(command) == 1:
            cmd = f'{LINUX_TERMINAL_CMD} {multicast_tcp_server_path}'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            time.sleep(2)
            cmd = f'{LINUX_TERMINAL_CMD} {multicast_test_path}'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        elif len(command) == 2:
            if command[1] == 't':
                cmd = f'{LINUX_TERMINAL_CMD} {multicast_test_path}'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            elif command[1] == 's':
                cmd = f'{LINUX_TERMINAL_CMD} {multicast_tcp_server_path}'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    elif command[0] == 'del':
        for f in glob('*.log'): 
            os.remove(f)
    else:
        return False

if __name__ == '__main__':
    print(GREETINGS)
    line_i = 1
    while True:
        try:
            command = str(input(f'[{line_i}]: '))
            if command in ('exit', 'e'):
                break
            if command in ('help', 'h'):
                print(GREETINGS)
                continue
            if sys.platform == 'win32':
                if exec_win32_(command) is False:
                    print(INPUT_ERR_MSG)
            elif sys.platform == 'linux': # Ubuntu
                if exec_linux_(command) is False:
                    print(INPUT_ERR_MSG)
            else:
                print('Not using Linux or Windows? \n BYE!')
                break
        except Exception as e:
            print(f'Exception: {e}')
            continue
        finally:
            line_i += 1