#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/1/9 15:24
# @Author  : ligang-s
# @File    : base.py

import socket
import struct
import hashlib
from functools import wraps
from threading import Thread
import ipaddress
import re


def host_qualify(host):
    host = host.lower()
    host_flag_1 = re.match(r'^([a-z0-9]\.|[a-z0-9][-a-z0-9]{0,61}[a-z0-9]\.)+([a-z0-9]|[a-z0-9][-a-z0-9]{0,61}[a-z0-9])$',host)!= None
    host_flag_2 = re.match(r'[0-9]+',host.split('.')[-1]) == None
    host_flag_3 = len(host) <= 253
    return host_flag_1 and host_flag_2 and host_flag_3


def ip_qualify(ip):
    ipv4_flag = re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$',ip) != None
    ipv6_flag = re.match(r'^([\da-fA-F]{1,4}:){6}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^::([\da-fA-F]{1,4}:){0,4}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:):([\da-fA-F]{1,4}:){0,3}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){2}:([\da-fA-F]{1,4}:){0,2}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){3}:([\da-fA-F]{1,4}:){0,1}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){4}:((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){7}[\da-fA-F]{1,4}$|^:((:[\da-fA-F]{1,4}){1,6}|:)$|^[\da-fA-F]{1,4}:((:[\da-fA-F]{1,4}){1,5}|:)$|^([\da-fA-F]{1,4}:){2}((:[\da-fA-F]{1,4}){1,4}|:)$|^([\da-fA-F]{1,4}:){3}((:[\da-fA-F]{1,4}){1,3}|:)$|^([\da-fA-F]{1,4}:){4}((:[\da-fA-F]{1,4}){1,2}|:)$|^([\da-fA-F]{1,4}:){5}:([\da-fA-F]{1,4})?$|^([\da-fA-F]{1,4}:){6}:$',ip) != None
    return ipv4_flag or ipv6_flag


def md5_qualify(md5):
    md5 = md5.lower()
    md5_pattern = '^[a-z0-9]{32}$'
    md5_flag = bool(re.match(md5_pattern,md5))
    exclude_pattern = '^'+'0'*30+'[a-z0-9]{2,2}$'
    return md5_flag and not re.match(exclude_pattern,md5)


class TimeOutException(Exception):
    # print "function time out"
    pass


def time_out():
    # print "function time out"
    return
    # raise TimeOutException


def getMd5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def ip2Num(ip):
    return socket.ntohl(struct.unpack("I",socket.inet_aton(ip))[0])


def num2Ip(num):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(num)))


def is_valid_ipv4(input_str):
    try:
        d1,d2,d3,d4 = input_str.strip().split('.')
        d1 = int(d1)
        d2 = int(d2)
        d3 = int(d3)
        d4 = int(d4)
        ll = [d1,d2,d3,d4]
        for i in ll:
            if 0>i or i>255:
                return False
        return True
    except:
        return False


def is_intra_ip(ip):
    try:
        d1,d2,d3,d4 = ip.strip().split('.')
        d1 = int(d1)
        d2 = int(d2)
        if d1 == 10: return True
        elif d1 == 172 and 16<=d2<=31: return True
        elif d1 == 192 and d2 == 168: return True
        else: return False
    except:
        return False


def ipv4_items(input_str):
    try:
        d1, d2, d3, d4 = input_str.strip().split('.')
        d1 = int(d1)
        d2 = int(d2)
        d3 = int(d3)
        d4 = int(d4)
        ll = [d1, d2, d3, d4]
        for i in ll:
            if 0 > i or i > 255:
                return []
        return map(str,ll)
    except:
        return []

ThreadStop = Thread._Thread__stop

def time_limit(interval):
    def run_test(func):
        @wraps(func)
        def deco_test(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self, _error=None, ):
                    Thread.__init__(self)
                    self._error = _error

                def run(self):
                    try:
                        self.result = func(*args, **kwargs)
                    except Exception, e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            t = TimeLimited()
            t.start()
            t.join(interval)
            if isinstance(t._error, TimeOutException):
                t._stop()
                raise TimeOutException('timeout for %s' % (func.__name__))
            if t.isAlive():
                t._stop()
                raise TimeOutException('timeout for %s' % (func.__name__))
            if t._error is None:
                return t.result
        return deco_test
    return run_test


def ip_reserve_judge(ip):
    tmp_ip = ipaddress.ip_address(ip.decode('gbk'))
    if not tmp_ip.is_global:
        return True
    if tmp_ip.is_link_local:
        return True
    if tmp_ip.is_loopback:
        return True
    if tmp_ip.is_multicast:
        return True
    if tmp_ip.is_reserved:
        return True
    if tmp_ip.is_unspecified:
        return True
    if ip.startswith('192.0.0.') or ip.startswith('192.88.99.'):
        return True

    return False
