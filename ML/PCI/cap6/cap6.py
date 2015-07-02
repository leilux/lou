##文档过滤 -- Document Filtering

本章介绍如何依据内容对文档进行分类，文档分类是机器智能（machine intelligence）的一个应用。

例子：

1. 垃圾邮件过滤
2. 将来自某一RSS订阅源的内容项目自动过滤到不同的分类中

###过滤垃圾信息 -- Filtering Spam

基于规则的分类器（rule-based classifier），使用时会有人事先设计好一组规则，用以指明某条信息是否属于垃圾信息。

存在的问题是

1. 垃圾信息制造者知道规则后，就可以绕开过滤器
2. 是否被当作垃圾信息很大程度上因其所面对的读者和张贴位置的不同而不同。

解决：程序在开始阶段逐渐收到更多消息之后，根据人们提供给它的有关哪些是垃圾邮件，哪些不是垃圾邮件的信息，不断地进行学习。通过这样的方式，我们可以分别为不同的用户、群组或网站建立起各自的应用实例和数据集，它们对垃圾信息的界定将逐步形成自己的观点。
 
###文档和单词 -- Documents and Words

分类器需要用某些特征来对不同的内容项进行分类。所谓特征，是指任何可以用来判断内容中具备或缺失的东西。
在对文档进行分类时，内容即是文档，特征则是文档中的单词。单词作为特征时，其假设是：某些单词相对而言更有可能出现在垃圾信息中。

```python
# docclass.py
import re
import math

def getwords(doc):
    splitter = re.compile('\\W*')
    # 根据非字母字符进行单词拆分
    words = [s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    # 只返回一组不重复的单词
    return {w:1 for w in words}
```

选择特征集时需要做大量的权衡，而且还要不断地进行调整


###对分类器进行训练 -- Training the Classifier

```python
class classifier:
    def __init__(self, getfeatures, filename=None):
        # 统计特征/分类组合的数量
        self.fc = {}
        # 统计每个分类中的文档数量
        self.cc = {}
        self.getfeatures = getfeatures

    def setdb(self, dbfile):
        self.con = sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')

    # 类方法不会直接引用这些字典，因为这会有碍于将训练数据存入文件或数据库的潜在选择。加入下列辅助函数
    def incf(self, f, cat):
        '''增加对特征/分类组合的计数值'''
        #self.fc.setdefault(f, {})
        #self.fc[f].setdefault(cat, 0)
        #self.fc[f][cat] += 1
        count = self.fcount(f, cat)
        if count == 0:
            self.con.execute("insert into fc values ('%s','%s'1)" % (f, cat))
        else:
            self.con.execute(
                "update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))

    def incc(self, cat):
        '''增加对某一分类的计数值'''
        #self.cc.setdefault(cat, 0)
        #sele.cc[cat] += 1
        count=self.catcount(cat)
        if count==0:
            self.con.execute("insert into cc values ('%s',1)" % (cat))
        else:
            self.con.execute("update cc set count=%d where category='%s'" 
                           % (count+1,cat)) 

    def fcount(self, f, cat):
        '''某一特征出现于某一分类中的次数'''
        #if f in self.fc and cat in self.fc[f]:
        #    return float(self.fc[f][cat])
        #return 0.0
        res=self.con.execute(
            'select count from fc where feature="%s" and category="%s"'
            %(f,cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    def catcount(self, cat):
        '''属于某一分类的内容项数量'''
        #if cat in self.cc:
        #    return float(self.cc[cat])
        #return 0
        res=self.con.execute('select count from cc where category="%s"'
            %(cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    def totalcount(self):
        '''所有内容项的数量'''
        #return sum(self.cc.values())
        res=self.con.execute('select sum(count) from cc').fetchone();
        if res==None: return 0
        return res[0]

    def categories(self):
        '''所有分类的列表'''
        #return self.cc.keys()
        cur=self.con.execute('select category from cc');
        return [d[0] for d in cur]

    def train(self, item, cat):
        '''将内容拆分为彼此独立的各个特征。
        针对该分类为每个特征增加计数值。增加对该分类的总计数值'''
        features = self.getfeatures(item)
        # 针对该分类为每个特征增加计数值
        for f in features:
            self.incf(f, cat)
        # 增加针对该分类的计数值
        self.incc(cat)
        self.con.commit()

    def fprob(self, f, cat):
        # 给定分类的单词概率——分类cat中出现特征f的概率
        if self.catcount(cat) == 0: return 0
        # 特征在分类中出现的总次数，除以分类中包含内容项的总数
        return self.fcount(f, cat)/self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        '''在我们手头掌握的有关当前特征的信息极为有限时，我们还需要根据一个假设的概率来作出判断'''
        # 计算当前的概率值
        basicprob = prf(f, cat)
        # 统计特征在所有分类中出现的次数
        totals = sum([self.fcount(f, c) for c in self.categories()])
        # 计算加权平均
        bp = ((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

# cl = classifier(getwords)
# cl.train('the quick brown fox jumps over the lazy dog', 'good')
# cl.train('make quick money in the online casino', 'bad')
# cl.fcount('quick', 'good')
# cl.fcount('quick', 'bad')

def sampletrain(cl):
    cl.train('Nobody owns the water', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')
```


