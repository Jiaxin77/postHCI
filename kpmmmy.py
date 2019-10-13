# -*- coding: utf-8 -*-

import numpy as np
import random
from collections import Counter
#from sklearn.datasets import load_iris
from sklearn import metrics
import pandas as pd

def loadDataSet(fileName):  # 解析文件，按tab分割字段，得到一个浮点数字类型的矩阵
    dataMat = []              # 文件的最后一个字段是类别标签
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(curLine)
        dataMat.append(fltLine)
    return dataMat


def dist(x, y):
    return np.sqrt(sum((x-y)**2))

def sigma(x, y):
    return len(x) - sum(x == y)

def findprotos(data, k):
    m, n = data.shape
    num = random.sample(range(m), k)
    O = []
    C = []
    O_data=np.zeros(shape=(m,n))

    C_data=[]
    for i in range(n):
        print(type(data[0, i]))
       # try:

            # if isinstance(data[0, i], numpy.int32) or isinstance(data[0, i], float):
            #     O.append(i)
            # elif isinstance(data[0, i], str):
            #     C.append(i)
        if (data[0,i].isdigit()):
            O.append(i)
            #O_data.append(float(data[0,i]))
            #elif (data[0,i])
        else:
            C.append(i)
            #C_data.append(data[0,i])
                #raise ValueError("the %d column of data is not a number or a string column" % i)

        #except TypeError as e:
            #print(e)

    O_data = data[:, O].astype(float)
    C_data = data[:, C]
    O_protos = O_data[num, :]
    C_protos = C_data[num, :]

    return O, C, O_data, C_data, O_protos, C_protos

def KPrototypes(data, k, max_iters=10, gamma=0):

    m, n = data.shape
    O, C, O_data, C_data, O_protos, C_protos = findprotos(data, k)

    cluster = None
    clusterShip = []
    clusterCount = {}
    sumInCluster = {}
    freqInCluster = {}
    for i in range(m):
        mindistance = float('inf')
        for j in range(k):
            distance = dist(O_data[i,:], O_protos[j,:]) + \
                gamma * sigma(C_data[i,:], C_protos[j,:])
            if distance < mindistance:
                mindistance = distance
                cluster = j
        clusterShip.append(cluster)
        if  clusterCount.get(cluster) == None:
            clusterCount[cluster] = 1
        else:
            clusterCount[cluster] += 1
        for j in range(len(O)):
            if sumInCluster.get(cluster) == None:
                sumInCluster[cluster] = [O_data[i,j]] + [0] * (len(O) - 1)
            else:
                sumInCluster[cluster][j] += O_data[i,j]
            O_protos[cluster,j] = sumInCluster[cluster][j] / clusterCount[cluster]
        for j in range(len(C)):
            if freqInCluster.get(cluster) == None:
                freqInCluster[cluster] = [Counter(C_data[i,j])] + [Counter()] * (len(C) - 1)
            else:
                freqInCluster[cluster][j] += Counter(C_data[i,j])
            C_protos[cluster,j] = freqInCluster[cluster][j].most_common()[0][0]

    for t in range(max_iters):
        for i in range(m):
            mindistance = float('inf')
            for j in range(k):
                distance = dist(O_data[i, :], O_protos[j, :]) + \
                           gamma * sigma(C_data[i, :], C_protos[j, :])
                if distance < mindistance:
                    mindistance = distance
                    cluster = j
            if clusterShip[i] != cluster:
                oldCluster = clusterShip[i]
                clusterShip[i] = cluster
                clusterCount[cluster] += 1
                clusterCount[oldCluster] -= 1

                for j in range(len(O)):
                    sumInCluster[cluster][j] += O_data[i,j]
                    sumInCluster[oldCluster][j] -= O_data[i,j]
                    O_protos[cluster,j] = sumInCluster[cluster][j] / clusterCount[cluster]
                    O_protos[oldCluster, j] = sumInCluster[oldCluster][j] / clusterCount[oldCluster]

                for j in range(len(C)):
                    freqInCluster[cluster][j] += Counter(C_data[i,j])
                    freqInCluster[oldCluster][j] -= Counter(C_data[i,j])
                    C_protos[cluster,j] = freqInCluster[cluster][j].most_common()[0][0]
                    C_protos[oldCluster,j] = freqInCluster[oldCluster][j].most_common()[0][0]

    return clusterShip


if __name__ == "__main__":

    #iris = load_iris()
    #print("iris.data::::")
    #print(iris.data)
    mydata = np.array(loadDataSet("./mmydatas.txt"))

    X=mydata[:]
    # m, n = X.shape
    # for j in range(n):
    #     X[0,j]=int(X[0,j])
    #     print(type(X[0,j]))
    #X=mydata.astype(int)[:]
    print(type(X[0,2]))
    #X=np.array(mydata[:])
    print("XXXX!!")
    print(X)
    O, C, O_data, C_data, O_protos, C_protos = findprotos(X, 3)
    print(O)
    print("==============")
    print(C)
    print("==============")
    print(O_data)
    print("==============")
    print(C_data)
    print("==============")
    print(O_protos)
    print(O_protos[1,1])
    print("==============")
    print(C_protos)
    cluster = KPrototypes(data=X,k=3, max_iters=30)
    print(cluster)
    s2 = pd.DataFrame(np.concatenate([X, np.array([cluster]).T], axis=1))
    s2.to_csv("D:/国庆学习任务/mydata2.csv")
