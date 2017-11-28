#-*- coding: utf-8 -*-
__author__ = 'liubo-it'

'''
    短信分类流程:
        1.去重 hadoop已做完
        2.分词,生成word2vec的向量 [本地]
        3.分类 [本地]
'''


from cal_cluster_id_hadoop import load_word_word2vec
import sys
import numpy as np
import cPickle
import msgpack
from time import time
import pdb

reload(sys)
sys.setdefaultencoding( "utf-8" )


if __name__ == '__main__':
    count = 0
    vector_length = 200
    # word2vec_file = 'spam_cut_words_vector.txt'
    word2vec_file = 'spam_fraud_cut_words_vector.txt'
    # all_data_clf = cPickle.load(open('spam_message_first_class_clf_all_data.p','rb'))
    all_data_clf = cPickle.load(open('spam_fraud_message_first_class_clf_all_data.p','rb'))

    word2vec_dic = load_word_word2vec(vector_length,word2vec_file)
    trans_index_dic = {}
    trans_index_dic[0] = '广告推销'
    trans_index_dic[1] = '违法信息'
    trans_index_dic[2] = '诈骗'

    predict_data = []
    predict_content = []
    start = time()
    for line in sys.stdin:
    # for line in open('/home/hdp-skyeye/liubo-it/learn/message/data/topic/20160204/data_cut.txt'):
        count += 1
        tmp = line.rstrip().split('\t')
        md5 = tmp[0]
        cut_word = tmp[1:]
        sentence_vector = np.asarray([0] * vector_length)
        find_word_num = 0
        for word in cut_word:
            if word in word2vec_dic:
                sentence_vector = sentence_vector + np.asarray(word2vec_dic.get(word))
                find_word_num += 1
        if find_word_num == 0:
            continue
        # print find_word_num
        # label =  trans_index_dic.get(all_data_clf.predict(sentence_vector)[0])
        # print (md5+'\t'+str(label)+'\t'+line.rstrip().replace('\t','').replace(md5,''))
        predict_data.append(sentence_vector)
        predict_content.append((md5,line.rstrip().replace('\t','').replace(md5,'')))
        if count % 500 == 0:
            predict_data = np.asarray(predict_data)
            predict_result = all_data_clf.predict(predict_data)
            length = len(predict_content)
            for index in range(length):
                md5,content = predict_content[index]
                label = trans_index_dic.get(predict_result[index])
                print (md5+'\t'+str(label)+'\t'+content)
            # print count,time()-start,len(predict_content),len(predict_result)
            # pdb.set_trace()
            start = time()
            predict_data = []
            predict_content = []
    # end = time()
    # print 'time',(end-start)