###计算概率 -- Calculating Probabilities

fprob：给定分类的单词概率——分类cat中出现特征f的概率
为条件概率，记为Pr(A|B)，在给定B的条件下A的概率
本例中，Pr(word|classification)
classifier.fprob(self, f, cat)

sampletrain(cl)
cl.fprob('quick', 'good')


####从一个合理的推测开始 -- Starting with a Reasonable Guess

fprob方法针对目前为止见到过的特征与分类，给出了一个精确的结果。但它有一个小问题——只根据以往见过的信息，会令其在训练的初期阶段，对那些极少出现的单词变得异常敏感。

为解决上述问题，在我们手头掌握的有关当前特征的信息极为有限时，我们还需要根据一个假设的概率来作出判断。一个推荐的初始值是0.5.我们还要为假设的概率赋以多大的权重——权重为1代表假设概率的权重与一个单词相当。经过加权的概率值返回的是一个有getprobability与假设概率组成的加权平均。

```python
classifier.weightedprob(self, f, cat, prf, weight=1.0, ap=0.5)

sampletrain(cl)
cl.weightedprob('money', 'good', cl.fprob)
sampletrain(cl)
cl.weightedprob('money', 'good', cl.fprob)
```


###朴素分类器 -- A Naive Classifier

将各个单词的概率进行组合，从而得出整篇文档属于该分类的概率。
本章将考查两种不同的分类方法。

朴素贝叶斯分类器：朴素指的是它假设将要被组合的各个概率是彼此独立的。即，一个单词在属于某个指定分类的文档中出现的概率，与其他单词出现于该分类的概率是不相关的。

事实上文章中的各个单词并不是独立的，这意味着我们无法采用朴素贝叶斯分类器所求得的结果实际用作一篇文档属于某个分类的概率。不过，我们还是可以对各个分类的计算结果进行比较，然后在看哪个分类的概率最大。在现实中，若不考虑假设的潜在缺陷，朴素贝叶斯分类器将被证明是一种非常有效的文档分类方法。


####整篇文档的概率 -- Probability of a Whole Document

假设概率的彼此独立性
Pr(Document|Category) = Pr(w1|Category) * Pr(w2|Category)...

```python
class naivebayes(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.thresholds = {}

    def setthreshold(self, cat, t):
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def docprob(self, item, cat):
        '''得到整篇文档的概率'''
        features = self.getfeatures(item)

        # 将所有特征的概率相乘
        p = 1
        for f in features: p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        '''计算分类的概率 Pr(Category|Document)
        = Pr(Document|Category) * Pr(Category) / Pr(Document)
        '''
        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

    def classify(self, item, default=None):
        probs = {}
        # 寻找概率最大的分类
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        # 确保概率超出域值*次大概率值
        for cat in probs:
            if cat == best: continue
            if probs[cat] * self.getthreshold(best)>probs[best]: return default
        return best
```

####贝叶斯定理简介 -- A Quick Introduction to Bayes Theorem

