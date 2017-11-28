#-*- coding: utf-8 -*-

import jieba
import jieba.posseg
import jieba.analyse
import os
import pdb
from time import time
import msgpack
import base64
import sys
import re
import traceback

reload(sys)
sys.setdefaultencoding( "utf-8" )

data_folder = '/data/liubo/message/'

def is_chinese_word(uchar):
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def stat_word():
    # folder = '/data/liubo/message/message_content'
    folder = './message_content'
    file_list = os.listdir(folder)
    word_id = 0
    word_id_dic = {}
    word_count_stat_dic = {}
    for file_name in file_list:
        start = time()
        absolute_path = folder + '/' + file_name
        file_word_ids = []
        for line in open(absolute_path):
            seg_list = jieba.cut(line.rstrip(),cut_all=False)
            for seg in seg_list:
                if seg in word_id_dic:
                    file_word_ids.append(word_id_dic.get(seg))
                else:
                    file_word_ids.append(word_id)
                    word_id_dic[seg] = word_id
                    word_id += 1
                word_count_stat_dic[seg] = word_count_stat_dic.get(seg,0) + 1
        end = time()
        print file_name,len(word_id_dic),(end-start)
        # pdb.set_trace()

    # msgpack.dump((word_id_dic,word_count_stat_dic),open(data_folder+'word_id_stat_dic','wb'))
    output_f = open("id_dict","w")
    for k,v in word_id_dic.iteritems():
        output_f.write(k + "\t" + str(v) + "\n")
    output_f = open("count_stat_dic", "w")
    for k,v in word_count_stat_dic.iteritems():
        output_f.write(k + "\t" + str(v) + "\n")
    output_f.close()

def cut_all_file(cut_all=False):
    folder = '/data/liubo/message/raw_data'
    cuted_folder = '/data/liubo/message/raw_data_cut_word'
    if not os.path.exists(cuted_folder):
        os.mkdir(cuted_folder)
    file_list = os.listdir(folder)
    count = 0
    has_cut_sentence = {}
    for file_name in file_list:
        try:
            f_write = open(os.path.join(cuted_folder,file_name),'w')
            start = time()
            absolute_path = folder + '/' + file_name
            for raw_line in open(absolute_path):
                line = raw_line.split('\001')[2]
                count += 1
                if count % 50000 == 0:
                    print count
                if line in has_cut_sentence:
                    sentence_word = has_cut_sentence.get(line)
                else:
                    sentence_word = []
                    seg_list = jieba.cut(line.rstrip(),cut_all=cut_all)
                    for seg in seg_list:
                        sentence_word.append(seg)
                    has_cut_sentence[line] = sentence_word
                f_write.write('\t'.join(sentence_word)+'\n')
            end = time()
            print file_name,(end-start)
        except:
            traceback.print_exc()
            continue

def get_useful_word(min_threshold = 100,max_threshold = 100000):
    word_id_dic,word_count_stat_dic = msgpack.load(open(data_folder+'word_id_stat_dic','rb'))
    # max_threshold : 停用词
    # min_threshold :
    useful_word_count_dic = {}
    nouseful_word_count_dic = {}
    for word in word_count_stat_dic:
        count = word_count_stat_dic.get(word)
        if count >= min_threshold and count <= max_threshold and is_chinese_word(word):
            useful_word_count_dic[word] = count
        else:
            nouseful_word_count_dic[word] = count
    # items = word_count_stat_dic.items()
    # items.sort(key=lambda x:x[1],reverse=True)
    msgpack.dump(useful_word_count_dic,open(data_folder+
                        'useful_word_count_dic_chinese_filter_%d_%d'%(min_threshold,max_threshold),'wb'))

def create_data(raw_data_folder,useful_word_count_dic,content_sentence_file,content_word_list_file):
    # folder = '/data/liubo/message/message_content'
    file_list = os.listdir(raw_data_folder)
    # useful_word_count_dic = msgpack.load(open(data_folder+'useful_word_count_dic','rb'))
    length = len(useful_word_count_dic)
    useful_word_count_dic_index = dict(zip(useful_word_count_dic.keys(),range(length)))
    # f_result = open(data_folder+'content_sentence.txt','w')
    # f_result_id = open(data_folder+'content_word_list.txt','w')
    f_result = open(content_sentence_file,'w')
    f_result_id = open(content_word_list_file,'w')
    count = 0
    for file_name in file_list:
        start = time()
        absolute_path = raw_data_folder + '/' + file_name
        for line in open(absolute_path):
            count += 1
            if count % 10000 == 0:
                print count
            sentence_word_ids = []
            # seg_list = jieba.cut(line.rstrip(),cut_all=False)
            seg_list = line.rstrip().split('\t')
            if not is_useful_sentence(seg_list):
                continue
            for seg in seg_list:
                if seg in useful_word_count_dic_index:
                    sentence_word_ids.append(useful_word_count_dic_index.get(seg))
                else:
                    continue
            if len(sentence_word_ids) > 0:
                f_result_id.write('\t'.join(map(str,sentence_word_ids))+'\n')
                f_result.write(line.rstrip()+'\n')
        end = time()
        print file_name,(end-start)

