#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : '2017-11-16 11:23'
# @Author  : 'ligang'

import sys
from bs4 import BeautifulSoup
import urllib2


a = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')


def getPage(url,header):
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req).read()

    return page


def test():
    # data = getPage("http://www.baidu.com")
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    data = getPage("http://www.gatherproxy.com",headers)
    print data


if __name__ == "__main__":
    test()