贝叶斯定理是一种对条件概率进行调换求解（flipping around）的方法，通常写作：
Pr(A|B) = Pr(B|A) * Pr(A) / Pr(B)
在本例中，即为：
Pr(Category|Document) = Pr(Document|Category) * Pr(Category)/Pr(Document)
Pr(Document|Category) = Pr(w1|Category) * Pr(w2|Category)...
Pr(Category)是随机选择一篇文档属于该分类的概率，因此就是属于该分类的文档数除以文档的总数。

naivebayes.prob(self, item, cat)

```python
cl = naivebayes(getwords)
sampletrain(cl)
cl.prob('quick rabbit', 'good')
cl.prob('quick rabbit', 'bad')
```


####选择分类 -- Choosing a Category

构造朴素贝叶斯分类器的最后一个步骤是实际判定某个内容项所属的分类。
此处最简单的方法是计算被考查内容在每个不同分类中的概率，然后选择概率最大的分类。
在许多问题中无法将各个分类同等看待，如与将正常邮件归为垃圾邮件相比，偶尔收到几封垃圾邮件还是可以容忍的。在另一些应用中承认不知道答案，要好过判断答案就是概率值稍大一些的分类。

为解决这一问题，我们可以为每个分类定义一个最小阈值。
以垃圾邮件过滤为例，假如过滤到“bad”分类的阈值为3，则针对“bad”分类的概率就必须至少3倍于针对“good”分类的概率才行。假如针对“good”分类的阈值为1，则对于任何邮件，只要概率确实大于针对“bad“分类的概率，它就是属于”good“分类的。任何有可能属于”bad“分类，但概率并没有超过3倍以上的邮件，都将被划归到”未知“分类中。

```python
# 阈值操作
classifier.__init__(self, getfeatures)
classifier.setthreshold(self, cat, t)
classifier.getthreshold(self, cat)

# 分类
classifier.classify(self, item, default=None)

cl = naivebayes(getwords)
sampletrain(cl)
cl.classify('quick rabbit', default='unknown')
cl.classify('quick money', default='unknown')
cl.setthreshold('bad', 3.0)
cl.classify('quick money', default='unknown')
for i in range(10): sampletrain(cl)
cl.classify('quick money', default='unknown')
```

###费舍尔方法 -- The Fisher Method

以R.A.Fisher的名字命名的费舍尔方法，是朴素贝叶斯方法的一种替代方案，它可以给出非常精确的结果，尤其适合垃圾信息过滤。

与朴素贝叶斯过滤器利用特征概率来计算整篇文档的概率不同，费舍尔方法为文档中的每个特征都求得了分类的概率，然后又将这些概率组合起来，并判断其是否可能构成一个随机集合。尽管该方法更为复杂，但是因为它在分类选择临界值（cutoff）时允许更大的灵活性，所以还是值得一学的。


####针对特征的分类概率 -- Category Probabilities for Features

cprob：给定单词的分类概率——特征f出现在cat中的概率
Pr(category|feature)
(具有指定特征的属于某分类的文档数)/(具有指定特征的文档总数)

为了进行归一化计算，函数将分别求得3个量
* 属于某分类的概率 clf=Pr(feature|category)
* 属于所有分类的概率 freqsum = Pr(feature|category)之和
* cprob = clf/(clf+nclf)

```python
class fisherclassifier(classifier):
    def __init__(self, getfeatures):
        classifier.__init__(self, getfeatures)
        self.minimums = {}

    def setminimum(self, cat, min):
        self.minimums[cat] = min

    def getminimun(self, cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]

    def cprob(self, f, cat):
        '''特征f出现在cat中的概率'''
        # 特征在该分类中出现的频率
        clf = self.fprob(f, cat)
        if clf == 0: return 0
        # 特征在所有分类中出现的频率
        freqsum = sum([self.fprob(f,c) for c in self.categories()])
        # 概率等于特征在该分类中出现的频率除以总体频率
        p = clf/(freqsum)

        return p

    def fisherprob(self, item, cat):
        # 将所有概率值相乘
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
        # 取自然对数，并乘以-2
        fscore = -2 * math.log(p)
        # 利用倒置对数卡方函数求得概率
        return self.invchi2(fscore, len(features)*2)

    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default=None):
        # 循环遍历并寻找最佳结果
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            # 确保其超过下限值
            if p > self.getminimun(c) and p > max:
                best = c
                max = p
        return best

# cl = fisherclassifier(getwords)
# sampletrain(cl)
# cl.cprob('quick', 'good')
# cl.cprob('money', 'bad')
```

