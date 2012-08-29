# -*- coding: utf8 -*-
from ConfigParser import RawConfigParser

_conf_defaults = dict(        
    pid_file_location='/var/run',
    clones=1,
    
    logging_level='debug',
    logging_format='%(levelname)s : %(name)s : %(message)s',
    logging_facility='user',
    
    amqp_host='localhost',
    amqp_port=5672,
    amqp_virtual_host='/',
    amqp_user='guest',
    amqp_password='guest',

    amqp_exchange='msg_exchange',
    amqp_queue='msg_queue',
    amqp_routing_key='msg_test',
    amqp_timeout=10,
    amqp_message_discard_time=1200,
)

conf = _conf_defaults.copy()

def init_config(conf_file_name):
    parser = RawConfigParser()
    parser.read(conf_file_name)
        
    for section in parser.sections():
        items = ((name, value)
                 for (name, value) in parser.items(section))
        
        conf.update(dict(items))
    
    for key in _conf_defaults:
        if isinstance(_conf_defaults[key], int):
            conf[key] = int(conf[key])
        elif isinstance(_conf_defaults[key], float):
            conf[key] = float(conf[key])


        
