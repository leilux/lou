#!/usr/bin/env python
#coding: utf-8
import itertools
from cap3 import *

# 5. 请修改K-均值聚类函数 令其在返回聚类结果的同时，一并返回所有数据项彼此之间的距离总和，以及它们各自的中心点位置

# 6. 待完成第5个练习之后 请编写一个函数，令其选择不同的k值来运行K-均值聚类算法 看一看总的距离值是如何随着聚类数量的增加而改变的？当处于哪个位置的时候，聚类数的多少对最终结果的影响才会变得微乎其微？

def kcluster(rows, distance=pearson, k=4):
    # determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) 
            for i in range(len(rows[0]))]

    # create k randomly placed centroids
    clusters = [[random.random()*(ranges[i][1] -ranges[i][0]) for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]

        # find which centroid is the closet for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row): 
                    bestmatch = i
            bestmatches[bestmatch].append(j)

        # if the results are the same as last time, this is complete
        if bestmatches == lastmatches: break
        lastmatches = bestmatches

        # move the cetroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    total_distance = sum(distance(*i) for i in itertools.combinations(clusters, 2))

    return bestmatches, total_distance, clusters

