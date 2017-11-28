#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : '2017-11-22 16:23'
# @Author  : 'ligang'

import sys
import codecs
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

a = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')


corpus = []
for line in open('china_txt', 'r').readlines():
    # print line
    corpus.append(line.strip())

# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

word = vectorizer.get_feature_names()

# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

resName = "china_txt_esult"
result = codecs.open(resName, 'w', 'utf-8')
for j in range(len(word)):
    result.write(word[j] + ' ')
result.write('\r\n\r\n')

for i in range(len(weight)):
    print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    for j in range(len(word)):
        result.write(str(weight[i][j]) + ' ')
    result.write('\r\n\r\n')

result.close()