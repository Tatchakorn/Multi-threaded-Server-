'''
Message Server
'''
import json
import sys
import os
from typing import Iterable, List
from pathlib import Path
from pprint import pformat

import pika

from message_queue import (
    FanoutMQ, 
    RoutingMQ,
    DefaultMQ,
    TopicsMQ
    )


class JsonHandler:
    '''As the name suggests.'''
    
    def __init__(self, file: Path) -> None:
        self._json_file = file


    def read(self) -> dict:
        if not self._json_file.exists():
            self.write({})
        with open(self._json_file, 'r', encoding='utf-8') as f:
            j = dict(json.loads(f.read()))
        return j
    
    
    def write(self, data: dict):
        with open(self._json_file, 'w', encoding='utf-8') as f:
            json.dump(data, indent=4, sort_keys=True, fp=f, ensure_ascii=False)

    
    def update(self, key: str, val: any) -> None:
        '''Shallow update'''
        data = self.read()
        data[key] = val
        self.write(data)
    

    def delete(self):
        pass


class MBJson(JsonHandler):
    def __init__(self, file: Path) -> None:
        super().__init__(file)

    
    def get_messages_by_user(self, user: str) -> dict:
        data = self.read()
        return list(filter(lambda x: x.get('user') == user, data.get('data')))
    

    def update_append(self, key: str, val: any):
        data = self.read()
        data[key].append(val)
        self.write(data)
    
    def write_message(self, val: dict):
        self.update_append('data', val)
    
    def exists(self) -> bool:
        return self._json_file.exists()


class Users:
    '''Check existing users.'''
    def __init__(self) -> None:
        self._users = set()
    
    def has_registered(self, username: str):
        return username in self._users

    def register(self, username: str) -> None:
        self._users.add(username)
    
    def delete(self, user: str):
        try:
            self._users.remove(user)
        except KeyError:
            print(f'{user} is not a user')
    def __str__(self) -> str:
        return str(self._users)


class MessageBoard:
    '''Message Board.'''
    def __init__(self) -> None:
        self.msg_file = MBJson(Path('msg_board.json'))
        if self.msg_file.exists():
            messages = self.msg_file.read().get('data')
            self._messages = messages
            self._msg_id = messages[-1].get('msg_id') + 1
        else:
            self._messages = []
            self._msg_id = 0
            self.msg_file.write({'data': []})


    def write(self, user: str, recievers: List[str], message: str) -> None:
        msg = {
            'msg_id': self._msg_id,
            'author': user,
            'recievers': recievers,
            'message': message,
        }
        self._messages.append(msg)
        self.msg_file.write_message(msg)
        self._msg_id += 1
    
    def get_txt_messages(self) -> Iterable[str]:
        return (msg.get('message') for msg in self._messages)
    
    def clear(self):
        self.msg_file.write({'data': []})
    

    def __str__(self) -> str:
        return pformat(self._messages)


class Server:
    '''
    user -> register ->
    '''
    def __init__(self) -> None:
        pass


    
def main() -> None:
    # DefaultMQ('test').publish('Greetings!')
    # FanoutMQ().publish('Good')
    # RoutingMQ('r1', 'test', 'routing_ex').publish('Goodd')
    # RoutingMQ('r2', 'test', 'routing_ex').publish('Booo!')
    mb = MessageBoard()
    mb.write('tar', ('user_1',), f'Greetings! 1')
    mb.write('tar', ('goog',), f'Greetings! 2')

    for i in mb.get_txt_messages():
        print(i)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        input('[Press ENTER]...')