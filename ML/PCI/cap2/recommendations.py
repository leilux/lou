#/usr/bin/env python
#coding: utf-8
'''
第2章 提供推荐
making recommandations
'''
from math import sqrt

# 协作型过滤 (collaborative filtering)

## 搜集偏好
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5, 
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0, 
        'Superman Returns': 3.5, 
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0,
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0, 
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5, 
        'Superman Returns': 5.0, 
        'You, Me and Dupree': 3.0,
        'The Night Listener': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5, 
        'Snakes on a Plane': 3.0,
        #'Just My Luck': 1.5, 
        'Superman Returns': 3.5, 
        #'You, Me and Dupree': 3.0,
        'The Night Listener': 4.0,
    },
    'Claudia Puig': {
        'Lady in the Water': 4.5, 
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0, 
        'Superman Returns': 4.0, 
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5,
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0, 
        'Superman Returns': 3.0, 
        'You, Me and Dupree': 2.0,
        'The Night Listener': 3.0,
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0,
        #'Just My Luck': 1.5, 
        'Superman Returns': 5.0, 
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0,
    },
    'Toby': {
        #'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.5,
        #'Just My Luck': 1.5, 
        'Superman Returns': 4.0, 
        'You, Me and Dupree': 1.0,
        #'The Night Listener': 3.5
    },
}

## 寻找相近的用户 finding similar users

# 用于比较的度量算法
# http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples

### 欧几里德距离评价 euclidean distance score

# returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    '''
    1/(1+sum((p1.a-p2.a)**2 ...))
    '''
    # get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # if they have no ratings in common, return 0
    if (len) == 0: return 0
    # add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
            for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sqrt(sum_of_squares))

### 皮尔逊相关度评价 pearson correlation score

# returns the pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    ''' sum(p1.a * p2.a, ...) - sum(p1.a, ...)*sum(p2.a, ...)/n
        _______________________________________________________
        ____________________________________________________________________________
       V (sum(p1.a**2, ...)-sum(p1.a, ...)**2/n) * (sum(p2.a**2, ...)-sum(p2.a, ...)**2/n)
    '''
    # get the list of mutually reated items
    si = {item:1 for item in prefs[p1] if item in prefs[p2]}

    # find the number of elements 
    n = len(si)

    # if they are no ratings in common, return 0
    if n == 0: return 0

    # add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # sum up the products
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # calculate pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))
    if den == 0: return 0

    return num/den

### 为评论者打分 ranking the critics

# returns the best matches for person from the prefs dictionary.
# number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
            for other in prefs if other != person]

    # sort the list so the highest scores appear at the top
    scores.sort(reverse=True)
    return scores[0:n]


## 推荐物品 recommending items

# gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
    '''user-based '''
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # similarity * score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                # sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]

    # return the sorted list
    rankings.sort(reverse=True)
    return rankings


## 匹配商品 matching products -- 了解哪些商品是彼此相近的

# 各个人对某一商品评分的集合
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            # flip item and person
            result[item][person] = prefs[person][item]
    return result


## 构建一个基于del.icio.us的链接推荐系统 -- building a del.icio.us link recommender

### the del.icio.us API

### building the dataset

### recommanding neighbors and links

## 基于物品的过滤 -- Item-Based Filtering
s = '''
总体思路：为每件物品预先计算好最为相近的其他物品。然后，当我们想为某位用户提供推荐时，就可以查看他曾经评过分的物品，并从中选出排位靠前者，在构造出一个加权列表，其中包含了与这些选中物品最为相近的其他物品
'''

### building the item comparison dataset

def calculateSimilarItems(prefs, n=10):
    # create a dictionary of items showing which other items they
    # are most similar to.
    result = {}

    # invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # status updates for large datasets
        c += 1
        if c%100 == 0: print '%d / %d' % (c, len(itemPrefs))
        # find the most similar items to this one
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result

### 获得推荐-- getting recommendations

def getRecommendedItems(prefs, itemMatch, user):
    '''Item-based'''
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # loop over items rated by this user
    for (item, rating) in userRatings.items():
        # loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            # ignore if this user has already rated this item
            if item2 in userRatings: continue

            # weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # divide each total score by total weighting to get an average
    rankings = [(score/totalSim[item], item) for (item, score) in scores.items()]

    # return the ranking from highest to lowest
    rankings.sort(reverse=True)
    return rankings

## 使用MovieLens数据集 -- using the MovieLens dataset

## 基于用户进行过滤还是基于物品进行过滤 -- User-Based or Item-Based Filtering?

## Exercises

### 1. tanimote score

# A = [1,2,3,4]
# B = [1,2,5]
# C = A n B = [1,2]
# T = Nc / (Na + Nb - Nc) = 2/(4+3-2)=0.4

### 2. tag similarity


### 3. User-based efficiency

### 4. Item-based bookmark filtering

### 5. audioscrobbler
