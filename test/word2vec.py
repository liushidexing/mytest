#-*- coding: utf-8 -*-

import numpy as np
from word_cut import is_chinese_word
import pdb
from time import time,sleep
import cPickle
import math
import os
from sklearn.cluster import k_means

data_folder = '/data/liubo/message/'

def cal_distance(vec1,vec2):
    return math.sqrt(sum( (a - b)**2 for a, b in zip(vec1, vec2)))

def load_word_word2vec(vector_length,word2vec_file):
    word2vec_dic = {}#{word:vec}
    for line in open(word2vec_file):
        tmp = line.rstrip().split()
        if len(tmp) != vector_length + 1:
            continue
        if is_chinese_word(tmp[0]):
            word2vec_dic[tmp[0]] = map(float,tmp[1:])
    return word2vec_dic

def word2vec_sentence(word2vec_file,raw_data_file,raw_data_vector_file):
    vector_length = 200
    f_vector = open(raw_data_vector_file,'w')
    word2vec_dic = load_word_word2vec(vector_length,word2vec_file)
    count = 0
    start = time()
    for line in open(raw_data_file):
        count += 1
        if count % 10000 == 0:
            print count,(time()-start)
            start = time()
        word_list = line.rstrip().split('\t')
        sentence_vector = [0] * vector_length
        for word in word_list:
            if word in word2vec_dic :
                sentence_vector = np.add(sentence_vector,word2vec_dic.get(word))
        f_vector.write('\t'.join(map(str,sentence_vector))+'\n')
    f_vector.close()

def load_data(raw_data_file,raw_data_vector_file):
    data = []
    sentence_list = []
    for line in open(raw_data_file):
        sentence_list.append(line.rstrip())
    for line in open(raw_data_vector_file):
        data.append(map(float,line.rstrip().split('\t')))
    data = np.asarray(data)
    return data,sentence_list

def cal_cluster_id(vector,cluster_centers,cluster_centers_pow):
    vector_pow = np.dot(vector,vector)
    tmp=np.dot(vector,np.transpose(cluster_centers))
    dist = []
    for index in range(10):
        dist.append(math.sqrt(vector_pow+cluster_centers_pow[index,index]-2*tmp[index]))
    return dist

def cluster():
    word2vec_file = data_folder+'content_topic_000000_0_30_duplicate_chinese_word_vector.txt'
    raw_data_file = data_folder+'content_topic_000000_0_30_duplicate_chinese_split.txt'
    raw_data_vector_file = data_folder+'content_topic_000000_0_30_duplicate_chinese_split_sentence_vectors.txt'
    # word2vec_sentence(word2vec_file,raw_data_file,raw_data_vector_file)
    data,sentence_list = load_data(raw_data_file,raw_data_vector_file)
    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters,n_jobs=15)
    kmeans.fit(data)
    data_predict = kmeans.fit_predict(data)
    result_file = data_folder+'content_topic_000000_0_30_duplicate_chinese_split_sentence_cluster_%d.txt'%(n_clusters)
    cPickle.dump(kmeans.cluster_centers_,open(data_folder+
                        'content_topic_000000_0_30_duplicate_chinese_split_sentence_cluster_%d_centers.txt'%(n_clusters),'w'))
    f_result = open(result_file,'w')
    result_stat_dic = {}
    for index in range(len(data_predict)):
        result_stat_dic[data_predict[index]] = result_stat_dic.get(data_predict[index],0) + 1
        f_result.write(str(data_predict[index])+'\t'+sentence_list[index].replace('\t','')+'\n')
    items = result_stat_dic.items()
    items.sort(key=lambda x:x[1],reverse=True)
    print items

def cal_all_data_cluster_id(vector_length=200):
    n_clusters = 10
    cluster_centers = cPickle.load(open(data_folder+'content_topic_000000_0_30_duplicate_chinese_'
                                                    'split_sentence_cluster_%d_centers.txt'%(n_clusters),'r'))
    cluster_centers_pow = np.dot(cluster_centers,np.transpose(cluster_centers))
    word2vec_file = data_folder+'content_topic_000000_0_30_duplicate_chinese_word_vector.txt'
    raw_data_cut_word_folder = data_folder + 'raw_data_cut_word'
    raw_data_cluster_id_folder = data_folder + 'raw_data_cluster_id'
    word2vec_dic = load_word_word2vec(vector_length,word2vec_file)
    raw_data_listdir = os.listdir(raw_data_cut_word_folder)
    has_process_sentence_dic = {}
    start = time()
    count = 0
    for file_name in raw_data_listdir:
        absolute_path = os.path.join(raw_data_cut_word_folder,file_name)
        f_cluster_id = open(os.path.join(raw_data_cluster_id_folder,file_name),'w')
        for line in open(absolute_path):
            if count % 50000 == 0:
                print count,(time()-start),len(has_process_sentence_dic)
            count += 1
            cut_word = line.rstrip().split('\t')
            chinese_word = []
            sentence_vector = [0] * vector_length
            for word in cut_word:
                if word in word2vec_dic:
                    chinese_word.append(word)
                    sentence_vector = np.add(sentence_vector,map(float,word2vec_dic.get(word)))
            chinese_word = ''.join(chinese_word)
            if chinese_word in has_process_sentence_dic:
                cluster_id = has_process_sentence_dic.get(chinese_word)
            else:
                cluster_id = np.argmin(cal_cluster_id(sentence_vector,cluster_centers,cluster_centers_pow))
                has_process_sentence_dic[chinese_word] = cluster_id
            f_cluster_id.write(str(cluster_id)+'\t'+''.join(cut_word)+'\n')



if __name__ == '__main__':
    # cal_all_data_cluster_id()
    vector_length = 200
    word2vec_file = 'content_topic_000000_0_30_duplicate_chinese_word_vector.txt'
    word2vec_dic = load_word_word2vec(vector_length,word2vec_file)
    for key in word2vec_dic:
        print key
        sleep(0.1)


