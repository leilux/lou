#!/usr/bin/env python
#coding: utf-8

#发现组群 -- Discovering Groups

# 数据聚类：一种用以寻找紧密相关的事、人或观点，并将其可视化的方法。
# 1. 从各种不同的来源中构造算法所需的数据
# 2. 两种不同的聚类算法
# 3. 更多有关距离度量（distance metrics）的知识
# 4. 简单的图形可视化代码，用以观察所生成的群组
# 5. 如何将异常复杂的数据集投影到二维空间中

##监督学习和无监督学习 -- Supervised versus Unsupervised Learning

# 监督学习法：利用样本输入和期望输出来学习如何预测的技术
# 如：神经网络、决策树、支持向量机，及贝叶斯过滤

# 无监督学习：不是利用带有正确答案的样本数据进行训练。它
#             们的目的是要在一组数据中找寻某种结构，而这
#             些数据本身并不是我们要找的答案。
# 如：聚类，负矩阵因式分解，自组织映射


##单词向量 -- Word Vectors

# 为聚类算法准备数据常见的做法是定义一组公共的数值型属性，可以利用这些属性对数据项进行比较。

###对博客用户进行分类 -- Pigeonholing the Bloggers

# 根据单词出现的频度对博客进行聚类。

###对订阅源中的单词进行计数 -- Counting the Words in a feed

# generatefeedvector.py
#import feedparser
import re

# returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    # parse the feed
    d = feedparser.parse(url)
    wc = {}

    # loop over all the entries
    for e in d.entries:
        summary = e.summary if 'summary' in e else\
                  e.description
        # extract a list of words
        words = getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return d.feed.title, wc

def getwords(html):
    # remove all the HTML tags
    txt = re.compile(r'<[^>]+>').sub('', html)

    # split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # convert to lowercase
    return [word.lower() for word in words if word != '']

def generatefeedvector():
    '''遍历订阅源并生成数据集'''
    # 生成针对每个博客的单词统计，及出现这些单词的博客数
    apcount = {}
    wordcounts = {}
    feedlist = [line for line in file('feedlist.txt')]
    for feedurl in feedlist:
        title, wc = getwordcounts(feedurl)
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1
    
    # 建立一个单词列表，实际用于针对每个博客的单词计数
    # 10% ～ 50%
    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if farc > 0.1 and farc < 0.5: wordlist.append(w)
    
    
    out = file('blogdata.txt', 'w')
    out.write('Blog')
    for word in wordlist: out.write('\t%s' % word)
    out.write('\n')
    for blog, wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc: out.write('\t%d' % wc[word])
            else: out.write('\t0')
        out.write('\n')


##分级聚类 -- Hierarchical Clustering

# 通过连续不断地将最为相似的群组两两合并，来构造出一个群组的层级结构。其中的每个群组都是从单一元素开始的。

# 树状图(dendrogram) 分级聚类的一种可视化形式

# clusters.py
def readfile(filename):
    lines = [line for line in file(filename)]

    # first line is column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # first column in each row is the rowname
        rownames.append(p[0])
        # the data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


from math import sqrt

