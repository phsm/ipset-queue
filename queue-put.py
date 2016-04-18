#!/usr/bin/env python
import sys
import os
from redis import StrictRedis
from rq import Queue
from ConfigParser import ConfigParser, NoOptionError
from lib.functions import ipset_add

if len(sys.argv) == 1:
    sys.stderr.write("Please specify IP-address to add.\n")
    sys.exit(1)

ipaddr = sys.argv[1]
cur_dir = os.path.dirname(os.path.abspath(__file__))
conf = ConfigParser()

with open(cur_dir + os.path.sep + 'config.ini') as f:
    conf.readfp(f)
try:
    r_host = conf.get('redis', 'server')
    r_port = conf.get('redis', 'port')
    r_db = conf.get('redis', 'db')
    queues = [e.strip() for e in conf.get('queue', 'proxies').split(',')]
except NoOptionError as e:
    print(e)
    sys.exit(1)

redis_conn = StrictRedis(host=r_host, port=r_port, db=r_db)
for i in queues:
    Queue(i, connection=redis_conn).enqueue(ipset_add, ipaddr)
