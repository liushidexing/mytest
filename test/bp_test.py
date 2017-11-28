#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/9/26 15:47
# @Author  : ligang-s
# @File    : bp_test.py

import numpy as np
import math,sys


def sigmoid(self, x):
    return math.tanh(x)

def dsigmoid(y):
    return 1.0 - y**2

class bp:
    def __init__(self,input_node_num,hidden_node_num,output_node_num,learn_rate):
        self.input_node_num = input_node_num
        self.hidden_node_num = hidden_node_num
        self.output_node_num = output_node_num
        self.learn_rate = learn_rate

        # print self.input_node_num
        # print self.hidden_node_num
        # print self.output_node_num

        ## para
        self.input_para_array = np.random.random((self.input_node_num,self.hidden_node_num))
        self.hidden_para_array = np.random.random((self.hidden_node_num,self.output_node_num))

        ## bias
        self.input_bias_array = np.random.random((self.hidden_node_num,1))
        self.hidden_bias_array = np.random.random((self.output_node_num,1))

        ## layer_array
        self.input_layer_array = np.random.random((self.input_node_num,1))
        self.hidden_layer_array = np.random.random((self.hidden_node_num,1))
        self.output_layer_array = np.random.random((self.output_node_num,1))

        ## error_array
        self.output_error_array = np.zeros(self.output_node_num)
        self.hidden_error_array = np.zeros(self.hidden_node_num)

    def forward(self,input_data):
        # print len(input_data)
        if len(input_data) != self.input_node_num:
            print "输入数据维度与输入层节点数不等"
            sys.exit(0)

        ## input_layer_array
        self.input_layer_array = np.array(input_data).reshape(1,2)

        ## hidden_layer_array
        for i in range(self.hidden_node_num):
            self.hidden_layer_array[i] = sigmoid(self,np.dot(self.input_layer_array,self.input_para_array[:,i]) + self.input_bias_array[i])

        # print self.hidden_layer_array

        ## output_layer_array
        for i in range(self.output_node_num):
            self.output_layer_array[i] = sigmoid(self,np.dot(self.hidden_layer_array[i],self.hidden_para_array[i])) + self.hidden_bias_array[i]
        # print self.output_layer_array

    def backward(self,input_label):

        ## output_error
        for i in range(self.output_node_num):
            self.output_error_array[i] = (input_label - self.output_layer_array) * dsigmoid(self.output_layer_array[i])
                                         # * dsigmoid(self.output_layer_array[i])
        # print self.output_error_array

        ## hidden_error
        for i in range(self.hidden_node_num):
            for j in range(self.output_node_num):
                # print "hidden_para:\t" + str(self.hidden_para_array[i])
                # print self.output_error_array[j]
                self.hidden_error_array[i] = self.hidden_para_array[i] * self.output_error_array[j] * dsigmoid((self.hidden_layer_array[i]))
                                             # * dsigmoid(self.hidden_layer_array[i])
        # print self.hidden_error_array

        ## update hidden para
        for i in range(self.hidden_node_num):
            for j in range(self.output_node_num):
                self.hidden_para_array[i] += self.learn_rate * self.output_error_array[j]

        ## update input para
        for i in range(self.input_node_num):
            for j in range(self.hidden_node_num):
                self.input_para_array[i] += self.learn_rate * self.hidden_error_array[j]

def test(n):
    print np.random.random((n,1))
    print np.array([1]) - np.array([[0.5]])

if __name__ == "__main__":
    bp = bp(2, 3, 1, 0.05)

    input_data = [[1, 0], [0, 1], [0, 0], [1, 1]]
    input_label = [0, 0, 1, 1]

    for i in range(1000):
        for j in range(4):
        # for j in [3]:
            bp.forward(input_data[j])
            print str(i) + "\t" + str(j) + "\t" + str(bp.output_layer_array)
            bp.backward(input_label[j])
    # test(3)