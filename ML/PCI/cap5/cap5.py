#!/usr/bin/env python
#coding: utf-8

#优化 -- optimization

# 本章使用一系列被称为**随机优化**（stochatic optimization）的技术来解决协作类问题。
# 优化技术擅长于处理：受多种变量的影响，存在许多可能解的问题，以及结果因这些变量的组合而产生很大变化的问题。
# 优化技术的应用：
# 物理学中：研究分支运动
# 生物学中：预测蛋白质结构
# 计算机科学中；预测算法的最坏可能运行时间

# 原理：优化算法通过尝试许多不同题解并给这些题解打分以确定其质量的方式来找到一个问题的最优解。
# 应用场景：存在大量可能的题解以至于我们无法对它们进行一一尝试的情况。以一种对题解可能有改进的方式来对其进行智能化地修正。

# 例子：无法将输入用一个简单的公式映射到输出，所以要想找到最优解，就必须借助与优化算法
# 1. 制定组团旅游计划：
#  输入：
#    每个人的航班时间表
#    须要租用多少辆汽车
#    哪个飞机场是最通畅的
#  输出：
#    总的成本、侯机的时间、起飞的时间
# 2. 如何基于人们的偏好来分配有限的资源？
# 3. 如何用最少的交叉线来可视化社会网络？

##组团旅游 -- Group Travel

# 为来自不同地方去往同一地点的人们安排一次旅游是一件极富挑战性的事情。
# 要求：家庭成员来自全国各地，他们希望在纽约会面。他们将在同一天到达，并在同一天离开，而且他们想搭乘相同的交通工具往返飞机场。
# 每天有许多航班从任何一位家庭成员的所在地飞往纽约，飞机起飞时间是不同的，价格和续航时间上也都不尽相同。

# optimization.py
import time
import random
import math

people = [
    ('Seymour', 'BOS'),
    ('Franny', 'DAL'),
    ('Zooey', 'CAK'),
    ('Walt', 'MIA'),
    ('Buddy', 'ORD'),
    ('Les', 'OMA'),
]

destination = 'LGA'

flights = {}
#
for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])

    # 将航班详情添加到航班列表中
    flights[(origin, dest)].append((depart, arrive, int(price)))

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60+x[4]


##描述题解 -- Respresenting Solutions

# 使用数字序列描述题解：一个数字可以代表某人选择乘坐的航班--0是这天中的第一次航班，1是第二次...。因为每个人都需要往返两个航班，所以列表的长度是人数的两倍。

def printschedule(r):
    for d in range(len(r)/2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (
                name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

#print '打印航班'
#s = [1,4,3,2,7,3,6,3,2,4,5,3]
#printschedule(s)


##成本函数 -- The Cost Function

# **成本函数**是用优化算法解决问题的关键，它通常是最难确定的。成本函数需要返回一个值用以表示方案的好坏。对于**好坏的程度**没有特定的衡量尺度，唯一的要求就是函数返回的值越大，表示该方案越差。

# 通常根据从多变量来鉴别方案的好坏是比较困难的。我们来考查一些在组团旅游的例子中能被度量的变量：
# 价格：所有航班的总票价，或者有可能是考虑财务因素之后的加权平均
# 旅行时间：每个人在飞机上花费的时间
# 等待时间：在机场等待其他成员到达的时间
# 出发时间：早晨太早起飞的航班也许会产生额外的成本，因为这要求旅行者减少睡眠的时间
# 汽车租用时间：超过24小时要多符一天的租金

def schedulecost(sol):
    totalprice = 0
    lastestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol)/2):
        # 得到往程和返程航班
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]

        # 总价格等于所有往程航班和返程航班价格之和
        totalprice += outbound[2]
        totalprice += returnf[2]

        # 记录最晚到达时间和最早离开时间
        if lastestarrival < getminutes(outbound[1]): lastestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]): earliestdep = getminutes(returnf[0])
    # 每个人必须在机场等待直到最后一个人到达为止
    # 他们也必须在相同时间到达，并等候他们的返程航班
    totalwait = 0
    for d in range(len(sol)/2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]
        totalwait += lastestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep
    # 这个题解要求多付一天的汽车租用费用吗？如果是，费用为50美元
    # 书上似乎有误 >
    if lastestarrival < earliestdep: totalprice += 50

    return totalprice + totalwait

# 成本函数建立后，我们的目标就是要通过选择正确的数字序列来最小化该成本。理论上我们可以尝试10^12种组合确保我们得到最优的答案，但是这会花费非常长的时间。


##随机搜索 -- Random Searching

# 随机搜索不是一种非常好的优化算法，但是它却使我们很容易领会所有算法的真正意图，并且也是我们评估其他算法优劣的基线（baseline）