def pearson(v1, v2):
    # simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # sums of the squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    # sum of the products
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    # calculate r (Pearson score)
    num = pSum - (sum1*sum2/len(v1))
    den = sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den == 0: return 0

    return 1.0 - num/den

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # clusters are initially just the rows
    clust = [bicluster(rows[i],id=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate the average of the two clusters
        mergevec = [
            (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, 
                               left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest,
                               id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


#print '调用hcluster方法'
#blognames, words, data = readfile('blogdata.txt')
#clust = hcluster(data)


def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    print ' '*n,
    if clust.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        print clust.id if labels==None else labels[clust.id]

    # now print the right and left branches
    if clust.left != None: printclust(clust.left, labels=labels, n=n+1)
    if clust.right!= None: printclust(clust.right, labels=labels, n=n+1)


#print '调用printclust'
#printclust(clust, labels=blognames)


##绘制树状图 -- Drawing the Dendrogram

from PIL import Image, ImageDraw

def getheight(clust):
    # is this an endpoint? then the height is just 1
    if clust.left == None and clust.right == None: return 1

    # otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
    # the distance of an endpoint is 0.0
    if clust.left == None and clust.right == None: return 0

    # the distance of branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # height and width
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling = float(w-150)/depth

    # create a new image with a white background
    img = Image.new('RGB', (w,h), (255,255,255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255,0,0))

    # draw the first node
    drawnode(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, 'JPEG')


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left)*20
        h2 = getheight(clust.right)*20
        top = y - (h1 + h2)/2
        bottom = y + (h1 + h2)/2
        # line length
        ll = clust.distance * scaling
        # vertical line from this cluster to children
        draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255,0,0))

        # horizontal line to left item
        draw.line((x, top+h1/2, x+ll, top+h1/2), fill=(255,0,0))

        # horizontal line to right item
        draw.line((x, bottom-h2/2, x+ll, bottom-h2/2), fill=(255,0,0))

        # call the function to draw the left and right nodes
        drawnode(draw, clust.left, x+ll, top+h1/2, scaling, labels)
        drawnode(draw, clust.right, x+ll, bottom-h2/2, scaling, labels)
    else:
        # if this is an endpoint, draw the item label
        draw.text((x+5,y-7), labels[clust.id], (0,0,0))

#print '生成图片'
#drawdendrogram(clust, blognames, jpeg='blogclust.jpg')

##列聚类 -- Column Clustering

def rotatematrix(data):
    '''使data的每行表示某个单词在每篇博客中出现的次数'''
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

#print '列聚类 -- 画图'
#rdata = rotatematrix(data)
#wordclust = hcluster(rdata)
#drawdendrogram(wordclust, labels=words, jpeg='wordclust.jpg')

# 聚类有一点很重要：当数据项的数量比变量多的时候，出现无意义的聚类的可能性就会增加?
# 单词聚类：显示了，人们在博客中探讨在线服务或与Internect相关的话题时，经常会用到的一组词汇。
# 我们可能会找到一些反映使用模式（usage patterns）的聚类，如fact，us，say，very及think，这些单词说明博客的写作风格是偏主观的（opinionated）

# 分级聚类的缺点：
# 1. 在没有额外投入的情况下，树形视图是不会真正将数据拆分成不同组的
# 2. 该算法的计算量非常惊人 n**2 - n - 1 = O(n**2)

##K-均值聚类 -- K-Means Clustering

# K-均值聚类：预先告诉算法希望生成的聚类数量，然后算法会根据数据的结构状况来确定聚类的大小。
# 首先会随机确定k个中心位置（位于空间中代表聚类中心的点）# 然后将各个数据项分配给最临近的中心点。
# 分配完成后，聚类的中心会移到分配给该聚类的所有节点的平均位置处
# 整个分配过程重新开始，一致重复，直到分配过程不再产生变化为止。

import random

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

    return bestmatches

#print 'k-means'
#kclust = kcluster(data, k=10)
#print [blognames[r] for r in kclust[0]]

##针对偏好的聚类 -- Clusters of Preferences

###获取数据和准备数据 -- Getting and Perparing the Data

###Beautiful Soup

###收集来自Zebo的结果 -- Scraping the Zebo Results

# downloadzebodata.py
def downloadzebodata():
    from bs4 import BeautifulSoup
    import urllib2
    import re
    chare = re.compile(r'[!-\.&]')
    itemowners = {}
    
    # words to remove
    dropwords = ['a','new','some','more','my','own','the','many','other','another']
    
    currentuser = 0
    for i in range(1,51):
        # url for the want search page
        c = urllib2.urlopen(
            'http://member.zebo.com/Main?event_key=USERSEARCH&wiowiw=wiw&keyword=car&page=%d'%(i))
        soup = BeautifulSoup(c.read())
        for td in soup('td'):
            # find the table cells of bgverdanasmall class
            if ('class' in dict(td.attrs) and td['class'] == 'bgverdanasmall'):
                items = [re.sub(chare, '', a.contents[0].lower()).strip() for a in td('a')]
                for item in items:
                    # remove extra words
                    txt = ' '.join([t for t in item.split(' ') if t not in dropwords])
                    if len(txt) < 2: continue
                    itemowners.setdefault(txt, {})
                    itemowners[txt][currentuser] = 1
                currentuser += 1
    
    out = file('zebo.txt', 'w')
    out.write('Item')
    for user in range(0, currentuser): out.write('\tU%d' % user)
    out.write('\n')
    for item, owners in itemowners.items():
        if len(owners) > 10:
            out.write(item)
            for user in rnage(0, currentuser):
                if user in owners: out.write('\t1')
                else: out.write('\t0')
            out.write('\n')


###定义距离度量标准 -- Defining a Distance Metric

# tanimoto系数（tonimoto coefficient）：它代表的是交集与并集的比率

def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0

    for i in range(len(v1)):
        if v1[i] != 0: c1 += 1 # in v1
        if v2[i] != 0: c2 += 1 # in v2
        if v1[i] != 0 and v2[i] != 0: shr += 1 # in both

    return 1.0 - (float(shr)/(c1+c2-shr))


###对结果进行聚类 -- Clustering Results

#wants, people, data = readfile('zebo.txt')
#clust = hcluster(data, distance=tanimoto)
#drawdendrogram(clust, wants)

##以二维形式展现数据 -- Viewing Data in Two Dimensions

# 多维缩放（multidimensional scaling）：为数据集找到一种二维表达形式

def scaledown(data, distance=pearson, rate=0.01):
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


##有关聚类的其他事宜 -- Other Things to Cluster


##Exercises

# 1. 利用第2章中的del.icio.us API，构造一个适合聚类的标签数据集 针对该数据集分别运行分级聚类算法和K-均值聚类算法 

# 2. 请修改解析博客的代码，以实现针对每个文章条目（entries）而非整个博客的聚类 来自同一博客的不同条目能否聚类在一起？拥有相同日期信息的条目又如何？

# 3. 请尝试使用实际距离，（即毕达哥拉斯距离）对博客进行聚类 这样会对结果产生什么样的影响呢？

# 4. 找到曼哈顿（manhattan）距离的定义 为其编写一个函数，看看它是如何影响Zebo数据集的结果的。

# 5. 请修改K-均值聚类函数 令其在返回聚类结果的同时，一并返回所有数据项彼此之间的距离总和，以及它们各自的中心点位置

# 6. 待完成第5个练习之后 请编写一个函数，令其选择不同的k值来运行K-均值聚类算法 看一看总的距离值是如何随着聚类数量的增加而改变的？当处于哪个位置的时候，聚类数的多少对最终结果的影响才会变得微乎其微？

# 7. 在两个维度上的多维缩放易于打印 不过这项技术也可以用于任意数量的维度。请尝试修改代码，以实现在一个维度上的缩放（即所有点都在一条直线上）。再尝试令其支持三个维度。
