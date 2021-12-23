'''Testing RabbitMQ & Pika'''
from abc import ABC, abstractmethod

import pika
from pika.spec import PERSISTENT_DELIVERY_MODE


class MQ(ABC):
    '''RabbitMQ: http://localhost:15672/'''

    def __init__(self, host:str = 'localhost') -> None:
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
            )
        self._channel = self._connection.channel()
    
    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def consume(self):
        pass

class DefaultMQ(MQ):
    '''Nameless'''

    def __init__(self, queue: str, host: str = 'localhost') -> None:
        super().__init__(host=host)    
        self.queue = queue
        self._channel.queue_declare(
            queue=self.queue, 
            # durable=True
            )
        
    
    def publish(self, message: str) -> None:
        '''default exchange'''
        self._channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=message
            )
        self._connection.close()
    

    def consume(self) -> None:
        '''default exchange'''
        def callback(channel, method, properties, body):
            print(f'[Recieved] {body}')
            channel.basic_ack(delivery_tag=method.delivery_tag)
        
        print(self.queue)
        self._channel.basic_consume(
            queue=self.queue, 
            on_message_callback=callback, 
            # auto_ack=True
        )
        print('[Waiting for Messages]')
        self._channel.start_consuming()


class FanoutMQ(MQ):
    def __init__(self, exchange: str = 'test',host: str = 'localhost') -> None:
        super().__init__(host=host)
        self._exchange = exchange    
        res_q = self._channel.queue_declare(
            queue='', 
            durable=True
            )
        self.queue = res_q.method.queue
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='fanout'
        )
        
    def publish(self, message: str) -> None:
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key='',
            body=message
            )
        properties = pika.BasicProperties(
            delivery_mode=PERSISTENT_DELIVERY_MODE
            )
        self._connection.close()
    
    def consume(self):
        self._channel.queue_bind(
            exchange=self._exchange,
            queue=self.queue
            ) 
        def callback(ch, method, properties, body):
            print(f'[x] {body}')

        self._channel.basic_consume(
            queue=self.queue, 
            on_message_callback=callback, 
            auto_ack=True
            )

        self._channel.start_consuming()


class RoutingMQ(MQ):
    
    def __init__(self, 
        routing_key: str, 
        queue: str, 
        exchange: str, 
        host: str = 'localhost') -> None:
        super().__init__(host=host)
        self._exchange = exchange
        self._routing_key = routing_key
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='direct'
            )
        self.queue = queue
        self._channel.queue_declare(
            queue=self.queue, 
            # exclusive=True,
            )
        
    
    def publish(self, message: str):
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._routing_key,
            body=message
            )
        print(f'[Messsage Sent] \n ex: {self._exchange} \n rt_k :{self._routing_key} \n {message}')

    def consume(self):
        self._channel.queue_bind(
            exchange=self._exchange,
            queue=self.queue,
            routing_key=self._routing_key
            )
        
        def callback(ch, method, properties, body):
            print(f'[x] {body}')
        print('[*]')

        self._channel.basic_consume(
            queue=self.queue, 
            on_message_callback=callback, 
            auto_ack=True
            )
        self._channel.start_consuming()


class TopicsMQ(MQ):
    def publish(self):
        pass
    
    def consume(self):
        pass 


if __name__ == '_main__':
    pass