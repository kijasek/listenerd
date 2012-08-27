# -*- coding: utf8 -*-
import logging
import amqplib.client_0_8 as amqp

from listenerd_lib.utils import timeout_call
from listenerd_lib.config import conf

logger = logging.getLogger(__name__)

class AmqpConnection(object):
    CONSUMER_TAG = 'listenerd'    
    
    def __init__(self):
        self.amqp_host_port = ':'.join([conf['amqp_host'], 
                                        str(conf['amqp_port'])])        
        self.amqp_virtual_host = conf['amqp_virtual_host'] 
        self.amqp_user = conf['amqp_user']
        self.amqp_password = conf['amqp_password']
        self.amqp_queue = conf['amqp_queue']
        self.amqp_exchange = conf['amqp_exchange']
        self.amqp_routing_key = conf['amqp_routing_key']
        self.amqp_timeout = conf['amqp_timeout'] 
        
        self.conn = None
        self.ch = None
        
        self.reconnect()
        
    def reconnect(self):
        self.__connect()
        if self.conn is not None:
            self.__set_up_channel()
            
    def __connect(self):                    
        try:
            logger.debug("creating amqp connection")
            self.conn = timeout_call(self.amqp_timeout,
                                     amqp.Connection, 
                                     host=self.amqp_host_port, 
                                     userid=self.amqp_user, 
                                     password=self.amqp_password, 
                                     virtual_host=self.amqp_virtual_host)
            
            self.conn.transport.sock.settimeout(self.amqp_timeout)            
        except Exception:
            logger.exception('Error connecting to rabbitmq.')
            self.conn = None
        
    def __set_up_channel(self):
        try:
            logger.debug("setting up amqp channel")
            self.ch = self.conn.channel()
            self.ch.access_request('/data', active=True, write=True, read=True)
            self.ch.exchange_declare(exchange=self.amqp_exchange, 
                                     type='direct', 
                                     durable=False, 
                                     auto_delete=False)
            self.ch.queue_declare(queue=self.amqp_queue, 
                                  durable=False, 
                                  exclusive=False,
                                  auto_delete=False)            
            self.ch.queue_bind(queue=self.amqp_queue, 
                               exchange=self.amqp_exchange, 
                               routing_key=self.amqp_routing_key)
        except Exception:
            logger.exception('Error setting up channel.')
            self.ch = None
            
    def get(self, no_ack=False):
        return timeout_call(self.amqp_timeout, 
                            self.ch.basic_get, 
                            self.amqp_queue,
                            no_ack)  
    
    def ack(self, delivery_tag):
        self.ch.basic_ack(delivery_tag)
        
    def register_callback(self, method):
        logger.debug("registering callback %s", method)
        try:
            self.ch.basic_consume(queue=self.amqp_queue,
                              no_ack=True,
                              callback=method,
                              consumer_tag=AmqpConnection.CONSUMER_TAG)
        except Exception:
            logger.exception('error registering callback')
            raise
    
    def unregister_callback(self):
        try:
            self.ch.basic_cancel(AmqpConnection.CONSUMER_TAG)
        except Exception:
            logger.exception('error unregistering callback')            
    
    def __del__(self):
        if self.ch is not None:
            try:
                self.ch.close()
            except:
                pass
            
        if self.conn is not None:
            try:
                self.conn.close()
            except:
                pass
            
