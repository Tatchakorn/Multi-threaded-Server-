'''
Assignment#5 Building Shared Message Board
# You are to build a simple shared message board.

# Your board must support persistent and asynchronous communication.
- The sender must be allowed to send a message and to away or even terminate w/o loosing the message.
- The receiver can recieve the message at any time after the message has been successfully placed on board.
- Both the senders and receivers are identified by symbolic names.

# A message can be read by more than one receivers but can only be removed by the owner.

# Your middleware class(es) must provide at least the following services.
- Name registration (register user names)
- Message Sending/receiving
- Message deletion
- Message checking (to prepare for receiving)

# Note that in order to provide persistency, your message server may need to save the messages in secondary storage.
'''

import sys
import os

from message_queue import (
    DefaultMQ, 
    FanoutMQ, 
    RoutingMQ
    )


def main() -> None:
    # DefaultMQ('test').consume()
    # FanoutMQ().consume()
    # r1 = RoutingMQ('r1', 'test', 'routing_ex')
    # r2 = RoutingMQ('r2', 'test2', 'routing_ex')
    # r1.consume()
    # r2.consume()
    pass

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        input('[Press ENTER]...')