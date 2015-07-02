#!/usr/bin/env python
#coding: utf-8

#搜索与排名 -- Searching and Ranking

# 对信息检索（information retrieval）中一部分关键概念加以解释
# 完整地介绍一个搜索引擎的构造过程。
# 检索网页（crawl）、建立索引、对网页进行搜索，以及以多种不同方式对搜索的结果进行排名

##搜索引擎的组成 -- what's in a search engine?
                                                                 
#searchengine.py
class carwler:
    # 初始化crawler类并传入数据库名称
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    # 辅助函数，用于获取条目的id，并且如果条目不存在，就将其加入数据库中
    def getentryid(self, table, filed, value, createnew=True):
        cur = self.execute(
            "select rowid from %s where %s='%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
                "insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    # 为每个网页建立索引
    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        print 'Indexing ' + url
        # 获取每个单词
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # 得到URL的id
        urlid = self.getentryid('urllist', 'url', url)

        # 将每个单词与该url关联
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)' %(urlid, wordid,i)


    # 从一个HTML网页中提取文字（不带标签的）
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

    # 根据任何非空白字符进行分词处理
    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    # 如果url已经建过索引，则返回true
    def isindexed(self, url):
        u = self.con.execute(
            "select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            # 检查它是否已经被检索过了
            v = self.con.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None: return True
        return False


    # 添加一个关联两个网页的链接
    def addlinkref(self, urlFrom, urlTo, linkText):
        words = self.separateWords(linkText)
        fromid = self.getentryid('urllist','url',urlFrom)
        toid = self.getentryid('urllist','url',urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))


    # 从一小组网页开始进行广度优先搜索，直至某一给定深度，
    # 期间为网页建立索引
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'could not open %s'%page
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'")!=-1: continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages = newpages

    # 创建数据库表
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location')
        self.con.execute('create link(fromid integer,toid integer)')
        self.con.execute('create linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')

        self.dbcommit()


##一个简单的爬虫程序 -- A Simple Crawler

# http://segaran.com/wiki

###Using urllib2

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin

# 构造一个单词列表，这些单词将被忽略
ignorewords = set(['the','of','to','and','a','in','is','it'])

###爬虫程序的代码 -- Crawler Code

# 广度优先的搜索方式
# crawler.crawl(self, pages, depth=2)

###建立索引 -- Building the Index

import sqlite3 as sqlite
# crawler.__init__(self, dbname)
# crawler.__del__(self)
# crawler.dbcommit(self)


###建立数据库schema -- Setting Up the Schema
     
#     +-------+      +--------+          +---------+
#     | link  |      | urllist|          | pagerank|
#     |-----  |  +---|----    |--------+ |-------- |
#   +-|rowid  |  |+--|rowid   |-----+  +-|urlid    |
#   | |fromid |--+|  |url     |     |    |score    |
#   | |toid   |---+  +--------+     |    +---------+
#   | +-------+                     |  
#   |                               |  
#   |                               |    +-------------+
#   | +----------+     +---------+  |    | wordlocation|
#   | | linkwords|     | wordlist|  |    |----------   |
#   | |--------  |     |-------  |  +----|urlid        |
#   | |wordid    |-----|rowid    |-------|wordid       |
#   +-|linkid    |     |word     |       |location     |
#     +----------+     +---------+       +-------------+                  

# createindextables(self)

#print 'setting up the schema'
#crawler = crawler('searchindex.db')
#crawler.createindextables()


###在网页中查找单词 -- Finding the Words on a page

# crawler.gettextonly(self, soup)
# crawler.separatewords(self, text)
# 中文分词：jieba
# 词干提取算法（stemming algorithm） 
#    http://www.tartarus.org/~martin/PorterStemmer/index.html
#    Porter Stemmer

###加入索引 -- Adding to the Index

# crawler.addtoindex(self, url, soup)
# crawler.getentryid(self, table, field, value,createnew=True)
# crawler.isindexed(self, url)


