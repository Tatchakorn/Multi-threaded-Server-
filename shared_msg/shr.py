'''
Assignment#5 Building Shared Message Board
# You are to build a simple shared message board.

# Your board must support persistent and asynchronous communication.
- The sender must be allowed to send a message and to away or even terminate w/o loosing the message.
- The receiver can recieve the message at any time after the message has been successfully placed on board.
- Both the senders and receivers are identified by symbolic names.

# A message can be read by more than one receivers but can inly be removed by the owner.

# Your middleware class(es) must provide at least the following services.
- Name registration (register user names)
- Message Sending/receiving
- Message deletion
- Message checking (to prepare for receiving)

# Note that in order to provide persistency, your message server may need to save the messages in secondary storage.
'''
if __name__ == '__main__':
    ...