# 此函数会随机产生1000次猜测，并对每一次猜测调用costf。它会跟踪最佳猜测并将结果返回。
def randomoptimize(domain, costf):
    '''Domain是由一个二元组构成的列表，指定了每个变量的最小最大值
    costf成本函数
    '''
    best = 999999999
    bestr = None
    for i in range(1000):
        # 创建一个随机解
        r = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        # 得到成本
        cost = costf(r)
        # 与到目前为止的最优解进行比较
        if cost < best:
            best = cost
            bestr = r
    return r

#print '随机搜索'
#domain = [(0,9)]*(len(people)*2)
#s = randomoptimize(domain, schedulecost)
#schedulecost(s)
#printschedule(s)

# 缺点：尝试各种题解是非常低效的，因为这种方式没有充分利用已经发现的优解。


##爬山法 -- Hill Climbing

# 爬山法：随机搜索的一个替代方法。以一个随机解开始，然后在其临近的解集中寻找更好的题解（具有更低的成本）。类似从斜坡上向下走。

def hillclimb(domain, costf):
    # 创建一个随机解
    sol = [random.randint(domain[i][0], domain[i][1])
            for i in range(len(domain))]
    # 主循环
    while 1:
        # 创建相邻解的列表
        neighbors = []
        for j in range(len(domain)):
            # 在每个方向上相对于原值偏离一点
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1]+so[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+so[j+1:])
        # 在相邻解中寻找最优解
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]

        # 如果没有更好的解，则退出循环
        if best == current:
            break

    return sol


# 该函数在给定域内随机生成一个数字列表，用以构造初始的题解。它通过循环遍历列表中的每一个元素，找到当前解的所有相邻题解，然后创建出两个新的列表：一个列表中的元素加1，另一个列表中的元素减1.相邻解中最优的一个将成为新的当前题解。

#print '爬山法'
#s = hillclimb(domain, schedulecost)
#schedulecost(s)
#printschedule(s)

# 简单地从斜坡滑下不一定产生全局最优解。最后的解会是一个局部范围内的最小值，它比邻近解的表现都好，但却不是全局最优的。
# 解决这一难题的一种方法被成为**随机重复爬山法**（random-restart hill climbing）
# 还有模拟退火算法和遗传算法


##模拟退火算法 -- Simulated Annealing

# 模拟退火算法：受物理学领域启发而来的一种优化算法。退火是指将合金加热后再慢慢冷却的过程。大量的原子因为受到激发而向周围跳跃，然后有逐渐稳定到一个低能阶的状态，所以这些原子能够找到一个低能阶的配置（configuration）

# 算法的关键部分在于： 如果新的成本值更低，则新的题解就会成为当前题解，这和爬山法非常相似。不过，如果成本值更高的话，则新的题解仍将可能成为当前题解，这是避免局部最小值问题的一种尝试。
# 较差解被接受的概率为p=e^(-(highcost-lowcost)/temperature)
# 模拟退火算法之所以管用，因为它在退火过程的开始阶段会接受变现较差的解。随着退火过程的不断进行，算法越来越不可能接受较差的解，直到最后，它只会接受更优的解。

def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
    # 随机初始化值
    vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
    
    while T>0.1:
        # 选择一个索引值
        i = random.randint(0, len(domain)-1)

        # 选择一个改变索引值的方向
        dir = random.randint(-step, step)
        # 创建一个代表题解的新列表，改变其中一个值
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]: vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]: vecb[i] = domain[i][1]
        # 计算当前成本和新的成本
        ea = costf(vec)
        eb = costf(vecb)

        # 它是更好的解吗？或者是趋向最优解的可能的临界解吗？
        if (eb<ea or random.random()<pow(math.e, -(eb-ea)/T)):
            vec = vecb

        # 降低温度
        T = T * cool
    return vec

#print '模拟退火算法'
#s = annealingoptimize(domain, schedulecost)
#schedulecost(s)
#printschedule(s)


##遗传算法 -- Genetic Algorithms

# 遗传算法：受自然科学的启发，运行过程是先随机生成一组解，称之为**种群**（population）。在优化过程的每一步，算法会计算整个种群的成本函数，从而得到一个有关题解的有序列表。
# 在对题解进行排序之后，一个新的种群--我们称之为下一代被创建出来了。首先，进行**精英选拔法（elitism）：将但前种群中位于最顶端的题解加入其所在的新种群中。余下部分是有修改最优解后形成的全新解组成的。
# 两种修改题解的方法:
# 变异（mutation）：对一个既有解进行微小的、简单的、随机的改变。
# 交叉（crossover）或配对（breeding）：选取最有解中的两个解，然后将它们按某种方式进行结合。
# 一个新的种群是通过对最优解进行随机的变异和配对处理构造出来的，它的大小通常与旧的种群相同。尔后，这一过程会一直重复进行。达到指定的迭代次数，或者连续经过数代后题解都没有得到改善，整个过程就结束了。

