##决策树建模 -- Modeling with Decision Trees

三个例子
1. 预测一个网站上有多少用户有可能会愿意为了某些高级功能而支付费用
2. 住房价格建模
3. 来自Hot or Not网站的热度(hotness)评价进行建模


###预测注册用户 -- Predicting Signups

```python
# treepredict.py
# 来源网站，位置，是否阅读过FAQ，浏览网页数，选择服务类型
my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]
```

我们已经掌握了用户相关的信息，包括：用户所在的位置，他们是通过哪些网站访问到这里的，以及他们在注册之前在这个网站上花费了多少时间；我们只须找到一种方法，能够将一个合理的推测值填入“服务”栏即可。


###引入决策树 -- Introducing Decision Trees

**决策树**：是一种更为简单的机器学习方法。它是对被观测数据（observations）进行分类的一种相当直观的方法，决策树在经过训练之后，看起来就像是以树状形式排列的一系列if-then语句。

```python
# 构造决策树的表达形式
class decisionnode:
    def __init__(self, col=-1, value=None, result=None, tb=None, fb=None):
        '''
        col是待检验的判断条件所对应的列索引，
        value对应于为了使结果为true，当前列必须匹配的值，
        tb和fb也是decisionnode，它们对应与结果分别为true或false时，树上相对于当前节点的子树上的节点，
        results保存的是针对于当前分支的结果，它是一个字典。除叶节点外，在其他节点上该值都为None。
        '''
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb
```


###对树进行训练 -- Training the Tree

本章使用一种叫做CART(classification and Regression Trees，即分类回归树)的算法：算法首先创建一个根节点。然后通过评估表中的所有观测变量，从中选出最合适的变量对数据进行拆分。

为此，算法考查了所有不同的变量，然后从中选出一个条件（如：是否读过FAQ？）对结果数据进行分解，以使我们能更容易地推测出用户的意图来。

```python
# 在某一列上对数据集合进行拆分，能够处理数值型数据或名词性数据
def divideset(rows, column, value):
    # 定义一个函数，令其告诉我们数据属于第一组(true)还是第二组(false)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    # 将数据集拆分成两个集合，并返回
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)
```

尝试按“Read FAQ”列对结果进行拆分：
```python
# import treepredict
# treepredict.divideset(treepredict.my_data, 2, 'yes')
```

目前，拆分结果所选用的变量并不是很理想，因为两边似乎都混杂了各种情况。我们需要一种方法来选择最合适的变量。


###选择最合适的拆分方案 -- Choosing the Best Split

我们要做的，就是找出合适的变量，使得生成的两个数据集合在混杂程度上能够尽可能小。
首先，用一个函数来对数据集合中的每一项结果进行技术。
然后，衡量数据集合中各种因素的混合情况。两种方法：
1. 基尼不纯度Gini Impurity：是指将来自集合中的某种结果随机应用于集合中某一数据项的预期误差率。
2. 熵Entropy：代表的是集合的无序程度——基本上就相当于我们在此处所说的集合的混杂程度。
两者的主要区别在于，熵达到峰值的过程要相对慢一些。因此，熵对于混乱集合的“判罚”往往要更重一些。

```python
def uniquecounts(rows):
    '''对各种可能的结果进行计数（结果为每一行数据的最后一列记录）
    '''
    results = {}
    for row in rows:
        r = row[-1]
        if r not in results: results[r] = 0
        results[r] += 1
    return results
```

####基尼不纯度 -- Gini Impurity

```python
def giniimpurity(rows):
    '''
    误差率的加权平均: c代表Ci分类的数量，t代表总数量
    [ c/t * (t-c)/t for c in [c1, c2, c3, ...]]
    '''
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts:
            if k1 == k2: continue
            p2 = float(counts[k2])/total
            imp += p1*p2
    return imp
```

####熵 -- Entropy

```python
def entropy(rows):
    '''
    p(i) = frequency(outcome) = count(outcome) / count(total rows)
    Entropy = [p(i)*log(p(i)) for p(i) in [...]]
    '''
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p*log2(p)
    return ent
```