def main():
    print 'find_use_word'
    min_threshold = 100
    max_threshold = 100000
    get_useful_word(min_threshold=min_threshold,max_threshold=max_threshold)
    print 'create_data'
    useful_word_count_dic = msgpack.load(open(data_folder+
                                        'useful_word_count_dic_chinese_filter_%d_%d'%(min_threshold,max_threshold),'rb'))
    raw_data_folder = '/data/liubo/message/message_content_False'
    content_sentence_file = data_folder + '/' + 'content_sentence_%d_%d'%(min_threshold,max_threshold)
    content_word_list_file = data_folder + '/' + 'content_word_list_%d_%d'%(min_threshold,max_threshold)
    create_data(raw_data_folder,useful_word_count_dic,content_sentence_file,content_word_list_file)

def is_useful_sentence(word_list):
    length = len(word_list)
    filter_threshold = 0.5
    alnum_num = 0
    not_chinese_num = 0
    chinese_num = 0
    for seg in word_list:
        if is_chinese_word(seg):
            chinese_num += 1
        elif seg.isalnum():
            alnum_num += 1
        else:
            not_chinese_num += 1
    if not_chinese_num * 1.0 / length >= filter_threshold or alnum_num *1.0 / length >= filter_threshold:
            return False
    else:
        return True

def filter_chinese(raw_content_file,dest_content_file,raw_word_list_file,dest_word_list_file):
    filter_id_list = []
    count = 0
    filter_threshold = 0.5
    filter_num = 0
    f_content_dest = open(dest_content_file,'w')
    f_word_list_dset = open(dest_word_list_file,'w')
    for line in open(raw_content_file):
        seg_list = line.rstrip().replace(' ','').split('\t')
        length = len(seg_list)
        alnum_num = 0
        not_chinese_num = 0
        chinese_num = 0
        for seg in seg_list:
            if is_chinese_word(seg):
                chinese_num += 1
            elif seg.isalnum():
                alnum_num += 1
            else:
                not_chinese_num += 1
        if not_chinese_num * 1.0 / length >= filter_threshold or alnum_num *1.0 / length >= filter_threshold:
            filter_num += 1
            filter_id_list.append(count)
        else:
            f_content_dest.write(line.rstrip()+'\n')
        count += 1
        if count % 100000 :
            print count,filter_num
    filter_id_set = set(filter_id_list)
    count = 0
    for line in open(raw_word_list_file):
        if count in filter_id_set:
            count += 1
        else:
            f_word_list_dset.write(line.rstrip()+'\n')
            count += 1
    f_word_list_dset.close()
    f_content_dest.close()

def process_one_file():
    f_content = open(data_folder + 'content_sentence_000000_0','w')
    f_word_list = open(data_folder + 'content_word_list_000000_0','w')
    raw_data = data_folder + 'raw_data/000000_0'
    word_id_dic = {}
    word_id = 0
    sentence_seglist_dic = {}
    count = 0
    for line in open(raw_data):
        count += 1
        if count % 50000 == 0:
            print count
        tmp = line.rstrip().split('\001')
        sentence = tmp[2]
        if sentence in sentence_seglist_dic:
            seglist =  sentence_seglist_dic.get(sentence)
            for seg in seglist:
                word_id_dic[seg] = word_id_dic.get(seg,0) + 1
        else:
            seglist = jieba.cut(sentence,cut_all=False)
            word_list = []
            for seg in seglist:
                word_list.append(seg)
                word_id_dic[seg] = word_id_dic.get(seg,0) + 1
            sentence_seglist_dic[sentence] = word_list
    msgpack.dump((sentence_seglist_dic,word_id_dic),open('000000_0','wb'))
    # sentence_seglist_dic,word_id_dic = msgpack.load(open('000000_0','rb'))
    word_index_dic = dict(zip(word_id_dic,range(len(word_id_dic))))
    for line in open(raw_data):
        tmp = line.rstrip().split('\001')
        sentence = tmp[2]
        word_id_list = []
        word_list = sentence_seglist_dic.get(sentence)
        for word in word_list:
            word_id_list.append(word_index_dic.get(word))
        f_content.write('\t'.join(word_list)+'\n')
        f_word_list.write('\t'.join(map(str,word_id_list))+'\n')
    f_content.close()
    f_word_list.close()

if __name__ == '__main__':
    # cut_all_file()
    # main()
    # process_one_file()
    # sentence_seglist_dic,word_id_dic = msgpack.load(open('000000_0','rb'))
    # pdb.set_trace()
    stat_word()