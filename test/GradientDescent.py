#! /usr/bin/env python
# coding:utf-8

__author__ = 'ligang-s'

import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.datasets import make_regression

def main():
    data_x, data_y = make_regression(1000,1,bias=0.5,tail_strength=2,noise=10)
    #
    # data = np.random.random((100,2))
    # plt.figure(1)
    # data_x = [1.15,1.9,3.06,4.66,6.84,7.95]
    # data_y = [1.37,2.4,3.02,3.06,4.22,5.42]
    # data_x = [1.26678499,-0.07140077,-1.58504926,-0.92604551,-0.19716341,0.56154149,-0.15240387,-1.73729316,0.02587862,0.50515503,-0.2329716,1.23257258,0.45911012,0.4427905,-1.320158,0.45941781,-1.92261363,-0.00777128,0.06975579,0.66774405,-0.77344728,-0.50700617,-0.01203364,-0.31200469,-1.43128103,-1.96565898,-1.28665334,-0.25780803,0.69505534,-0.54475871,-0.7309375,-0.5341021,0.36373375,0.68459006,0.982707,0.91102146,-1.00923651,-1.22454187,0.4597288,0.61513739,-0.97844567,0.6996396,-0.0769421,0.63659425,1.26488038,-1.86980068,1.39764272,-0.34819051,2.30307695,0.39168013,0.94930699,0.36837809,0.81247906,0.36867394,0.65587723,-0.01784625,1.26277257,-1.03274957,-1.88013565,0.70166529,-0.3733448,-0.56650197,0.66813404,-0.44904389,1.16646259,0.09903506,-0.56564715,-0.23358104,-1.77532554,0.19072374,-0.2727764,-1.79091993,-0.51099863,0.07629464,0.385568,1.47656912,-1.54348188,-0.38302744,-2.07410931,0.10166255,-1.45264436,0.6450626,0.13585143,0.27290773,1.74678259,1.2132979,-0.19900907,0.10431539,-0.5396724,0.12464576,0.07188719,-1.19344428,1.97713205,0.43536745,-0.17124772,-0.65079267,1.98608624,0.21864734,-0.21478042,-0.19302155]
    # data_y = [84.40796689,-15.88407337,39.94094558,-115.4526636,112.2807292,17.37703113,-78.25167158,176.9867123,-20.43273531,27.38921003,32.91580594,296.3505062,10.73609195,-10.18563021,-14.29549313,82.059927,-82.82780253,188.3646621,75.36426545,183.2538827,-72.74751434,-85.44095819,-108.0078464,-101.8245249,-8.448327979,-148.7988474,23.24159059,26.03972851,103.0533753,-55.02767094,-89.73010796,-72.74283842,171.3882845,190.4818041,124.958446,-2.565187766,83.86821696,-95.84460059,-52.58135788,32.20721574,16.08421704,-60.18510731,-134.872001,-5.125284684,-38.55673434,-38.85799549,42.46442938,-2.842928641,25.39633511,168.0362866,174.9533299,-158.1022726,162.6905448,-16.65189134,14.74452918,-148.4121458,298.1736052,-37.03041916,-72.32022902,34.02486447,112.9059403,-16.93912052,-9.581729508,-25.11322195,-6.582838844,53.41325642,-82.00714601,-152.5003025,-183.1424705,-156.2626441,61.14276994,-209.2834206,-58.54148398,106.1769928,-61.26928832,211.7672416,-231.4273476,-27.82367963,-273.942935,125.8481811,-88.12773576,151.1652129,86.13012587,43.20401786,173.6134098,174.3776762,25.16271339,-34.74284748,-97.4924197,185.3690543,-50.95992354,-63.20567985,91.93467777,-82.31110093,152.8072513,46.45382065,154.9286027,65.4713251,55.86962771,-17.22422762]
    data_x = data_x[0:20]
    data_y = data_y[0:20]
    length = len(data_x)

    for i in xrange(len(data_x)):
        # print str(data_x[i][0]) + "\t" + str(data_y[i])
        plt.plot(data_x[i],data_y[i],'ro')
    # plt.show()

    learn_rate = 0.05
    iteration_times = 5000
    epsilon = 0.0001

    para_list = [0,0]
    error0 = 0
    error1 = 0
    finish_flag = 0

    wucha_list = []

    iteration_i = 0
    while iteration_i < iteration_times:
        wucha_sum = 0
        for j in range(length):
            # print "x is " + "\t" + str(data_x[j][0])
            diff = para_list[0] + data_x[j] * para_list[1] - data_y[j]
            # print "diff:" + "\t" + str(diff)
            wucha_sum += diff ** 2
            if iteration_i == 7:
                print str(para_list[0] + data_x[j] * para_list[1]) + "\t" + str(data_y[j]) + "\t" + str(diff) + "\t" + str(wucha_sum)

            # print para_list
            para_list[0] = para_list[0] - learn_rate * diff
            para_list[1] = para_list[1] - learn_rate * diff * data_x[j]
        print str(iteration_i) + "\t" + str(para_list) + "\t" + str(wucha_sum) + "\t" + str(error0) + "\t" + str(error1)
        # print wucha_list

        wucha_list.append(wucha_sum)
        if abs(para_list[0] - error0) < epsilon and abs(para_list[1] - error1) < epsilon:
            finish_flag = 1
            print "iteration times:" + "\t" + str(iteration_times)
        else:
            error0 = para_list[0]
            error1 = para_list[1]
        # print str(para_list) + "\t" + str(error0) + "\t" + str(error1)
        if finish_flag:
            print "finish_flag is 1"
            break
        iteration_i += 1


    test_x = [i for i in range(10)]
    test_y = [ (para_list[0] + para_list[1] * i) for i in test_x]
    plt.plot(test_x,test_y)
    plt.show()

    plt.figure(2)
    # print len(wucha_list)
    # print wucha_list
    error_x = [i for i in range(len(wucha_list))]
    plt.plot(error_x,wucha_list)
    plt.show()
    print data_x
    print "xxxxxxxxxxxxxxxxxxx"
    for x in data_x:
        print x
    print "yyyyyyyyyyyyyyyyyyy"
    for y in data_y:
        print y

if __name__ == "__main__":
    main()