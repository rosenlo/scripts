#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
Author: Rosen
Mail: rosenluov@gmail.com
File: ssl_expiry_check.py
Created Time: Tue Nov 26 16:26:59 2019
"""

import socket
import time
import ssl
import datetime
import json

domain_list = '''
www.example1.com
www.example2.com
'''


def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


def ssl_valid_time_remaining(hostname):
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.now()


def check_push_falcon():
    hostname = socket.gethostname()
    ts = int(time.time())
    metric = 'ssl_expires'
    falcon_data = [
        {
            'endpoint': hostname,
            'metric': metric,
            'timestamp': ts,
            'value': ssl_valid_time_remaining(domain).days,
            'counterType': 'GAUGE',
            'tags': 'domain=%s' % domain,
            'step': 60
        }
        for domain in domain_list.split('\n')
        if domain
    ]
    print(json.dumps(falcon_data))


if __name__ == '__main__':
    check_push_falcon()
