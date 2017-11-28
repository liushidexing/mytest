__author__ = 'ligang-s'
#! /usr/bin/env python
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs

def distanceNorm(type,vector_a,vector_b):
    if type == "cos":
        fenzi = np.dot(vector_a,vector_b)
        fenmu_a = np.sum(np.power(vector_a,2)) ** 0.5
        fenmu_b = np.sum(np.power(vector_b,2)) ** 0.5
        fenmu = fenmu_a * fenmu_b
        if fenmu != 0:
            distance = fenzi / fenmu
        else:
            distance = 0
    elif type == "eu":
        distance = np.sum(np.power((vector_a - vector_b),2)) ** 0.5

    return distance

def compute_distance(type,data_array):
    record_num = len(data_array[:,0])
    distance_array = np.zeros([record_num,record_num])
    max_distance = 0
    for i in xrange(record_num):
        for j in xrange(i+1, record_num):
            distance_array[i,j] = distanceNorm(type,data_array[i],data_array[j])
            if distance_array[i,j] > max_distance:
                max_distance = distance_array[i,j]
    distance_array += distance_array.T

    return distance_array,max_distance

def compute_density(distance_array,distance_threshold):
    record_num = len(distance_array[0])
    density_array = np.zeros(record_num)
    max_density = 0
    for i in xrange(record_num):
        for j in xrange(record_num):
            if distance_array[i][j] <= distance_threshold:
                density_array[i] += 1
            if density_array[i] > max_density:
                max_density = density_array[i]
                max_density_index = i
    return density_array,max_density_index

def compute_density_distance(density_array, max_density_index, max_distance, distance_array):
    record_num = len(density_array)
    distance_result = np.zeros(record_num)
    for i in xrange(record_num):
        if i == max_density_index:
            distance_result[i] = max_distance
        else:
            min_distance = 100000000
            for j in xrange(record_num):
                if density_array[j] > density_array[i]:
                    if distance_array[i][j] < min_distance:
                        min_distance = distance_array[i][j]
            distance_result[i] = min_distance

    return distance_result

if __name__ == "__main__":
    features,labels = make_blobs(centers = 2,center_box = (-10.0,10.0))

    distance_array, max_distance = compute_distance("eu",features)
    density_array, max_density_index = compute_density(distance_array,0.5)
    distance_result = compute_density_distance(density_array, max_density_index, max_distance, distance_array)

    final_result = np.vstack((density_array,distance_result))

    # p
    print distance_array
    print density_array
    plt.figure(1)
    dataGraph = plt.subplot(211)
    densityGraph = plt.subplot(212)
    plt.sca(dataGraph)
    for index in range(len(labels)):
        if labels[index] == 0:
            plt.plot(features[index][0],features[index][1],'ro')
        else:
            plt.plot(features[index][0],features[index][1],'go')
    print final_result.shape
    print final_result
    print "final_result"
    plt.sca(densityGraph)
    for index in range(len(labels)):
        print str(final_result[0][index]) + "\t" +str(final_result[1][index])
        if labels[index] == 0:
            plt.plot(final_result[0][index],final_result[1][index],'ro')
        else:
            plt.plot(final_result[0][index],final_result[1][index],'go')
            # plt.plot(density_array[index],distance_array[index],'go')
    plt.show()