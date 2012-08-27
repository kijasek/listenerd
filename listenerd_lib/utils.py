# -*- coding: utf8 -*-
import socket
import time
import logging

logger = logging.getLogger(__name__)

def timeout_call(timeout, function, *args, **kwargs):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        result = function(*args, **kwargs)
    finally:
        socket.setdefaulttimeout(old_timeout)
    return result


def profiler(func):
    def wrapper(*args):
        time_before = time.time()
        result = func(*args)    
        time_after = time.time()
        time_diff = time_after - time_before
        logger.debug("%s EXECUTION TIME: %.4fs" % (func.__name__, time_diff))
        return result
    return wrapper