对于因为算法接触单词的次数太少，所以它有可能会对概率值估计过高。因此可以对概率进行加权处理

cl.weightedprob('money', 'bad', cl.cprob)


####将各概率值组合起来 -- Combining the Probabilities

费舍尔方法返回的结果是对概率的一种更好的估计，这对于结果报告或临界值判断而言是非常有价值的。

费舍尔方法的计算过程是将所有概率相乘起来，然后取自然对数，在将结果乘以-2

```python
fisherclassifier.fisherprob(self, item, cat)

cl = fisherclassifier(getwords)
sampletrain(cl)
cl.cprob('quick', 'good')
cl.fisherprob('quick rabbit', 'good')
cl.fisherprob('quick rabbit', 'bad')
```

####对内容项进行分类 -- Classifying Items

我们可以利用fisherprob的返回值来决定如何进行分类。不像贝叶斯过滤器那样需要乘以阈值，此处我们可以为每个分类指定下限。
在垃圾信息过滤器中，我们可以将“bad”分类的下限值设得很高，如0.6，将“good”分类的下限值设置得很低，比如0.2.任何针对“good”分类的分值低于0.2，针对“bad”分类的分值低于0.6的邮件，将被划归到“未知”分类中。

```python
fisherclassifier.__init__(self, getfeatures)
fisherclassifier.setminimum(self, cat, min)
fisherclassifier.getminimun(self, cat)
fisherclassifier.classify(self, item, default=None)

sampletrain(cl)
cl.classify('quick rabbit')
cl.classify('quick money')
cl.setminimum('bad', 0.8)
cl.classify('quick money')
cl.setminimum('good', 0.4)
cl.classify('quick money')
```


###将经过训练的分类器持久化 -- Persisting the Trained Classifiers

####Using SQLite

```python
import sqlite3 as sqlite

# 需要修改的函数
classifier.setdb(self, dbfile)
classifier.incf(self, f, cat)
classifier.fcount(self, f, cat)
classifier.incc(self, cat)
classifier.catcount(self, cat)
classifier.categories(self)
classifier.totalcount(self)

cl = fisherclassifier(getwords)
cl.setdb('test1.db')
sampletrain(cl)
cl2 = naivebayes(getwords)
cl2.setdb('test1.db')
cl2.classify('quick money')
```

###过滤博客订阅源 -- Filtering Blog Feeds

```python
import feedparser
import re

# Takes a filename of URL of a blog feed and classifies the entries
def read(feed,classifier):
  # Get feed entries and loop over them
  f=feedparser.parse(feed)
  for entry in f['entries']:
    print
    print '-----'
    # Print the contents of the entry
    print 'Title:     '+entry['title'].encode('utf-8')
    print 'Publisher: '+entry['publisher'].encode('utf-8')
    print
    print entry['summary'].encode('utf-8')
    

    # Combine all the text to create one item for the classifier
    fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

    # Print the best guess at the current category
    print 'Guess: '+str(classifier.classify(entry))

    # Ask the user to specify the correct category and train on that
    cl=raw_input('Enter category: ')
    classifier.train(entry,cl)


# cl = fisherclassifier(getwords)
# cl.setdb('python_feed.db')
# read('python_search.xml', cl)

# cl.cprob('python', 'prog')
# cl.cprob('python', 'snake')
# cl.cprob('python', 'monty')
# cl.cprob('eric', 'monty')
# cl.fprob('eric', 'monty')
```


###对特征检测的改进 -- Improving Feature Detection

几种不同的方法可以对其加以改进
* 不真正区分大写和小写的单词，而是将”含有许多大写单词“这样的现象作为一种特征
* 除了单个单词外，还可以使用词组
* 捕获更多的元信息，如：是谁发送的电子邮件，或者一篇博客被提交到了哪个分类下，可以将这样的信息标示为元信息
* 保持URL和数字原封不动，不对其进行拆分

