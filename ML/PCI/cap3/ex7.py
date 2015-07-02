#!/usr/bin/env python
#coding: utf-8
import random
from cap3 import *


def scaledown_2d(data, distance=pearson, rate=0.01):
    n = len(data)

    # 每一对数据项之间的真实距离
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]

    outersum = 0.0

    #随机初始化节点在二维空间中的起始位置
    loc = [[random.random(), random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # 寻找投影后的距离
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x]-loc[j][x], 2) for x in range(len(loc[i]))]))
        # 移动节点
        grad = [[0.0,0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # 误差值等于目标距离与当前距离之间差值的百分比
                errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]
                # 每一个节点都需要根据误差的多少，按比例移离或移向其他节点
                grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
                # 记录总的误差值
                totalerror += abs(errorterm)
        print totalerror

        # 如果节点移动之后的情况变得更糟，则程序结束
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # 根据rate参数与grad值相乘的结果，移动每一个节点
        for k in range(n):
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]

    return loc


def scaledown_1d(data, distance=pearson, rate=0.1):
    n = len(data)

    # 每一对数据项之间的真实距离
    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]

    outersum = 0.0

    #随机初始化节点在一维空间中的起始位置
    loc = [[random.random()] for i in range(n)]
    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # 寻找投影后的距离
        for i in range(n):
            for j in range(n):
                fakedist[i][j] = sqrt(sum([pow(loc[i][x]-loc[j][x], 2) for x in range(len(loc[i]))]))
        # 移动节点
        grad = [[0.0] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # 误差值等于目标距离与当前距离之间差值的百分比
                errorterm = (fakedist[j][k]-realdist[j][k])/realdist[j][k]
                # 每一个节点都需要根据误差的多少，按比例移离或移向其他节点
                grad[k][0] += ((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                #grad[k][1] += ((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm
                # 记录总的误差值
                totalerror += abs(errorterm)
        print totalerror

        # 如果节点移动之后的情况变得更糟，则程序结束
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # 根据rate参数与grad值相乘的结果，移动每一个节点
        for k in range(n):
            loc[k][0] -= rate*grad[k][0]
            #loc[k][1] -= rate*grad[k][1]

    return loc


def scaledown_3d(data, distance=pearson, rate=0.01):
    pass

def draw1d(data, jpeg='mds1d.jpg'):
    r = 20
    c = lambda : random.randint(0,255)
    img = Image.new('RGB', (3500,500), (255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 500 + r
        y = 250
        draw.ellipse((x-r,y-r, x+r, y+r), (c(),c(),c()))
    img.save(jpeg, 'JPEG')


def draw2d(data, labels, jpeg='mds2d.jpg'):
    img = Image.new('RGB', (2000,2000), (255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x,y), labels[i], (0,0,0))
    img.save(jpeg, 'JPEG')

#print '二维形式展现数据'
#blognames, words, data = readfile('blogdata.txt')
#coords = scaledown(data)
#draw2d(coords, blognames, jpeg='blogs2d.jpg')