def geneticoptimize(domain, costf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100):
    '''popsize:种群大小，mutprob:种群的新成员是由变异而非交叉得来的概率
    elite:种群中被认为是优解且被允许传入下一代的部分
    maxiter:需运行多少代
    '''
    # 变异(mutation)操作
    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]

    # 交叉(crossover)操作
    def crossover(r1, r2):
        i = random.randint(1, len(domain)-2)
        return r1[0:i]+r2[i:]

    # 构造初始种群
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1])
                for i in range(len(domain))]
        pop.append(vec)

    # 每一代中有多少胜出者？
    topelite = int(elite * popsize)

    # 主循环
    for i in range(maxiter):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s,v) in scores]

        # 从纯粹的胜出者开始
        pop = ranked[0:topelite]
        # 添加变异和配对后的胜出者
        while len(pop) < popsize:
            if random.random() < mutprob:
                # 变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                # 交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
        # 打印当前最优值
        print scores[0][0]

    return scores[0][1]

#print '遗传算法'
#s = geneticoptimize(domain, schedulecost)
#printschedule(s)

# 优化可能不起作用：一种优化方法是否管用很大程度上取决与问题本身。大多数优化算法都有赖于这样一个事实：对于大多数问题而言，最优解应该接近于其他的优解。
# 如果成本的最低点实际上处在一个非常陡峭的区域。接近它的任何解都有可能被排除在外，因为这些解的成本都很高，所以我们永远都找不到通往全局最小值的途径。大多数算法都会陷入图中左边某个局部最小化的区域里。


##真实的航班搜索 -- Real Flight Searches

###The Kayak API

###The minidom Package

###航班搜索 -- Flight Searches

##涉及偏好的优化 -- Optimizing for Preferences

# 本节我们考查另一个不同的问题：如何将有限的资源分配给多个表达了偏好的人，并尽可能使他们都满意或尽可能满意


###学生宿舍优化问题 -- Student Dorm Optimization

# 问题：依据学生的首选和次选，为其分配宿舍。
# 可以推广到：
# 在线纸牌游戏中玩家的牌桌分配
# 大型编程项目中开发人员的bug分配
# 家庭成员中的家务分配

# dorm.py
import random
import math

# 代表宿舍，每个宿舍有两个可用的隔间
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']
# 代表学生及其首选和次选
prefs = [
    ('Toby', ('Bacchus', 'Hercules')),
    ('Steve', ('Zeus', 'Pluto')),
    ('Audrea', ('Athena', 'Zeus')),
    ('Sarah', ('Zeus', 'Pluto')),
    ('Dave', ('Athena', 'Bacchus')),
    ('Jeff', ('Hercules', 'Pluto')),
    ('Fred', ('Pluto', 'Athena')),
    ('Suzie', ('Bacchus', 'Hercules')),
    ('Laura', ('Bacchus', 'Hercules')),
    ('Neil', ('Hercules', 'Athena')),
]

# [(0,9), (0,8), (0,7), (0,6),...,(0,0)]
domain = [(0, (len(dorms)*2)-i-1) for i in range(0, len(dorms)*2)]

def printsolution(vec):
    slots = []
    # 为每个宿舍建两个槽
    for i in range(len(dorms)): slots += [i,i]

    # 遍历每一名学生的安置情况
    for i in range(len(vec)):
        x = int(vec[i])

        # 从剩余槽中选择
        dorm = dorms[slots[x]]
        # 输出学生及其被分配的宿舍
        print prefs[i][0], dorm
        # 删除该槽
        del slots[x]


###成本函数 -- The Cost Function

def dormcost(vec):
    cost = 0
    # 建立一个槽序列
    slots = [0,0,1,1,2,2,3,3,4,4]
    # 遍历每一名学生
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        # 首选成本为0，次选成本为1
        if pref[0] == dorm: cost += 0
        elif pref[1] == dorm: cost += 1
        else: cost += 3
        # 不在选择之列则成本值为3

        # 删除选中的槽
        del slots[x]

    return cost

# 我们知道最优解的成本为零，当优化算法找到一个最优解时，我们可以让优化算法停止搜索更优的解，也可以了解目前与最优解的差距有多少。


###执行优化函数 -- Running the Optimization

print '分配宿舍'
s = randomoptimize(domain, dormcost)
print dormcost(s)
geneticoptimize(domain, dormcost)
printsolution(s)


##网络可视化 -- Network Visualization

###布局问题 -- The Layout Problem

# 运用优化算法来构建更好的而非杂乱无章的网络图。