###以递归方式构造树 -- Recursive Tree Building

为了弄明白一个属性的好坏程度，算法首先求出整个群组的熵，然后尝试利用每个属性的可能取值对群组进行拆分，并求出两个新群组的熵。计算相应的**信息增益**(Information gain，当前熵与两个新群组经加权平均后的熵之间的差值)，来确定哪个属性最适合用来拆分。
算法会针对每个属性计算相应的信息增益，然后从中选出信息增益最大的属性。
算法根据上步的属性将观测数据拆分成了两个组，其中一组符合判断条件，另一组则与判断条件不符。
算法随后会判断是否对其做进一步的拆分，或者我们已经获得了一个明确的结论而无须再行拆分了。
当拆分某个节点所得的信息增益不大与0的时候，对分支的拆分才会停止。

```python
def buildtree(rows, scoref=entropy):
    '''它通过为当前数据集选择最合适的拆分条件来实现决策树的构造过程
    '''
    if len(rows) == 0: return decisionnode()
        current_score = scoref(rows)

        # 定义一些变量以记录最佳拆分条件
        best_gain = 0.0
        best_criteria = None
        best_sets = None

        column_count = len(rows[0]) - 1
        for col in range(0, column_count):
            # 当前列中生成一个由不同值构成的序列
            column_values = {}
            for row in rows:
                column_values[row[col]] = 1
            # 接下来根据这一列中的每个值，尝试对数据集进行拆分
            for value in column_values.keys():
                (set1, set2) = divideset(rows, col, value)
                # 信息增益
                p = float(len(set1)) / len(rows)
                gain = current_score - p*scoref(set1) - (1-p)*scoref(set2)
                if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                    best_gain = gain
                    best_criteria = (col, value)
                    best_sets = (set1, set2)
            # 创建子分支
            if best_gain > 0:
                trueBranch = buildtree(best_sets[0])
                falseBranch = buildtree(best_sets[1])
                return decisionnode(col=best_criteria[0], value=best_criteria[1], tb=trueBranch, fb=falseBranch)
            else:
                return decisionnode(results=uniquecounts(rows))
```

代码假定了数据集的最后一列对应于目标值，我们只要简单地将数据集传进去，就可以构造出决策树来：

```
# reload(treepredict)
# tree = treepredict.buildtree(treepredict.my_data)
```


###决策树的显示 -- Displaying the Tree

```python
def printtree(tree, indent=''):
    # 这是一个叶节点吗？
    if tree.results != None:
        print str(tree.results)
    else:
        # 打印判断条件
        print str(tree.col) + ':' + str(tree.value) + '? '
        # 打印分支
        print indent + 'T->',
        printtree(tree.tb, indent+' ')
        print indent + 'F->',
        printtree(tree.fb, indent+' ')
```

####图形显示方式 -- Graphical Display

未看？?


###对新的观测数据进行分类 -- Classifying New Observations

接受新的观测数据作为参数，然后哦根据决策树对其进行分类。

```python
def classify(observations, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observations[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value: branch = tree.tb
            else: branch = tree.fb
        else:
            if v == tree.value: branch = tree.tb
            else: branch = tree.fb
        return classify(observations, branch)
```

每次调用之后，函数会根据调用结果来判断是否达到分支的末端。如果尚未达到末端，它会对观测数据作出评估，以确认列数据是否与参考值匹配。如果匹配，则会再次在True分支上调用classify；如果不匹配，则会在False分支上调用classify。
reload(treepredict)
treepredict.classify(['(direct)','USA','yes',5], tree)# {'Basic': 4}


###决策树的剪枝 -- Pruning the Tree

前述方法训练决策树会有一个问题，就是决策树可能会变得**过度拟合**(overfitted)。也就是说，它可能会变得过于针对训练数据。专门针对训练集所创建出来的分支，其熵值与真实情况相比可能会有所降低，但决策树上的判断条件实际上是完全随意的，因此一棵过度拟合的决策树所给出的答案也许比实际情况更具特殊性。