#print 'adding to the index'
#crawler = crawler('searchindex.db')
#pages = ['http://segaran.com/wiki/Categorical_list_of_programming_languages.html']
#crawler.crawl(pages)

# 也可以从 http://segaran.com/db/searchindex.db下载 searchindex.db


##查询 -- Querying

class searcher:
    def __init__(self, dbname):
        self.mynet = searchnet('nn.db')
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self, q):
        '''接受一个查询字符串作为参数，并将其拆分为多个单词，然后构造一个SQL查询，只查找那些包含所有不同单词的URL
        example:
          select w0.urlid, w0.location, w1.location
          from wordlocation w0, wordlocation w1
          where w0.urlid=w1.urlid
          and w0.wordid=10
          and w1.wordid=17
        '''
        # 构造查询的字符串
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # 根据空格拆分单词
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # 获取单词的ID
            wordrow = self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber-1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1

        # 根据各个组分，建立查询
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]
        # rows[w0.urlid w0.location w1.location]
        return rows, wordids

    def getscoredlist(self, rows, wordids):
        totalscores = {row[0]:0 for row in rows}
        
        # 此处是稍后放置评价函数的地方
        weights = [
            (1.0, self.frequencyscore(rows)),
            (1.0, self.locationscore(rows)),
            (1.0, self.distancescore(rows)),
            (1.0, self.pagerankscore(rows)),
            (1.0, self.linktextscore(rows, wordids)),
            (1.0, self.nnscore(rows, wordids)),
        ]

        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight*scores[url]

        return totalscores

    def geturlname(self, id):
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self, q):
        '''查询结果'''
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows, wordids)
        rankedscores = sorted([(score, url) for (url, score) in scores.items()], reverse=True)
        for (score, urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score, self.geturlname(urlid))
        # 此结果可以被直接传入searchnet.trainquery(wordids, urlids, selectedurl)
        return wordids, [r[1] for r in rankedscores[0:10]]

    def normalizescores(self, scores, smallIsBetter=False):
        '''将结果归一化处理，并返回一个介于0和1之间的值'''
        vsmall = 0.00001 # 避免除零
        if smallIsBetter:
            minscore = min(scores.values())
            return {u: float(minscore)/max(vsmall, i) for (u, i) in scores.items()}
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return {u: float(c)/maxscore) for (u,c) in scores.items()}

    def frequencyscore(self, rows):
        '''单词频度'''
        counts = {row[0]: 0 for row in rows}
        for row in rows: counts[row[0]] += 1
        return self.normalizescores(counts)

    def locationscore(self, rows):
        '''文档位置'''
        locations = {row[0]: 1000000 for row in rows}
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc
        return self.normalizescores(locations, smallIsBetter=True)

    def distancescore(self, rows):
        '''单词距离'''
        # 如果仅有一个单词，则得分都一样
        if len(rows[0]) <= 2: return {row[0]: 1.0 for row in rows}

        # 初始化字典，并填入一个很大的数
        mindistance = {row[0]: 1000000 for row in rows}

        for row in rows:
            dist = sum(abs(row[i]-row[i-1]) for i in range(2, len(row)))
            if dist < mindistance[row[0]]: mindistance[row[0]] = dist
        return self.normalizescores(mindistance, smallIsBetter=True)

    def inboundlinkscore(self, rows):
        '''inbound link 简单计数'''
        uniqueurls = set([row[0] for row in rows])
        inboundcount = {u: self.con.execute(
            'select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls}
        return self.normalizescores(inboundcount)

    def calculatepagerank(self, iterations=20):
        # 清除当前的PageRank表
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')

        # 初始化每个url，令其PageRank值为1
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

        for i in range(iterations):
            print 'Iteration %d' % i
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15
                # 循环遍历指向当前网页的所有其他网页
                for (linker,) in self.con.execute(
                    'select distinct fromid from link where toid=%d' % urlid):
                    # 得到链接源对应网页的PageRank值
                    linkingpr = self.con.execute(
                        'select score from pagerank where urlid=%d' % linker).fetchone()[0]

                    # 根据链接源，求得总的链接数
                    linkingcount = self.con.execute(
                        'select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85*(linkingpr/linkingcount)
                self.con.execute(
                    'update pagerank set score=%f where urlid=%d' % (pr, urlid))
            self.dbcommit()

    def pagerankscore(self, rows):
        '''PageRank'''
        pageranks = {row[0]: self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0] for row in rows}
        maxrank = max(pageranks.values())
        normalizescores = {u: float(l)/maxrank for (u,l) in pageranks.items()}
        return normalizescores

    def linktextscore(self, rows, wordids):
        '''链接文本 + pagerank'''
        linkscores = {row[0]: 0 for row in rows}
        for wordid in wordids:
            cur = self.con.execute('select link.fromid, link.toid from linkwords, link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid, toid) in cur:
                if toid in linkscores:
                    pr = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid] += pr
        maxscore = max(linkscores.values())
        normalizescores = {u:float(l)/maxscore for (u,l) in linkscores.items()}
        return normalizescores

    def nnscore(self.rows, wordids):
        # 获取一个由唯一的URL ID构成的有序列表
        urlids = [urlid for urlid in set([row[0] for row in rows])]
        nnres = self.mynet.getresult(wordids, urlids)
        scores = {urlids[i]: nnres[i] for i in range(len(urlids))}
        return self.normalizescores(scores)


##基于内容的排名 -- Content-Based Ranking

# 对几种只依据查询条件和网页内容进行评价计算的方法进行考查。包括以下三种：
# 1. 单词频度
# 2. 文档位置：文档的主题有可能会出现在靠近文档的开始处
# 3. 单词距离：多个单词在文档中出现的位置应该靠得很近

# searcher.getscoredlist(self, rows, wordids)
# searcher.geturlname(self, id)
# searcher.query(self, q)


###归一化函数 -- Normalization Function

# searcher.normalizescores(self, scores, smallIsBetter=0)


###单词频度 -- Word Frequency

# searcher.frequencyscore(self, rows)


###文档位置 -- Document Location

# searcher.locationscore(self, rows)


###单词距离 -- Word Distance

# searcher.distancescore(self, rows)


##利用外部回指链接 -- Using Inbound Links

###简单计数 -- Simple Count

# searcher.inboundlinkscore(self, rows)


###PageRank算法 -- The PageRank Algorithm

# 网页的重要性依据指向该网页的所有其他网页的重要性，以及这些网页中所包含的链接数求得
# PageRank计算的是某个人在任意次链接点击之后到达某一网页的可能性。
# 如果某个网页拥有来自其他热门网页的外部回指链接越多，人们无意间到达该网页的可能性也就越大.
# 如果用户始终不停地点击，那么他们终将到达每一个网页，但是绝大多数人在浏览一段时间后都会停止点击。
# 为了反映这一情况，PageRank还使用了一个值为0.85的阻尼因子，用以指示用户持续点击每个网页中链接的概率为85%。

#        +---+      +---+      +---+
#    <---| B |      | A |      | C |----->
#    <---|   |----> |   | <----|   |----->
#    <---|.5 |      | ? |      |.7 |----->
#        +---+      +---+      +---+
#                     ^
#                     |
#                   +---+
#                   | D |
#                   |.2 |
#                   +---+
#  PR(A) = 0.15 + 0.85 * (PR(B)/links(B) + PR(C)/links(C) + PR(D)/links(D))
#        = 0.15 + 0.85 * (0.5/4 + 0.7/5 + 0.2/1)
#        = 0.15 + 0.85 * (0.125 + 0.14 + 0.2)
#        = 0.54525

# 如何对一组还没有PageRank值的网页进行PageRank计算？
# 解决：为所有的PageRank都设置一个任意的初始值，然后反复计算，迭代若干次。
#       每次迭代期间每个网页的PageRank值将会越来越接近真实值

# searcher.calculatepagerank(self, iterations=20)
# searcher.pagerankscore(self, rows)


###利用链接文本 -- Using the Link Text

# searcher.linktextscore(slef, rows, wordids)


##从点击行为中学习 -- Learning from Clicks

# 记录用户点击查询结果的情况，并利用这一信息来改进搜索结果的排名
# 构造一个人工神经网络（artificail neural network）
# 向其提供：提供查询条件中的单词，返回给用户的搜索结果，以及用户的点击决策，然后再对其加以训练。

###一个点击跟踪网络的设计 -- Design of a Click-Tracking Network

# 神经网络都以一组节点（神经元）构成，并且彼此相连。
# 将要介绍的为多层感知机（multilayer perceptron，MLP）网络。
# 此类网络有多层神经元构造而成，
# 其中第一层神经元接受输入，本例中，即用户输入的单词
# 最后一层神经元给予输出，本例中，即一个涉及被返回的不同URL的权重列表
# 神经网络可以有多个中间层，因为外界无法直接与其交互，所以该中间层被称为隐藏层，其职责是对输入进行组合。

# 本节用一种称为反向传播（backpropagation）的算法对网络进行训练

# 为什么要用神经网络这样的复杂技术？ 它能根据与其他查询的相似度情况，对以前从未见过的查询结果做出合理的猜测。


###设置数据库 -- Setting Up the Database

# 数据表
# hiddennode(create_key)：代表隐藏层的数据表
# wordhidden(fromid,toid,strength)：单词层到隐藏层的连接状况
# hiddenurl(fromid,toid,strength)：隐藏层与输出层连接状况

# nn.py
from math import tanh
import sqlite3 as sqlite

class searchnet:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid,toid,strength)')
        self.con.execute('create table hiddenurl(fromid,toid,strength)')
        self.con.commit()
    
    def getstrength(self, fromid, toid, layer):
        if layer == 0: talbe = 'wordhidden'
        else: table = 'hiddenurl'
        res = self.con.execute('select strength from %s where fromid=%d and toid=%d' % (table, fromid, toid)).fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        '''判断连接是否已存在，并利用新的强度值更新连接或创建连接'''
        if layer == 0: table = 'wordhidden'
        else: table = 'hiddenurl'
        res = self.con.execute('select rowid from %s where fromid=%d and toid=%d' % (table,fromid,toid)).fetchone()
        if res == None:
            self.con.execute('insert into %s (fromid, toid, strength) values (%d, %d, %f)' % (table, fromid, toid, strength))
        else:
            rowid = res[0]
            self.con.execute('update %s set strength=%f where rowid=%d' % (table, strength, rowid))

    def generatehiddennode(self, wordids, urls):
        '''每传入一组从前未见过的单词组合，就会在隐藏层建立一个新的节点，
        随后会为单词与隐藏节点之间，及查询节点与url结果之间建立有默认权重的连接
        '''
        if len(wordids) > 3: return None
        # 检查我们是否已经为这组单词建好了一个节点
        createkey = '_'.join(sorted([str(wi) for wi in wordids]))
        res = self.con.execute(
            "select rowid from hiddennode where create_key='%s'" % createkey).fetchone()

        # 如果没有，则建立之
        if res == None:
            cur = self.con.execute(
                "insert into hiddennode (create_key) values ('%s')" % createkey)
            hiddenid = cur.lastrowid
            # 设置默认权重
            for wordid in wordids:
                self.setstrength(wordid, hiddenid, 0, 1.0/len(wordids))
            for urlid in urls:
                self.setstrength(hiddenid, urlid, 1, 0.1)
            self.con.commit()

    def getallhiddenids(self, wordids, urlids):
        '''从隐藏层中找出与某项查询相关的所有节点，
        其他节点不会用来判断结果或训练网络，没必要将它们包含在内
        '''
        ll = {}
        for wordid in wordids:
            cur = self.con.execute(
                'select toid from wordhidden where fromid=%d' % wordid)
            for row in cur: ll[row[0]] = 1
        for urlid in urlids:
            cur = self.con.execute(
                'select fromid from hiddenurl where toid=%d' % urlid)
            for row in cur: ll[row[0]] = 1
        return ll.keys()

    def setupnetwork(self, wordids, urlids):
        '''利用数据库中保存的信息，建立起包括所有当前权重值在内相应网络
        '''
        # 值列表
        self.wordids = wordids
        self.hiddenids = self.getallhiddenids(wordids, urlids)
        self.urlids = urlids

        # 节点输出
        self.ai = [1.0] * len(self.wordids)
        self.ah = [1.0] * len(self.hiddenids)
        self.ao = [1.0] * len(self.urlids)

        # 建立权重矩阵
        self.wi = [[self.getstrength(wordid, hiddenid, 0)
            for hiddenid in self.hiddenids] 
            for wordid in self.wordids]
        self.wo = [[self.getstrength(hidden, urlid, 1)
            for urlid in self.urlids]
            for hiddenid in self.hiddenids]

    def feedforward(self):
        '''算法接受一列输入，将其推入网络，然后返回所有输出层节点的输出。
        所有来自输入层节点的输出结果都将总是1
        只要持续不断地将上一层的输出作为下一层的输入，我们可以很容易地对网络加以扩展，令其包含更多的层
        '''
        # 查询单词是仅有的输入
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # 隐藏层节点的活跃程度
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # 输出层节点的活跃程度
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward()

    def backPropagate(self, targets, N=0.5):
        '''反向传播，按照正向传播的计算方法，反向传回
        对于输出层中的每个节点：
        1. 计算节点当前输出结果与期望结果之间的差距
        2. 利用dtanh函数确定节点的总输入需要如何改变
        3. 改变每个外部回指链接的强度值，其值与链接的当前强度及学习速率（learning rate）成一定比例
        对于每个隐藏层中的节点：
        1. 将每个输出链接（output link）的强度值乘以其目标节点所需的改变量，在累加求和，从而改变节点的输出结果
        2. 利用dtanh函数确定节点的总输入需要如何改变
        3. 改变每个输入链接（input link）的强度值，其值与链接的当前强度及学习速率成一定比例
        '''
        # 计算输出层的误差
        output_deltas = [0.0] * len(self.urlids)
        for k in range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k]) * error

        # 计算隐藏层的误差
        hidden_deltas = [0.0] * len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j]) * error

        # 更新输出权重
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change

        # 更新输入权重
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change

    def trainquery(self, wordids, urlids, selectedurl):
        # 如果必要，生成一个隐藏节点
        self.generatehiddennode(wordids, urlids)

        self.setupnetwork(wordids, urlids)
        self.feedforward()
        targets = [0.0] * len(urlids)
        targets[urlids.index(selectedurl)] = 1.0
        self.backPropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        '''将权重信息wi，wo更新到数据库'''
        # set them to database values
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i],self. hiddenids[j],0,self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k])
        self.con.commit()

