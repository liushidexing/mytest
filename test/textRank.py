#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : '2017-11-15 11:36'
# @Author  : 'ligang'

import sys
import jieba
import jieba.analyse

a = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')


# test_a = "政务互联安全，从技术上来说，首先要考虑基础架构的转变，要适应基础架构及政务业务未来易扩展、勤变更、高效运维管理的需要"
test_a = "基于互联网的电子政务系统要从管理、技术等各个方面来综合防范。根据应用系统的安全需求，要合理配置信息安全资源，如经费、设备、人员等方面，采取相应的措施，进行有效的管理，确保系统安全。 "

b = jieba.analyse.textrank(test_a, withWeight=True, topK=5)

for word,score in b:
    print word,score