```python
def entryfeatures(entry):
  splitter=re.compile('\\W*')
  f={}
  
  # Extract the title words and annotate
  titlewords=[s.lower() for s in splitter.split(entry['title']) 
          if len(s)>2 and len(s)<20]
  for w in titlewords: f['Title:'+w]=1
  
  # Extract the summary words
  summarywords=[s.lower() for s in splitter.split(entry['summary']) 
          if len(s)>2 and len(s)<20]

  # Count uppercase words
  uc=0
  for i in range(len(summarywords)):
    w=summarywords[i]
    f[w]=1
    if w.isupper(): uc+=1
    
    # Get word pairs in summary as features
    if i<len(summarywords)-1:
      twowords=' '.join(summarywords[i:i+1])
      f[twowords]=1
    
  # Keep creator and publisher whole
  f['Publisher:'+entry['publisher']]=1

  # UPPERCASE is a virtual word flagging too much shouting  
  if float(uc)/len(summarywords)>0.3: f['UPPERCASE']=1
  
  return f

cl = fisherclassifier(entryfeatures)
cl.setdb('python_feed.db')
read('python_search.xml', cl)
```

###Using Akismet

??

###替代方法 -- Alternative Methods

本章介绍的两个分类器都是监督型学习方法(supervised learning methods)的例子
第4章中的人工神经网络是另一个监督型学习的例子。通过将特征作为输入，并令输出代表每一种可能的分类，我们也可以将神经网络用于本章中的相同问题。
第9章中介绍的支持向量机(support vector machines)，也可以用于解决本章的问题

贝叶斯分类器被常用于文档分类的原因是，与其他方法相比它所要求的计算资源更少。
相对与神经网络的复杂性导致了其在理解上的困难，我们可以清楚地看到单词的概率，以及它们对最终分值的实际贡献有多大，而对于网络中两个神经元之间的连接强度而言，则并不存在同样简单的解释

另一方面，神经网络和支持向量机有一个很大的优势：它们可以捕捉到输入特征之间更为复杂的关系。神经网络中，某个特征的概率可能会依据其他特征的存在或缺失而改变。也许你正在试图阻止赌博的垃圾信息，但是有对跑马很感兴趣，在这种情况下，只有电子邮件中的其他地方没有出现单词'horse'时，单词'casino'才被认为'bad'的。朴素贝叶斯分类器无法捕获这样的相互依赖性，而神经网络却是可以的。


###Exercises

1. **改变假设概率** 请修改classifier类，使其能够支持对不同假设概率。修改init方法，使其能够接受其他分类器作为参数，并从一个更合理的假设概率推测值(而不是0.5)开始。
2. **计算 Pr(Document)** 在朴素贝叶斯分类器中，Pr(Document)的计算被略过了，因为它对于比较概率值而言并不是必需的。在特征彼此独立的前提下，事实上利用Pr(Document)来计算整体概率值是可行的。应该如何计算Pr(Document)呢？
 = Pr(w1) * Pr(w2) ...
3. **POP-3 电子邮件过滤器** Python有一个用于下载电子邮件的库，叫做poplib，请编写一段脚本，从服务器下载电子邮件，并尝试对其进行分类。一封电子邮件包含有哪些不同的属性？你将如何利用这些属性来构建特征提取函数呢？
4. **任意长度的短语** 本章为你示范了提取词组和单个单词的方法。请修改代码令特征提取过程变得可配置，使其能够一次提取出一组拥有指定数量的单词，并将之作为一个独立特征。
5. **保留IP地址** IP地址、电话号码，以及其他数字信息可能有助于对垃圾信息的识别。请修改特征提取函数，使其将这些信息作为特征加以返回（IP地址中包含有句号，但是你依然须要剔除句子间的句号）。
6. **其他虚拟特征** 有许多像UPPERCASE那样的虚拟特征，这些特征可能对文档分类很有帮助。篇幅过长的文档或长单词占据又是的情况也有可能是一种线索。请将这些情况也作为特征。你还能想到其他情况吗？
7. **神经网络分类器** 请修改第4章中的神经网络，利用它对文档进行分类。如何对神经网络的输出结果进行比较？编写一个程序对文档进行分类，并对其进行上千次的训练。记录每一种算法执行所需的时间。如何对这些算法做出对比呢？
> 输入层：文档特征（单词，作者等），隐含层：特征集合，输出层：分类类别