# socialnetwork.py
import math
people = ['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']
links = [
    ('Augustus', 'Willy'),
    ('Mike', 'Joe'),
    ('Miranda', 'Mike'),
    ('Violet', 'Augustus'),
    ('Miranda', 'Willy'),
    ('Charlie', 'Mike'),
    ('Veruca', 'Joe'),
    ('Miranda', 'Augustus'),
    ('Willy', 'Augustus'),
    ('Joe', 'Charlie'),
    ('Veruca', 'Augustus'),
    ('Miranda', 'Joe'),
]

# **质点弹簧算法**（mass-and-sprint algorithm）：从物理学建模而来，各结点彼此向对方施以推力并试图分离，而结点间的连接则试图将关联结点彼此拉近。
# 借助质点弹簧算法网络便会逐渐呈现出这样一个布局：未关联的节点被推离，而关联的节点则被彼此拉近--却又不会靠得很拢。但该算法无法避免交叉线。

# 使用优化算法来构建布局：我们只需确定一个成本函数，并尝试令它返回值尽可能地小。在本例中一个值得一试的成本函数是计算彼此交叉的连线数。

###计算交叉线 -- Counting Crossed Lines

# 判断两条线段是否相交：计算线条的'分数值'。如果两条线的分数值介于0（表示线的一端）和1（表示线的另一端）之间，则它们彼此交叉。反之，则不交叉。

# socialnetwork.py
def crosscount(v):
    '''该函数遍历每一对连线，并利用连线端点的当前坐标来判断它们是否交叉。如果交叉，则总分加1。
    '''
    # 将数字序列转换成一个person:(x,y)的字典
    loc = {people[i]:(v[i*2], v[i*2+1]) for i in range(0, len(people))}
    total = 0
    # 遍历每一对连线
    for i in range(len(links)):
        for j in range(i+1, len(links)):
            # 获取坐标位置
            (x1,y1), (x2,y2) = loc[links[i][0]], loc[links[i][1]]
            (x3,y3), (x4,y4) = loc[links[j][0]], loc[links[j][1]]

            den = (y4-y3) * (x2-x1) - (x4-x3)*(y2-y1)

            # 如果两线平行，则den==0
            if den==0: continue

            # 否则，ua与ub就是两条交叉线的分数值
            ua = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
            ub = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
            # 如果两条线的分数值介于0和1之间，则两线彼此交叉
            if ua>0 and ua<1 and ub>0 and ub<1:
                total += 1

    # 对两个结点放置太近的题解进行'判罚'(penalize)
    for i in range(len(people)):
        for j in range(i+1, len(people)):
            # 获取两结点的位置
            (x1,y1),(x2,y2) = loc[people[i]], loc[people[j]]
            # 计算两结点的间距
            dist = math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
            # 对间距小于50个像素的结点进行判罚
            if dist < 50:
                total += (1.0 - (dist/50.0))

    return total

#print 'socialnetwork'
#sol = randomoptimize(domain, crosscount)
#print crosscount(sol)
#annealingoptimize(domain, crosscount, step=50, cool=0.99)
#print crosscount(sol)
#print sol


###绘制网络 -- Drawing the Network

import Image
import ImageDraw

def drawnetwork(sol):
    # 建立image对象
    img = Image.new('RGB',(400,400),(255,255,255))
    draw = ImageDraw.Draw(img)
    # 建立标示位置信息的字典
    pos = {people[i]:(sol[i*2],sol[i*2+1]) for i in range(0,len(people))}
    # 绘制连线
    for (a,b) in links:
        draw.line((pos[a], pos[b]), fill=(255,0,0))
    # 绘制代表人的结点
    for n,p in pos.items():
        draw.text(p, n, (0,0,0))

    img.show()


##其他可能的应用场合 -- Other Possiblities

##Exercises

# 1. **组团旅游的成本函数**：请以飞机上每分钟0.50美元的成本将总飞行时间计入成本。然后在尝试追加20美元的罚款，以确保任何人都能在上午8点之前抵达机场。

# 2. **退火算法的初始值**：模拟退火算法的结果很大程度上取决于其初始值。请构造一个优化函数，用多个初始值来模拟退火，并返回最优解。

# 3. **遗传优化算法的结束条件**：本章中的函数是以固定迭代次数来进行遗传优化的。请改变算法的结束条件，使其在经过10次迭代之后，任一最优解都没有任何改善时，方才结束。

# 4. **往返定价**：Kayak购买往返机票的价格可能会更加便宜。修改代码取得往返票价，并修改成本函数，令其针对某一特定往返航班进行票价查询，而不是只对单程票价进行求和运算

# 5. **学生组队**：假设并非要求学生列出对宿舍的偏好，而是令其表达对同住舍友的偏好。那么你将如何表达学生组队的结果呢？成本函数又将如何定义呢？

# 6. **连线夹角的判断**：请在连接同一个人的两线夹角非常小的时候，为网络布局算法的成本函数在增加一项成本。（提示：可以使用向量的叉乘）
