# -*- coding: utf8 -*-
import logging
from logging.handlers import SysLogHandler

from listenerd_lib.config import conf

def configure_logging(): 
    logging_level = getattr(logging, 
                            conf['logging_level'].upper(), 
                            logging.INFO)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)    

    syslog_handler = SysLogHandler('/dev/log', 
                                   facility=conf['logging_facility'])
    syslog_handler.setLevel(logging_level)
    syslog_formatter = logging.Formatter(conf['logging_format'])
    syslog_handler.setFormatter(syslog_formatter)
    
    root_logger.addHandler(syslog_handler)
    