#print '设置数据库'
#mynet = searchnet('nn.db')
#mynet.maketables()
#wWorld, wRiver, wBank = 101, 102, 103
#uWordBank, uRiver, uEarth = 201, 202, 203
#mynet.generatehiddennode([wWorld, wBank], [uWordBank, uRiver, uEarth])

###前馈法 -- Feeding Forward

# 选择一个函数，用以指示每个节点对输入的响应程度。
# 反双曲正切变换函数（hyperbolic tangent，tanh）
# 特点：当输入接近0时，输出便开始快速爬高
#       当输入为2时，输出几乎停留在1的位置上不再变化
# 这是一类S型函数（sigmoid function），所有该类型的函数都会呈现这样的S形状。
# 神经网络几乎总是利用S型函数来计算神经元的输出

# searchnet.getallhiddenids(self, wordids, urlids)
# searchnet.setupnetwork(self, wordids, urlids)
# searchnet.feedforward(self)
# searchnet.getresult(self, wordids, urlids)


###利用反向传播法进行训练 -- Training with Backpropagation

# 反向传播法：该算法在调整权重值时是沿着网络反向行进的。
# >因为在对网络进行训练时，我们始终都知道每个输出层节点的期望输出，
# >所以在这种情况下，如果用户点击了预期的结果，则它应该朝着1的方向推进，否则就朝着0的方向推进。