一种可能的解决办法是，只要当熵减少的数量小于某个最小值时，我们就停止分支的创建。
但是它有一个小小的缺陷——我们有可能会遇到这样的数据集：某一次分支的创建并不会令熵降低多少，但是随后创建的分支却会使熵大幅度降低。
对此，一种替代的策略是，先构造好如前所述的整颗树，然后在尝试消除多余的节点。这个过程就是剪枝。

剪枝算法：对具有相同父节点的一组节点进行检查，判断如果将其合并，熵的增加量是否会小于某个指定的阈值。如果确实如此，则这些节点会被合并成一个单一的节点，合并后的新节点包含了所有可能的结果值。这种做法有助于避免过度拟合的情况，也使得根据决策树作出的预测结果，不至于比从数据集中得到的实际结论还要特殊。

```python
def prune(tree, mingain):
    # 如果分支不是叶节点，则对其进行剪枝操作
    if tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb.results == None:
        prune(tree.fb, mingain)

    # 如果两个子分支都是叶节点，则判断它们是否需要合并
    if tree.tb.results != None and tree.fb.results != None:
        # 构造合并后的数据集
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]]*c
        for v, c in tree.fb.results.items():
            fb += [[v]]*c

        # 检查熵的减少情况
        delta = entropy(tb+fb) - (entropy(tb)+entropy(fb)/2)
        if delta < mingain:
            # 合并分支
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts(tb+fb)
```

###处理缺失数据 -- Dealing with Missing Data

除了易于解释外，决策树还有一个优点，就是它处理缺失数据的能力。我们所使用的数据集也许会缺失某些信息。为了使决策树能够处理这种情况，我们须要实现一个新的预测函数。

```python
def mdclassify(observations, tree):
    '''
    与classify相比，唯一的区别在于末尾处：如果发现有重要数据缺失，则每个分支的对应结果值都会被计算一遍，并且最终的结果值会乘以它们各自的权重。
    '''
    if tree.results != None:
        return tree.results
    else:
        v = observations[tree.col]
        if v ==  None:
            tr, fr = mdclassify(observations, tree.tb), mdclassify(observations, tree.fb)
            tcount = sum(tr.values())
            fcount = sum(fr.values())
            tw = float(tcount) / (tcount+fcount)
            fw = float(fcount) / (tcount+fcount)
            result = {}
            for k,v in tr.items(): result[k] = v*tw
            for k,v in fr.items():
                if k not in result: result[k] = 0
                result[k] += v*fw
            return result
        else:
          branch = None
          if isinstance(v, int) or isinstance(v, float):
              if v >= tree.value: branch = tree.tb
              else: branch = tree.fb
          else:
              if v == tree.value: branch = tree.tb
              else: branch = tree.fb
          return mdclassify(observations, branch)

# reload(treepredict)
# treepredict.mdclassify(['google', None, 'yes', None], tree)
# {'Premium': 1.5, 'Basic': 1.5}
# treepredict.mdclassify(['google', 'France', None, None], tree)
# {'None':0.125, 'Premium': 2.25, 'Basic': 0.125}
```


###处理数值型结果 -- Dealing with Numerical Outcomes

如果我们将所有数字都看作是不同的分类，那么目前的算法将不会考虑这样一个事实：有些数字彼此非常的接近，而其他数字则相差很远；我们将这些数字完全看成了绝对的离散。
为了解决这个问题，当我们拥有一棵以数字作为输出结果的决策树时，我们可以使用方差(variance)作为评价函数来取代熵或基尼不纯度。

```python
def variance(rows):
    if len(rows) == 0: return 0
    data = [float(row[-1]) for row in rows]
    mean = sum(data)/len(data)
    variance = sum([(d-mean)**2 for d in data])/len(data)
    return variance
```

当使用方差作为评价函数来构造决策树时，我们选择节点判断条件的依据就变成了：拆分之后令数字较大者位于树的一侧，数字较小者位于树的另一侧。以这种方式来拆分数据，就可以降低分支的整体方差。


###对住房价格进行建模 -- Modeling Home Prices


####The Zillow API


