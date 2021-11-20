#! /usr/bin/python3
import socket
import logging
import sys
import struct
from conn import CODEC_FORMAT, MULTICAST_GROUP

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'server.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)


def multicast_send(msg: str):
    
    # MULTICAST_GROUP = ('255.255.255.255', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a timeout so the socket does not block indefinitely when
    # trying to receive data.
    sock.settimeout(1)
    # Set the time-to-live for messages to 1 so they do not go 
    # past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        logger.info(f'[SEND] "{msg}"')
        sock.sendto(msg.encode(CODEC_FORMAT), MULTICAST_GROUP)
        
        # Look for responses from all recipients
        while True:
            print('[WAIT RESPOND]...')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                logger.info('[TIMED OUT] no more responses')
                break
            else:
                logger.info(f'[RECEIVED] "{data}" from {server}')
    finally:
        logger.info('[CLOSING] socket')
        sock.close()

if __name__ == '__main__':
    try:
        data = list(range(10))
        for d in data:
            multicast_send(str(d))
    except Exception as e:
        print(e)
    finally:
        input('Press [ENTER]...')