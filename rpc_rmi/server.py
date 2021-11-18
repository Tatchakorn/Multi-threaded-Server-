#! /usr/bin/python3

"""
Distributed Systems Assignment #4
1. Design a SciCalculatorServer class to accept calculation 
requests from clients.
2. The server should accept requests such as add, sub, mul, 
div, pow, sqr, log, sin, cos operations. Define remote 
interface if necessary.
3. Design a SciCalculatorClient class to invoke the remote 
operations in a loop until exist

Author: Tatchakorn Saibunjom
"""

import Pyro5.api


@Pyro5.api.expose
class GreetingMaker:
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
            "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)

daemon = Pyro5.api.Daemon()             # make a Pyro daemon
uri = daemon.register(GreetingMaker)    # register the greeting maker as a Pyro object

print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
daemon.requestLoop()                    # start the event loop of the server to wait for calls