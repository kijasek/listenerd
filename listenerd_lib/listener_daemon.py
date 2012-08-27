# -*- coding: utf8 -*-
import logging
import time

import simplejson

from listenerd_lib.daemon import Daemon
from listenerd_lib.config import conf
from listenerd_lib.utils import profiler
from listenerd_lib.mq import AmqpConnection

logger = logging.getLogger(__name__)

@profiler
def process_message(msg):
    logger.info('received message: %s', msg.body)
    message = simplejson.loads(msg.body)
    logger.debug("message: %s", message)

class ListenerDaemon(Daemon):
    
    def run(self):
        logger.debug('ListenerDaemon run...')        
        amqp_connection = AmqpConnection()
        amqp_connection.register_callback(process_message)
        
        while True:            
            try:            
                amqp_connection.ch.wait()
            except Exception:
                logger.exception('Problems with rabbitmq')
                amqp_connection.unregister_callback()
                amqp_connection.reconnect()
                amqp_connection.register_callback(process_message)
            
