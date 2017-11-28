import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs


def distanceNorm(Norm,D_value):
	# initialization
	

	# Norm for distance
	if Norm == '1':
		counter = np.absolute(D_value)
		counter = np.sum(counter)
	elif Norm == '2':
		counter = np.power(D_value,2)
		counter = np.sum(counter)
		counter = np.sqrt(counter)
	elif Norm == 'Infinity':
		counter = np.absolute(D_value)
		counter = np.max(counter)
	else:
		raise Exception('We will program this later......')

	return counter


def chi(x):
	if x < 0:
		return 1
	else:
		return 0


def fit(features,labels,t,distanceMethod = '2'):
	# initialization
	distance = np.zeros((len(labels),len(labels)))
	distance_sort = list()
	density = np.zeros(len(labels))
	distance_higherDensity = np.zeros(len(labels))


	# compute distance
	for index_i in xrange(len(labels)):
		for index_j in xrange(index_i+1,len(labels)):
			D_value = features[index_i] - features[index_j]
			distance[index_i,index_j] = distanceNorm(distanceMethod,D_value)
			distance_sort.append(distance[index_i,index_j])
	distance += distance.T

	# compute optimal cutoff
	distance_sort = np.array(distance_sort)
	cutoff = int(np.round(distance_sort[len(distance_sort) * t]))

	# computer density
	for index_i in xrange(len(labels)):
		distance_cutoff_i = distance[index_i] - cutoff
		for index_j in xrange(1,len(labels)):
			density[index_i] += chi(distance_cutoff_i[index_j])

	# search for the max density
	Max = np.max(density)
	MaxIndexList = list()
	for index_i in xrange(len(labels)):
		if density[index_i] == Max:
			MaxIndexList.extend([index_i])

	# computer distance_higherDensity
	Min = 0
	for index_i in xrange(len(labels)):
		if index_i in MaxIndexList:
			distance_higherDensity[index_i] = np.max(distance[index_i])
			continue
		else:
			Min = np.max(distance[index_i])
		for index_j in xrange(1,len(labels)):
			if density[index_i] < density[index_j] and distance[index_i,index_j] < Min:
				Min = distance[index_i,index_j]
			else:
				continue
		distance_higherDensity[index_i] = Min

	return density,distance_higherDensity,cutoff





###############################################################################################
###############################################################################################
#	Additional Method
###############################################################################################
###############################################################################################

def searchCenter(density,distance_higherDensity):
	
	area = np.multiply(density,distance_higherDensity)
	distance_higherDensity_max = np.max(distance_higherDensity)
	area_max = np.max(area)
	for index_i in xrange(len(distance_higherDensity)):
		if distance_higherDensity[index_i] == distance_higherDensity_max and area[index_i] == area_max:
			return index_i


def kickNoise(center,radius,pos,neg,distanceMethod = '2'):
	# initialization
	distance = np.zeros(len(neg))
	keep_list = list()
	# compute distance
	for index_j in xrange(len(neg)):
		D_value = pos[center] - neg[index_j]
		distance[index_j] = distanceNorm(distanceMethod,D_value)

	# keep the neighbour neg
	for index_j in xrange(len(neg)):
		if distance[index_j] > radius:
			keep_list.append(index_j)

	return keep_list


def test():
	features,labels = make_blobs(centers = 2,center_box = (-10.0,10.0))

	density,distance_higherDensity,distance = fit(features,labels,0.1)
	index = searchCenter(density,distance_higherDensity)



	plt.figure(1)
	dataGraph = plt.subplot(211)
	densityGraph = plt.subplot(212)
	plt.sca(dataGraph)
	for index in range(len(labels)):
		if labels[index] == 0:
			plt.plot(features[index][0],features[index][1],'ro')
		else:
			plt.plot(features[index][0],features[index][1],'go')
	plt.sca(densityGraph)
	for index in range(len(labels)):
		if labels[index] == 0:
			plt.plot(density[index],distance_higherDensity[index],'ro')
		else:
			plt.plot(density[index],distance_higherDensity[index],'go')
	plt.show()

if __name__ == '__main__':
    test()