# 修改某一节点输出结果的唯一方法，是修改针对该节点的总输入。
# 那么该如何改变总的输入？ 
# >训练算法须要知道tanh函数在其当前输出级别上的斜率（slope）。
# >当输出为0.0时，斜率就会非常的‘陡’，只改变一点点输入就会获得很大的变化
# >如果输入接近-1或1，则改变输入对输出构成的影响就会变得越来越小。

# sinh(x) = (e**x - e**(-x)) / 2
# cosh(x) = (e**x + e**(-x)) / 2
# tanh(x) = sinh(x) / cosh(x)
# coth(x) = 1 / tanh(x)
# sech(x) = 1 / cosh(x)
# csch(x) = 1 / sinh(x)
def dtahh(y):
    return 1.0 -y*y

# searchnet.backPropagate(self, targets, N=0.5)
# searchnet.trainquery(self, wordids, urlids, selectedurl)
# searchnet.updatedatabase(self)


###Training Test

#print 'training test'
#allurls = [uWordBank, uRiver, uEarth]
#for i in range(30):
#    mynet.trainquery([wWorld, wBank], allurls, uWordBank)
#    mynet.trainquery([wRiver, wBank], allurls, uRiver)
#    mynet.trainquery([wWorld], allurls, uEarth)

# 神经网络不仅掌握了URL与查询的联系，还了解到一次特定查询中，哪些单词是重要的 -- 这些信息是单纯从查询与URL的关联关系中无法获取的


