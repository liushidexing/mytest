#! /usr/bin/env python
#coding:utf-8

__author__ = 'ligang-s'

import math
import sys
import numpy as np


class BP:

    def __init__(self,input_node_num,hidden_node_num,output_node_num,learn_rate):
        self.input_node_num = input_node_num
        self.hidden_node_num = hidden_node_num
        self.output_node_num = output_node_num
        self.learn_rate = learn_rate

        self.input_para_array = np.random.random((self.input_node_num,self.hidden_node_num))
        self.hidden_para_array = np.random.random((self.hidden_node_num,self.output_node_num))
        self.input_bias_array = np.random.random((self.hidden_node_num,1))
        self.input_layer_array = np.random.random((self.input_node_num,1))
        self.hidden_layer_array = np.random.random((self.hidden_node_num,1))
        self.output_layer_array = np.random.random((self.output_node_num,1))
        self.hidden_bias_array = np.random.random((self.output_node_num,1))

        self.output_error_array = np.zeros(self.output_node_num)
        self.hidden_error_array = np.zeros(self.hidden_node_num)

    def sigmoid(self,x):
        return math.tanh(x)

    # 函数 sigmoid 的派生函数, 为了得到输出 (即：y)
    def dsigmoid(self,y):
        # print "y\t" + str(y)
        return 1.0 - y ** 2

    ##单个样本
    def forward_process(self,input_data,index_num):
        # print len(input_data)
        if len(input_data) != self.input_node_num:
            print "输入数据维度与输入层节点数不等"
            sys.exit(0)

        ##输入层
        self.input_layer_array = input_data

        print self.input_layer_array.shape
        print self.input_para_array[:, 0].shape
        print np.dot(self.input_layer_array,self.input_para_array[:,0])
        print self.input_para_array[:,0]

        # ##隐藏层
        # # print self.input_layer_array
        # for i in range(self.hidden_node_num):
        #     #print "####" + str(i)
        #     # print self.input_para_array[:,i]
        #     # print self.input_bias_array[i]
        #     tmp_sum = (np.dot(self.input_layer_array,self.input_para_array[:,i]) + self.input_bias_array[i])
        #     # print "tmp_sum"
        #     # print tmp_sum
        #     # print tmp_sum[0]
        #     # print self.sigmoid(tmp_sum[0])
        #     # self.hidden_layer_array[i] = self.sigmoid(np.dot(self.input_layer_array,self.input_para_array[:,i]) + self.input_bias_array[i])
        #     self.hidden_layer_array[i] = self.sigmoid(tmp_sum[0])
        #
        # # print self.hidden_layer_array
        #
        # ##输出层
        # #print self.hidden_para_array
        #
        # for i in range(self.output_node_num):
        #     # print "###" + str(i)
        #     # print np.dot(self.hidden_layer_array.transpose(),self.hidden_para_array,)
        #     #print self.hidden_bias_array[i]
        #     self.output_layer_array = np.dot(self.hidden_layer_array.transpose(),self.hidden_para_array,) + self.hidden_bias_array[i]
        #
        #     # print self.output_layer_array
        # print str(index_num) + "\t" + str(self.output_layer_array)
        # return self.output_layer_array

    def backforward_process(self,target):
        if len(target) != self.output_node_num:
            print "输出节点数与目标数据维度不等"
            sys.exit(0)

        ##计算输出层误差
        for i in range(self.output_node_num):
            self.output_error_array[i] = target[i] - self.output_layer_array[i]
        print "output_error_array\t" + str(self.output_error_array)

        # ##计算隐藏层误差
        for i in range(self.hidden_node_num):
            for j in range(self.output_node_num):
                # print self.output_layer_array[j]
                # print self.output_layer_array
                # print len(self.output_layer_array[j])
                # print (self.output_layer_array[j])[0]
                # print self.dsigmoid((self.output_layer_array[j])[0])
                self.hidden_error_array[i] += self.hidden_para_array[i][j] * self.output_error_array[j] \
                                              # * self.dsigmoid((self.output_layer_array[j])[0])
        # print "hidden_error_array\t" + str(self.hidden_error_array)

        ##更新隐藏层参数
        for i in range(self.hidden_node_num):
            for j in range(self.output_node_num):
                self.hidden_para_array[i] += self.learn_rate * self.hidden_layer_array[i] * self.output_error_array[j]

        ##更新输入层参数
        # for i in range(self.input_node_num):
        #     for j in range(self.hidden_node_num):
        #         self.input_para_array[i] += self.learn_rate * self.hidden_error_array[j]

if __name__ == "__main__":
    bp = BP(2,3,1,0.05)
    # print bp.input_layer_array
    # print bp.input_layer_array.shape
    # # print bp.hidden_layer_array
    # print bp.hidden_layer_array.shape
    # # print bp.output_layer_array
    # print bp.output_layer_array.shape
    #
    # print bp.input_para_array.shape
    # print bp.hidden_para_array.shape

    input_data = [[1,0],[0,1],[0,0],[1,1]]
    input_label = [0,0,1,1]
    input_array = np.array(input_data)
    print input_array.shape
    #
    print input_array[0]
    for i in range(1):
        output_layer_array = bp.forward_process(input_array[0],0)
        # bp.backforward_process([input_label[0]])
    #     output_layer_array = bp.forward_process(input_array[1],1)
    #     bp.backforward_process([input_label[1]])
    #     output_layer_array = bp.forward_process(input_array[2],2)
    #     bp.backforward_process([input_label[2]])
    #     output_layer_array = bp.forward_process(input_array[3],3)
    #     bp.backforward_process([input_label[3]])
    # print output_layer_array