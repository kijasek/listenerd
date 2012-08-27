#!/usr/bin/env python2.5
# -*- coding: utf8 -*-
import sys
import traceback

from listenerd_lib.config import init_config
from listenerd_lib.config import conf
from listenerd_lib.logging_utils import configure_logging
from listenerd_lib.listener_daemon import ListenerDaemon

CONFIG_FILE_LOCATION = '/etc/listenerd.conf'
PID_FILE_TEMPLATE = '/listenerd_%s.pid'

def control(cmd):
    if 'start' == cmd:
    
            print 'starting...'
            for daemon in daemons:
                print daemon
                daemon.start()
            print 'started'                                
    
    elif 'stop' == cmd:
        
        print 'stopping...'
        for daemon in daemons:
            try:
                print daemon
                daemon.stop()
            except Exception:
                print 'error stoping daemon: %s' % daemon
                traceback.print_exc()
                continue
        print 'stopped'                                
    
    elif 'restart' == cmd:
        
        print 'restarting...'
        for daemon in daemons:
            try:
                print daemon
                daemon.restart()
            except Exception:
                print 'error restarting daemon: %s' % daemon
                traceback.print_exc()
                continue
        print 'restarted'
                                        
    else:
        print "Unknown command"
        sys.exit(2)    

if __name__ == "__main__":
    
    init_config(CONFIG_FILE_LOCATION)
    configure_logging()
    
    pid_file_location = conf['pid_file_location']
    clones = conf['clones']
    
    daemons = []
    
    for clone_no in xrange(clones):
        pid_file_name = PID_FILE_TEMPLATE % clone_no
        pid_file_name = pid_file_location + pid_file_name        
        daemons.append(ListenerDaemon(pid_file_name))
    
    if len(sys.argv) == 2:
        control(sys.argv[1])
        sys.exit(0)        
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