###Connecting to the Search Engine

# searcher.nnscore(self, rows, wordids)

##Exercises

# 1. **分词** separatewords方法目前将任何非字母和非数字字符都当作了分隔符，这意味着它无法为诸如'C++','$20','Ph.D','617-555-1212'这样的词条建立正确的索引。更好的分词方法是什么呢？使用空白符作为分隔符是否可以？请编写一个更好的分词函数

# 2. **布尔操作符** python OR perl这样的搜索条件。一个OR查询可以通过分别执行两次查询后在对结果进行组合的方式来实现，但是对与'python AND (program OR code)'又该如何处理呢？请修改查询方法以支持某些基本的布尔操作。

# 3. **精确匹配** 编写一个新的getrows函数，返回顺序必须与查询条件中的单词顺序相同，而且中间不允许夹杂任何其他的单词的精确匹配结果

# 4. **长文/短文搜索** 编写一个权重函数，该函数将根据传入的参数，倾向与给出较长或较短的文档。如查找有关疑难问题的长篇，或查找命令行工具的快速参考短篇。

# 5. **单词频度偏好** ‘单词计数’的度量方法更偏向与较长的文档，因为篇幅较长的文档拥有更多的单词，而且因此也更有可能包含要搜索的单词。请编写一个新的度量方法，以文档中单词数量的百分比作为频度进行计算。

# 6. **外部回指链接搜索** ? 不明白什么意思

# 7. **不同的训练选项** 对神经网络进行训练时，我们使用的一组0值代表所有用户没有点击的URL，而用1来代表用户点击过的URL。请修改函数，令其能够允许用户对结果给予从1到5的评价 searchnet.trainquery()

# 8. **附加层** 目前的神经网络只有一个隐藏层。请修改searchnet类， 令其支持任意数量的隐藏层。关于层数，我们可以在初始化时加以指定。 searchnet.generatehiddennode()