###对"热度"评价进行建模 -- Modeling "Hotness"


###什么时候使用决策树 -- When to Use Decision Trees

或许决策树最大的优势在于它可以轻易地对一个受训模型给予解释。在本章的例子里，执行完算法程序之后，我们不仅可以得到一棵用以预测新用户的决策树，而且还可以得到一个有助于我们做出判断的问题列表。

与其他几种机器学习算法不同，决策树可以同时接受分类(categorical)数据和数值(numerical)数据作为输入。不仅如此，许多算法在运行之前都要求我们必须对输入数据做预处理，或是归一化处理，而本章的代码却可以接受包括分类数据和数值数据在内的任何数据列表，并据此构造出相应的决策树来。

决策树还允许数据的不确定性分配（即允许数据的缺失）。在一棵决策树上也许会存在一部分节点，它们具有多种可能的结果值，但是又无法再进一步拆分。本章中的代码会返回一个字典对象，其中包含了针对不同结果的统计量，借助这一信息我们可以判断出结果的可信度。并不是所有算法都能够评估出一个不确定结果的概率来。

缺陷：对于只包含少数几种可能结果的问题而言，算法处理起来非常有效，但是当面对拥有大量可能结果的数据集时，算法就变得不那么有效了。当输出结果有上百个的时候，决策树就会变得异常复杂，而且预测的效果也可能会大打折扣。
只能创建满足“大于/小于”条件的节点。对于某些数据集，当我们对其进行分类的时候，决定分类的因素往往取决与更多变量的复杂组合，此时要根据前述的决策树进行分类就比较困难了。。例如，假设结果值是由两个变量的差来决定的，那么这棵树就会变得非常庞大，而且预测的准确性也会迅速下降。

总之，对于有大量数值型输入和输出的问题，决策树未必是一个好的选择；如果数值型输入之间存在许多错综复杂的关系，比如金融数据或影像，决策树同样也不一定是很好的选择。决策树最适合用来处理的，是那些带分界点(breakpoints)的、由大量分类数据和数值数据共同组成的数据集。如果对决策过程的理解至关重要，那么采用决策树就再合适不过了。


###Exercies

1. **针对结果的概率** 目前，classify和mdclassify函数都是以总计数值的形式给出最终结果的。请对它们进行修改，以给出最终结果属于某个分类的概率。 t=sum(results.values()); {k:v/t for k,v in results.items()}
2. **缺失数据的范围** mdclassify允许我们使用“None”来表示一个值的缺失。对数值型数据而言，其结果未必是绝对未知的，也许相应的取值会落在某个已知的范围内。请修改mdclassify函数，允许使用一个如(20,25)这样的元组来代替原来的单一值，并且如果有必要的话，对两个分支都进行遍历。
3. **提早停止向下拆分** 不同于对决策树的剪枝. buildtree可以在它到达某个节点,而该节点处对应熵的下降幅度又没有达到足够量的时候,停止继续向下拆分。有时这种做法未必能够达到理想的效果,但是它的确省去了额外的剪枝工作。消修改buildtree函数、令其接受一个代表最小增益的参数,一旦最小增益条件不满足，停止继续向下拆分。
```python
def buildtree(rows, scoref=entropy, mingain):
    ...
            # 创建子分支
            if best_gain > mingain:
    ...
```
4. **数据有缺失的决策树构造** 我们编写的函数能够对一个有缺失的数据行进行分类.但是如果训练集中也有数据缺失的现象,那又该怎么办呢?请修改buildtree函数,令其检查数据是否有缺失的情况,并且当我们无法将结果沿某个分支向下传递的时候,令其同时沿两个分支向下传递。
```
divideset >> set1, set2, set3(None)
best_sets = (set1+set3, set2+set3)
```
5. **多路径拆分** 本章中构造的所有树都是严格的二叉决策树。然而,有些数据集却允许我们可以将一个节点拆分成两个以上的分支,根据这些数据集构造出来的决策树也许会更加的简单。如果是这样的话,那么你将如何表达此类决策树?又如何对其加以训练呢?
